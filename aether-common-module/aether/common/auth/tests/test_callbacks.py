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
        attributes = {
            'roles': 'org1:add,org1:delete,org1:change',
        }
        print(Group.objects.count())
        auth_callback('common')(None, user, attributes)
        for group in Group.objects.all():
            print('---------------', group)
            for permission in group.permissions.all():
                print(permission)
        print(Group.objects.count())
