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

import re
import string
import random

from django.conf import settings
from django.utils.translation import ugettext as _

from ..couchdb import api, setup

'''
Generate and update CouchDB credentials and dbs
(for mobile users authenticating via their google token)

The CouchDB User represents a Device. There should be one username per device id not per
mobile user, that can be shared among different devices.

This file contains tools to create and update CouchDB credentials and dbs.

Use the create_or_update_user function, which either creates a new set of credentials or
generates a new password for an existing user (as an automatic 'forgot password' function).
'''


def filter_id(device_id):
    #  filter according to:  http://docs.couchdb.org/en/master/api/database/common.html#put--db
    #  + remove some more special chars, since they're annoying
    return re.sub(r'[^a-z0-9_-]', '', device_id.lower())


def generate_password():
    '''
    Generate a long password string.

    These passwords are never intended to be typed by hand, but rather
    used behind the scene to authenticate the mobile app.

    http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630
    '''

    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase
    ) for _ in range(100))


def generate_user_id(device_id):
    '''
    Generates CouchDB user (uses ``device_id`` but removes special chars).
    '''

    return f'org.couchdb.user:{filter_id(device_id)}'


def generate_db_name(device_id):
    '''
    Generates device CouchDB name (uses ``device_id`` but removes special chars).
    '''

    return f'device_{filter_id(device_id)}'


def create_db(device_id):
    '''
    Creates device CouchDB database.
    '''

    db_name = generate_db_name(device_id)
    # Create or update the couchdb db where only the user has access
    setup.setup_db(db_name, {
        '_id': '_design/sync',
        'views': {
            'data': {
                'map': 'function (doc) { if (!doc.type || doc.type !== "sync_doc") { emit(doc._id, doc._rev); } }'
            },
            'errors': {
                'map': 'function (doc) { if (doc.error) { emit(doc.time, doc.error); } }'
            },
            'log': {
                'map': 'function (doc) { if (doc.type === "sync_doc") { emit(doc.time, doc.aether_id || doc.error); } }'
            }
        },
        '_security': {
            'admins': {'names': [], 'roles': []},
            'members': {'names': [], 'roles': [device_id]},
        },
    })


def create_user(email, password, device_id):
    '''
    - Uses the device id as username.
    - Creates a user for that username.
    - Grants permission to sync this device.
    '''

    # couchdb stops empty username
    # should throw on invalid password,
    if password is None or password == '':
        raise ValueError(_('No password Provided'))

    username = filter_id(device_id)
    user_id = generate_user_id(username)

    # http://docs.couchdb.org/en/master/intro/security.html#users-documents
    user_doc = {
        'name': username,
        'password': password,
        'roles': [device_id],
        'type': 'user',
        # meta fields
        'email': email,
        'mobile_user': True,
    }

    # this raises HttpError 409 if user exists
    r = api.put(f'_users/{user_id}', json=user_doc)
    r.raise_for_status()


def update_user(url, password, device_id, existing):
    '''
    Updates existing user with new password.
    '''

    del existing['derived_key']
    del existing['salt']
    existing['password'] = password
    existing['roles'].append(device_id)
    api.put(url, json=existing)


def create_or_update_user(email, device_id):
    '''
    - For devices not having a CouchDB user, creates a DB, and a couchdb user,
      and returns the credentials for that DB.

    - For devices with an existing user, generates a new password, updates the user,
      and returns the new credentials set.
    '''

    if email is None or email == '':
        raise ValueError(_('No email provided'))

    if device_id is None or device_id == '':
        raise ValueError(_('No Device ID provided'))

    username = filter_id(device_id)
    user_id = generate_user_id(device_id)

    if username == '' or username == settings.COUCHDB_USER:
        raise ValueError(_('Invalid Device ID'))

    user_url = '_users/{}'.format(user_id)

    r = api.get(user_url)
    exists = r.status_code < 400

    password = generate_password()

    if exists:
        update_user(user_url, password, device_id, r.json())
    else:
        create_user(email, password, device_id)

    return {
        'username': username,
        'password': password,
    }


def delete_user(device_id):
    '''
    Removes user. Revokes sync access to any Device with this user account.
    '''

    # We need to retrieve the revision to delete the user
    user_url = '_users/' + generate_user_id(device_id)
    get_user = api.get(user_url)

    if get_user.status_code != 200:
        return

    couch_user = get_user.json()
    r = api.delete('{url}?rev={rev}'.format(url=user_url, rev=couch_user['_rev']))
    r.raise_for_status()


def create_document(device_id, doc):
    '''
    Creates document in the device database.
    '''
    return api.post(generate_db_name(device_id), json=doc)
