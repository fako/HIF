# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 11:32
from __future__ import unicode_literals

import core.utils.configuration
from django.db import migrations, models
import django.db.models.deletion
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('online_discourse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadabilityClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(db_index=True, default=None, max_length=255)),
                ('config', core.utils.configuration.ConfigurationField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('purge_at', models.DateTimeField(blank=True, null=True)),
                ('retainer_id', models.PositiveIntegerField(null=True)),
                ('data_hash', models.CharField(db_index=True, default='', max_length=255)),
                ('request', json_field.fields.JSONField(default=None, help_text='Enter a valid JSON object')),
                ('head', json_field.fields.JSONField(default='{}', help_text='Enter a valid JSON object')),
                ('body', models.TextField(blank=True, default=None, null=True)),
                ('status', models.PositiveIntegerField(default=0)),
                ('retainer_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
