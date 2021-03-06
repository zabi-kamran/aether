# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-12 09:38
from __future__ import unicode_literals

import aether.kernel.api.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kernel', '0002_auto_20171218_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('submission_revision', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('attachment_file', models.FileField(upload_to=aether.kernel.api.models.__attachment_path__)),
                ('md5sum', models.CharField(blank=True, max_length=36)),
            ],
            options={
                'ordering': ['submission', 'submission_revision', 'name'],
                'default_related_name': 'attachments',
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='kernel.Submission'),
        ),
        migrations.AlterModelOptions(
            name='mapping',
            options={'ordering': ['name', 'revision']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name', 'revision']},
        ),
        migrations.AlterModelOptions(
            name='schema',
            options={'ordering': ['name', 'revision']},
        ),
        migrations.AlterModelOptions(
            name='submission',
            options={'ordering': ['mapping', '-date']},
        ),
    ]
