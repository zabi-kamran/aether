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

import mock

from aether.sync.api.tests import ApiTestCase, DEVICE_TEST_FILE

from ..couchdb_file import load_backup_file


class LoadFileViewsTests(ApiTestCase):

    def test__load_backup_file(self):
        with open(DEVICE_TEST_FILE, 'rb') as fp:
            stats = load_backup_file(fp)

        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['success'], 3)
        self.assertEqual(stats['erred'], 0)

    @mock.patch('aether.sync.api.couchdb_file.create_db', side_effect=Exception)
    def test__load_backup_file__couchdb_error(self, mock_create_db):
        with open(DEVICE_TEST_FILE, 'rb') as fp:
            stats = load_backup_file(fp)
            mock_create_db.assert_called_once()

        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['success'], 0)
        self.assertEqual(stats['erred'], 3)
