from django.contrib.auth.models import Permission
from django.test import TestCase

from aether.odk.api import models

from aether.common.auth.permissions import assign_permissions

"""
check if model has the expected permissions

check if user with permissions can be created

check if object-level permissions can be assigned to user

create resource for user
user retrieves resource
checks if permissions are created

"""

class TestPermissions(TestCase):

    def setUp(self):
        self.b = 1234

    def test_project_has_permissions(self):
        print(models.Project._meta.permissions)
        # import ipdb; ipdb.set_trace()
        # for p in Permission.objects.all():
        #     print(p)
        print(assign_permissions)
