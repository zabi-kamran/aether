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
from django.http.response import JsonResponse
from django.shortcuts import redirect as redirect_response
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated

import base64
from jwcrypto.jwk import JWK
import jwt
import json
import requests


KC_URL = 'http://keycloak:8080/keycloak/auth/'  # internal, should through kong
KEYCLOAK_EXTERNAL = 'http://aether.local/keycloak/auth/'
REFRESH_URL = 'http://aether.local/auth/user/{realm}/refresh'

PK = {}

def get_public_key(kc_url, realm):
    CERT_URL = f'{kc_url}realms/{realm}/protocol/openid-connect/certs'
    res = requests.get(
        CERT_URL
    )
    jwk_key = res.json()['keys'][0]
    key_obj = JWK(**jwk_key)
    RSA_PUB_KEY = str(key_obj.export_to_pem(), 'utf-8')
    return RSA_PUB_KEY


class AetherKCMiddleware(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        cookies = request.COOKIES
        if 'aether-realm' and 'aether-jwt' in cookies:
            realm = request.COOKIES['aether-realm']
            token = request.COOKIES['aether-jwt']
            if not realm in PK:
                try:
                    PK[realm] = get_public_key(KC_URL, realm)
                except Exception as err:
                    return JsonResponse({"detail": 'Realm not found'},
                                    status=AuthenticationFailed.status_code)
            try:
                decoded = jwt.decode(token, PK[realm], audience='account', algorithms='RS256')
            except jwt.ExpiredSignatureError:  
                # We want to handle this with a redirect to the login screen.
                path = request.get_full_path()
                host = request.META['HTTP_X_FORWARDED_HOST']
                redirect = f'http://{host}{path}'
                url = REFRESH_URL.format(realm=realm) + f'?redirect={redirect}'
                return redirect_response(url)
                
            # Create user
            
            try:
                username = decoded['preferred_username']
            except KeyError:
                return JsonResponse({"detail": AuthenticationFailed.default_detail},
                                    status=AuthenticationFailed.status_code)
            try:
                UserModel = get_user_model()
                user_model = UserModel.objects
                user = user_model.get(username=username)
            except UserModel.DoesNotExist:
                user = user_model.create_user(
                    username=username,
                    password=user_model.make_random_password(length=100),
                )
            finally:
                # add user to request as request.user
                request.user = user

        return None