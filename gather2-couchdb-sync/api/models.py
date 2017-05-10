import logging
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .couchdb_helpers import create_db, delete_user, generate_db_name

logger = logging.getLogger(__name__)


class MobileUser(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return 'MobileUser: ' + self.email


class DeviceDB(models.Model):
    mobileuser = models.ForeignKey(MobileUser, on_delete=models.SET_NULL, null=True)
    device_id = models.TextField(unique=True)

    # used to log the sync execution
    last_synced_date = models.DateTimeField(null=True)
    last_synced_seq = models.TextField(null=True, default=0)
    last_synced_log_message = models.TextField(null=True)

    @property
    def db_name(self):
        ''' Returns the device's db name. '''
        return generate_db_name(self.device_id)


@receiver(post_save, sender=DeviceDB)
def device_db_post_save(sender, instance, *args, **kwargs):  # type: ignore
    ''' Create the accompaning couchdb db for the device db record '''
    # only create db when model is first saved
    if kwargs.get('created', False):
        create_db(instance.device_id)


@receiver(pre_delete, sender=MobileUser)
def mobile_user_pre_delete(sender, instance, *args, **kwargs):  # type: ignore
    ''' When a Mobile User is deleted, delete the CouchDB users to revoke sync access '''
    devices = instance.devicedb_set.all()
    for device in devices:
        delete_user(device.device_id)
