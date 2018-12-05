from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from aether.common.auth.callbacks import auth_callback


class CallbacksTest(TestCase):

    def test_auth_callback(self):
        user = get_user_model().objects.create_user(
            username='test',
            password='testtest',
        )
        permissions = ['view', 'add', 'delete', 'change']
        attributes = {
            'roles': 'org1:add_token'
        }
        auth_callback(None, user, attributes)

