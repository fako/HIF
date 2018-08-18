# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-18 18:54
from __future__ import unicode_literals

import core.utils.configuration
from django.db import migrations, models
import django.db.models.deletion
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('open_data', '0002_auto_20170320_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialAnnouncementsDocumentNetherlands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(db_index=True, default=None, max_length=255)),
                ('status', models.PositiveIntegerField(default=0)),
                ('config', core.utils.configuration.ConfigurationField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('purge_at', models.DateTimeField(blank=True, null=True)),
                ('retainer_id', models.PositiveIntegerField(null=True)),
                ('data_hash', models.CharField(db_index=True, default='', max_length=255)),
                ('request', json_field.fields.JSONField(default=None, help_text='Enter a valid JSON object')),
                ('head', json_field.fields.JSONField(default='{}', help_text='Enter a valid JSON object')),
                ('body', models.TextField(blank=True, default=None, null=True)),
                ('retainer_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Official announcements document (Dutch)',
                'verbose_name_plural': 'Official announcements document (Dutch)',
            },
        ),
        migrations.CreateModel(
            name='OfficialAnnouncementsNetherlands',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(db_index=True, default=None, max_length=255)),
                ('status', models.PositiveIntegerField(default=0)),
                ('config', core.utils.configuration.ConfigurationField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('purge_at', models.DateTimeField(blank=True, null=True)),
                ('retainer_id', models.PositiveIntegerField(null=True)),
                ('data_hash', models.CharField(db_index=True, default='', max_length=255)),
                ('request', json_field.fields.JSONField(default=None, help_text='Enter a valid JSON object')),
                ('head', json_field.fields.JSONField(default='{}', help_text='Enter a valid JSON object')),
                ('body', models.TextField(blank=True, default=None, null=True)),
                ('retainer_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Official announcements (Dutch)',
                'verbose_name_plural': 'Official announcements (Dutch)',
            },
        ),
    ]
