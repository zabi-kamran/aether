# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-31 07:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_pipeline_published_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertokens',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserTokens',
        ),
    ]