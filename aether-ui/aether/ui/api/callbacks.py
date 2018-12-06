from django_cas_ng.signals import cas_user_authenticated
from aether.common.auth.callbacks import auth_callback

ui_auth_callback = auth_callback('ui')
cas_user_authenticated.connect(ui_auth_callback)

