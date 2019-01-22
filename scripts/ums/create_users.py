import dotenv
import os
import requests

from requests.auth import HTTPBasicAuth

dotenv.load_dotenv('.env')

users = [
    {
        'username': 'tester',
        'password': 'testing',
        'groups': [
            {
                'project': 'kernel-local',
                'group_name': 'uploader',
            },
            {
                'project': 'odk-local',
                'group_name': 'uploader',
            },
            {
                'project': 'couchdb-sync-local',
                'group_name': 'uploader',
            },
            {
                'project': 'ui-local',
                'group_name': 'uploader',
            },
        ]
    },
]

base_url = 'http://0.0.0.0:8080'

auth = HTTPBasicAuth(
    username=os.environ['UMS_ADMIN_USERNAME'],
    password=os.environ['UMS_ADMIN_PASSWORD'],
)

for user in users:
    url = f'{base_url}/create-user/'
    res = requests.post(
        url,
        auth=auth,
        json=user,
    )
    res.raise_for_status()
    print(res.json())
