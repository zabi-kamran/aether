import re
import string
import random
from django.conf import settings
from couchdb_tools import api, setup

'''
Generate and update CouchDB credentials and dbs
(for mobile users authenticating via their google token)

This file contains tools to create and update CouchDB credentials and dbs.
Use the create_or_update_user function, which either creates a new set of credentials or
generates a new password for an existing user (as an automatic 'forgot password' function)
'''


def filter_id(device_id):
    #  filter according to:  http://docs.couchdb.org/en/master/api/database/common.html#put--db
    #  + remove some more special chars, since they're annoying
    return re.sub('[^a-z0-9_-]', '', device_id.lower())


def generate_password():
    '''
    Generate a long password string
    These passwords are never intended to be typed by hand, but rather
    used behind the scene to authenticate the mobile app

    http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630
    '''
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits + string.ascii_lowercase
    ) for _ in range(100))


def generate_user_id(device_id):
    return 'org.couchdb.user:{}'.format(filter_id(device_id))


def generate_db_name(device_id):
    return 'device_{}'.format(filter_id(device_id))


def create_db(device_id):
    db_name = generate_db_name(device_id)
    # Create or update the couchdb db where only the user has access
    setup.setup_db(db_name, {
        '_id': '_design/sync',
        'views': {
            'errors': {
                'map': 'function (doc) { if (doc.error) { emit(doc.time, doc.error); } }'
            }
        },
        '_security': {
            'admins': {'names': [], 'roles': []},
            'members': {'names': [], 'roles': [device_id]}
        }
    })


def create_user(email, password, device_id):
    '''
    Uses the email as username
    Creates a user for that username.
    '''
    # couchdb stops empty username
    # should throw on invalid password,
    if password is None or password == '':
        raise ValueError('No password Provided')

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
        'mobile_user': True
    }

    # this raises HttpError 409 if user exists
    r = api.put('_users/{}'.format(user_id), json=user_doc)
    r.raise_for_status()


def update_user(url, password, device_id, existing):
    '''
    Update existing user with new password
    '''
    del existing['derived_key']
    del existing['salt']
    existing['password'] = password
    existing['roles'].append(device_id)
    api.put(url, json=existing)


def create_or_update_user(email, device_id):
    '''
    For emails not having a CouchDB user, creates a DB, and a couchdb user,
    returns the credentials for that DB

    For emails with an existing user, generate a new password, update
    the user and return the new credentials set
    '''
    if email is None or email == '':
        raise ValueError('No email provided')

    username = filter_id(device_id)
    user_id = generate_user_id(device_id)

    if username is None or username == settings.COUCHDB_USER:
        raise ValueError('Invalid Device ID')

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
        'password': password
    }


def delete_user(device_id):
    # We need to retreive the revision to delete the user
    user_url = '_users/' + generate_user_id(device_id)
    get_user = api.get(user_url)

    if get_user.status_code != 200:
        return

    couch_user = get_user.json()
    r = api.delete(user_url + '?rev={}'.format(couch_user['_rev']))
    r.raise_for_status()
