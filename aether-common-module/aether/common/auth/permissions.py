# Copyright (C) 2018 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from django.contrib.auth.models import Group  # pragma: nocover
from django.apps import apps  # pragma: nocover
from guardian.shortcuts import (
    assign_perm,
    get_groups_with_perms,
    get_perms,
    get_perms_for_model,
)  # pragma: nocover

from rest_framework.permissions import DjangoObjectPermissions  # pragma: nocover
from rest_framework.response import Response  # pragma: nocover
from rest_framework.status import HTTP_201_CREATED  # pragma: nocover


def get_permissions_in_app(app_name):  # pragma: nocover
    config = apps.get_app_config(app_name)
    result = []
    for model in config.get_models():
        result.extend(get_perms_for_model(model))
    return result


def assign_permissions(group_names, instance):  # pragma: nocover
    if group_names:
        for group_name in group_names:
            group, _ = Group.objects.get_or_create(name=group_name)
            perms = get_perms_for_model(instance)
            # TODO: use group names directly, e.g.
            # org1:view_project -> Permission(codename='view_project')
            for p in perms:
                group.permissions.add(p)
                assign_perm(p.codename, group, instance)
            # TODO: redundant?
            group.save()


def assign_permissions_via_project(project, instance):  # pragma: nocover
    groups = get_groups_with_perms(project)
    for group in groups.all():
        try:
            project_permissions = get_perms(group, project)
        except Exception:
            # TODO: log
            # import ipdb; ipdb.set_trace()
            return
        for project_permission in project_permissions:
            permission = project_permission.split('_')[0] + '_' + instance.__class__.__name__.lower()
            try:
                assign_perm(permission, group, instance)
            except Exception:
                # TODO: log
                # import ipdb; ipdb.set_trace()
                return


def create_with_permissions(cls, request, *args, **kwargs):  # pragma: nocover
    serializer = cls.get_serializer(data=request.data)
    model = serializer.Meta.model
    serializer.is_valid(raise_exception=True)
    cls.perform_create(serializer)
    permissions = get_perms_for_model(model)
    for group in request.user.groups.all():
        for permission in permissions:
            assign_perm(permission.codename, group, serializer.instance)
    headers = cls.get_success_headers(serializer.data)
    return Response(
        serializer.data,
        status=HTTP_201_CREATED,
        headers=headers
    )


class CreateWithPermissionsMixin(object):  # pragma: nocover
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        model = serializer.Meta.model
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        permissions = get_perms_for_model(model)
        for group in request.user.groups.all():
            for permission in permissions:
                assign_perm(permission.codename, group, serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
            headers=headers
        )


class CustomObjectPermissions(DjangoObjectPermissions):  # pragma: nocover
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
