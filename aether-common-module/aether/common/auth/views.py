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

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    permission_classes,
    renderer_classes,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import requests

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group, Permission

from aether.common.auth.callbacks import register_user


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated, IsAdminUser])
def obtain_auth_token(request):
    '''
    Given a username generates an auth token for him/her.
    If the username does not belong to an existing user,
    it's going to be created with a long and random password.
    '''

    UserModel = get_user_model()
    user_model = UserModel.objects

    try:
        username = request.data['username']

        # gets the existing user or creates a new one
        try:
            user = user_model.get(username=username)
        except UserModel.DoesNotExist:
            user = user_model.create_user(
                username=username,
                password=user_model.make_random_password(length=100),
            )
        if settings.CAS_SERVER_URL:
            headers = {'Authorization': f'Token {settings.CAS_PROJECT_ADMIN_TOKEN}'}
            clientservice_name = settings.CAS_CLIENTSERVICE_NAME
            res = requests.get(
                f'{settings.CAS_SERVER_URL}/get-groups-for-user/{clientservice_name}/{user.username}/',
                headers=headers,
            )
            res.raise_for_status()
            role_names = res.json().get('result', [])
            register_user(user, role_names)

        # gets the user token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
