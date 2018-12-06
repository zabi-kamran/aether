from django_cas_ng.signals import cas_user_authenticated
from aether.common.auth.callbacks import auth_callback

kernel_auth_callback = auth_callback('kernel')
cas_user_authenticated.connect(kernel_auth_callback)

