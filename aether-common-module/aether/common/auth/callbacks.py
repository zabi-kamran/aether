from django.contrib.auth.models import Group, Permission

from rest_framework.authtoken.models import Token


def auth_callback(sender, user=None, attributes=None, **kwargs):
    if attributes.get('roles'):
        for role_name in attributes.get('roles', '').split(','):
            organisation, permission_codename = role_name.split(':')
            group, _ = Group.objects.get_or_create(name=role_name)
            group.user_set.add(user)
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.add(permission)
        token, _ = Token.objects.get_or_create(user=user)
        token.save()
        user.save()
