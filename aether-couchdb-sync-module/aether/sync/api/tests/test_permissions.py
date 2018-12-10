import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from guardian.shortcuts import get_perms_for_model

from aether.common.auth.permissions import assign_permissions

from ..models import Project, Schema
from . import trigger_auth_callback, default_auth_roles


class TestPermissions(TestCase):

    def assert_has_permissions(self, user, instance):
        for permission in get_perms_for_model(instance):
            has_permission = user.has_perm(permission.codename, instance)
            self.assertTrue(has_permission, permission.codename)

    def assert_has_no_permissions(self, user, instance):
        for permission in get_perms_for_model(instance):
            has_permission = user.has_perm(permission.codename, instance)
            self.assertFalse(has_permission, permission.codename)

    def test_permissions(self):
        '''
        Assert that all models which have a foreign key relationship to a
        Project will inherit that project's permissions.
        '''
        user = get_user_model().objects.create(
            username='test',
            password='testtest',
        )
        trigger_auth_callback(user)
        name = 'a-project-name'
        id = uuid.uuid4()
        project = Project.objects.create(name=name, project_id=id)
        self.assert_has_no_permissions(user, project)
        assign_permissions(default_auth_roles, project)
        self.assert_has_permissions(user, project)
        schema = Schema.objects.create(
            project=project,
            avro_schema={'name': 'name'}
        )
        self.assert_has_permissions(user, schema)
