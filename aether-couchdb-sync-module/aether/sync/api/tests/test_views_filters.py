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
from django.test import TestCase

from aether.common.auth.callbacks import auth_callback
from aether.common.auth.permissions import assign_permissions

from ..models import Project, Schema
from . import ApiTestCase, trigger_auth_callback, default_auth_roles


class FilterViewsTests(TestCase):

    def setUp(self):
        super(FilterViewsTests, self).setUp()

        username = 'test'
        email = 'test@example.com'
        password = 'testtest'
        self.user = get_user_model().objects.create_user(username, email, password)
        self.assertTrue(self.client.login(username=username, password=password))
        trigger_auth_callback(self.user)

    def tearDown(self):
        super(FilterViewsTests, self).tearDown()
        self.client.logout()

    def test__schema__filters(self):
        projects = []
        for i in range(4):
            projects.append(
                Project.objects.create(name=f'sample-{i}')
            )

        for project_index, project_name in zip([0, 0, 1, 2], ['1', '2', '3', '4']):
            schema = Schema.objects.create(project=projects[project_index], name=project_name, avro_schema={})
            assign_permissions(group_names=default_auth_roles, instance=schema)

        response = self.client.get('/schemas.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 4)

        url = '/schemas.json?project_id={}'.format(projects[0].pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

        url = '/schemas.json?project_id={}'.format(projects[1].pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

        url = '/schemas.json?project_id={}'.format(projects[2].pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

        url = '/schemas.json?project_id={}'.format(projects[3].pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
