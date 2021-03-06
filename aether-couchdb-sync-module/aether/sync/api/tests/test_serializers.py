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

import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

from ..serializers import SchemaSerializer
from ..models import Project


AVRO_SAMPLE = {
    'namespace': 'org.ehealthafrica.sample',
    'name': 'Person',
    'type': 'record',
    'fields': [
        {
            'name': 'first_name',
            'type': 'string',
        },
        {
            'name': 'last_name',
            'type': 'string',
        },
        {
            'doc': 'UUID',
            'name': 'id',
            'type': 'string',
        },
    ],
}


class SerializersTests(TestCase):

    def setUp(self):
        super(SerializersTests, self).setUp()
        self.request = RequestFactory().get('/')

        project = Project.objects.create(name='sample')
        self.KERNEL_ID = str(project.pk)

    def test_schema_serializer__no_file(self):
        schema = SchemaSerializer(
            data={
                'project': self.KERNEL_ID,
                'kernel_id': self.KERNEL_ID,
                # 'name': 'person',  # take name from AVRO schema
                'avro_schema': AVRO_SAMPLE,
            },
            context={'request': self.request},
        )
        self.assertTrue(schema.is_valid(), schema.errors)
        schema.save()

        self.assertEqual(schema.data['avro_schema'], AVRO_SAMPLE)
        self.assertEqual(schema.data['name'], 'Person')

    def test_schema_serializer__with_file(self):
        schema = SchemaSerializer(
            data={
                'project': self.KERNEL_ID,
                'kernel_id': self.KERNEL_ID,
                'name': 'person',
                'avro_file': SimpleUploadedFile('person.avsc', json.dumps(AVRO_SAMPLE).encode('utf-8')),
            },
            context={'request': self.request},
        )

        self.assertTrue(schema.is_valid(), schema.errors)
        schema.save()
        self.assertEqual(schema.data['avro_schema'], AVRO_SAMPLE)

    def test_schema_serializer__with_wrong_file(self):
        schema = SchemaSerializer(
            data={
                'project': self.KERNEL_ID,
                'kernel_id': self.KERNEL_ID,
                'name': 'person',
                'avro_file': SimpleUploadedFile('person.avsc', b'{"name"}'),
            },
            context={'request': self.request},
        )

        self.assertFalse(schema.is_valid(), schema.errors)
        self.assertIn('avro_file', schema.errors)
