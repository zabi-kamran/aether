# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-26 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odk', '0002_auto_20170213_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xform',
            name='username',
        ),
        migrations.AlterField(
            model_name='xform',
            name='title',
            field=models.CharField(default='', editable=False, max_length=64, unique=True),
        ),
    ]