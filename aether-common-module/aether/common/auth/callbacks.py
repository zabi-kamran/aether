from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group, Permission

from rest_framework.authtoken.models import Token

additional_permissions = {
    'odk': [
        'add_user',
        'view_user',
        'change_user',
        'delete_user',
    ]
}

def register_user(user, role_names):
    app_name = settings.AETHER_MODULE_NAME
    app_config = apps.get_app_config(app_name)
    model_names = [model.__name__.lower() for model in app_config.get_models()]
    for role_name in role_names:
        organisation, permission_name = role_name.split(':')
        group, _ = Group.objects.get_or_create(name=role_name)
        group.user_set.add(user)
        for model_name in model_names:
            permission_codename = f'{permission_name}_{model_name}'
            permission = Permission.objects.get(
                codename=permission_codename
            )
            group.permissions.add(permission)
        for permission_codename in additional_permissions.get(app_name, []):
            permission = Permission.objects.get(
                codename=permission_codename
            )
            group.permissions.add(permission)


def auth_callback(app_name):  # pragma: nocover
    def inner(sender, user=None, attributes=None, **kwargs):  # pragma: nocover
        app_config = apps.get_app_config(app_name)
        model_names = [model.__name__.lower() for model in app_config.get_models()]
        if attributes.get('roles'):
            role_names = attributes.get('roles', '').split(',')
            register_user(user, role_names)
        token, _ = Token.objects.get_or_create(user=user)
        user.save()  # TODO: redundant?
    return inner
