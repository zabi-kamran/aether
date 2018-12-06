from django_cas_ng.signals import cas_user_authenticated
from aether.common.auth.callbacks import auth_callback

sync_auth_callback = auth_callback('sync')
cas_user_authenticated.connect(sync_auth_callback)

