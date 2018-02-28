# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-10 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sync', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicedb',
            name='mobileuser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sync.MobileUser', related_name='devices'),
        ),
    ]