import requests

from requests.auth import HTTPBasicAuth

projects = [
    {
        'name': 'kernel-local',
        'auth_methods': ['ums'],
        'clientservice': {
            'name': 'a',
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
    },
    {
        'name': 'odk-local',
        'auth_methods': ['ums'],
        'clientservice': {
            'name': 'a',
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
    username='asdf',
    password='asdfasdfasdf',
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
