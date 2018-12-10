from django.apps import apps
from django.contrib.auth.models import Group, Permission

from rest_framework.authtoken.models import Token


def auth_callback(app_name):  # pragma: nocover
    def inner(sender, user=None, attributes=None, **kwargs):  # pragma: nocover
        app_config = apps.get_app_config(app_name)
        model_names = [model.__name__.lower() for model in app_config.get_models()]
        if attributes.get('roles'):
            for role_name in attributes.get('roles', '').split(','):
                organisation, permission_name = role_name.split(':')
                group, _ = Group.objects.get_or_create(name=role_name)
                group.user_set.add(user)
                for model_name in model_names:
                    permission_codename = f'{permission_name}_{model_name}'
                    permission = Permission.objects.get(codename=permission_codename)
                    group.permissions.add(permission)
            token, _ = Token.objects.get_or_create(user=user)
            token.save()
            user.save()
    return inner
