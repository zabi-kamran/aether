# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-11 09:21
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kernel', '0016_auto_20180907_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappingset',
            name='schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]