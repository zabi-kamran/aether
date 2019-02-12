#!/usr/bin/env python

# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
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

import json
import os
import requests

from jwcrypto.jwk import JWK
from keycloak import KeycloakAdmin

from settings import (
    KEYCLOAK_URL,
    CONSUMERS_URL,

    KC_URL,
    KC_ADMIN_USER,
    KC_ADMIN_PASSWORD,
    KC_MASTER_REALM,

    REALMS_PATH,
)


# Get administrative Token with KC Master Credentials

def make_realm(name, config):
    print(f'Creating realm: {name}')

    keycloak_admin = KeycloakAdmin(server_url=KC_URL,
                                   username=KC_ADMIN_USER,
                                   password=KC_ADMIN_PASSWORD,
                                   realm_name=KC_MASTER_REALM,
                                   verify=False)

    token = keycloak_admin.token['access_token']

    # Register realm with provided config
    realm_url = f'{KC_URL}admin/realms'
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {token}',
    }
    res = requests.post(realm_url, headers=headers, data=json.dumps(config))
    if not res.status_code is 201:
        print(res.json())
        raise ValueError('Could not create realm.')

    # Make a Single Kong Consumer for JWT covering the whole realm.
    data = {
        'username': f'{name}-jwt-consumer',
    }
    res = requests.post(CONSUMERS_URL, data=data)
    res.raise_for_status()

    details = res.json()
    consumer_id = details['id']

    # Get the public key from Keycloak
    CERT_URL = f'{KC_URL}realms/{name}/protocol/openid-connect/certs'
    res = requests.get(CERT_URL)
    res.raise_for_status()

    jwk_key = res.json()['keys'][0]

    # Transform JWK into a PEM.
    key_obj = JWK(**jwk_key)
    RSA_PUB_KEY = str(key_obj.export_to_pem(), 'utf-8')

    # Add JWT public key to Kong Consumer
    CONSUMER_CREDENTIALS_URL = f'{CONSUMERS_URL}/{consumer_id}/jwt'
    data = {
        'key': f'{KEYCLOAK_URL}realms/{name}',
        'algorithm': 'RS256',
        'rsa_public_key': RSA_PUB_KEY,
    }
    res = requests.post(CONSUMER_CREDENTIALS_URL, data=data)
    res.raise_for_status()

    print(f'Realm: {name} created on keycloak: {KEYCLOAK_URL}')


def find_available_realms():
    realms = {}
    _files = os.listdir(REALMS_PATH)
    for f in _files:
        name = f.split('.json')[0]
        with open(f'{REALMS_PATH}/{f}') as _f:
            config = json.load(_f)
            realms[name] = config
    return realms


if __name__ == '__main__':
    realms = find_available_realms()
    for name, config in realms.items():
        make_realm(name, config)