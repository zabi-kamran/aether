import requests
import os

from requests.auth import HTTPBasicAuth

def make_project(project_name, hostname):
    return {
        'name': project_name,
        'auth_methods': ['ums'],
        'clientservice': {
            'name': f'{project_name}-clientservice',
            'hostname': 'kernel.aether.local',
        },
        'groups': [
            {
                'name': 'uploader',
                'roles': [
                    {'name': 'org-1:view'},
                    {'name': 'org-1:add'},
                    {'name': 'org-1:change'},
                    {'name': 'org-1:delete'},
                ]
            },
            {
                'name': 'analyst',
                'roles': [
                    {'name': 'org-1:view'},
                ]
            },
        ]
    }

projects = [
    make_project('kernel-local', 'kernel.aether.local'),
    {
        'name': 'odk-local',
        'auth_methods': ['ums'],
        'clientservice': {
            'name': 'odk-aether-local',
            'hostname': 'odk.aether.local',
        },
        'groups': [
            {
                'name': 'uploader',
                'roles': [
                    {'name': 'org-1:view'},
                    {'name': 'org-1:add'},
                    {'name': 'org-1:change'},
                    {'name': 'org-1:delete'},
                ]
            },
            {
                'name': 'analyst',
                'roles': [
                    {'name': 'org-1:view'},
                ]
            },
        ]
    },
]

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
                'project': 'kernel-local',
                'group_name': 'analyst',
            },
        ]
    },
]

base_url = 'http://0.0.0.0:8080'

auth = HTTPBasicAuth(
    username=os.environ['UMS_ADMIN_USERNAME'],
    password=os.environ['UMS_ADMIN_PASSWORD'],
)

for project in projects:
    url = f'{base_url}/create-project/'
    res = requests.post(
        url,
        auth=auth,
        json=project,
    )
    res.raise_for_status()
    print(res.json())

for user in users:
    url = f'{base_url}/create-user/'
    res = requests.post(
        url,
        auth=auth,
        json=user,
    )
    res.raise_for_status()
    print(res.json())
