from django_cas_ng.signals import cas_user_authenticated
from aether.common.auth.callbacks import auth_callback

odk_auth_callback = auth_callback('odk')
cas_user_authenticated.connect(odk_auth_callback)

