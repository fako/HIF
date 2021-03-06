# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-21 12:53
from __future__ import unicode_literals

import core.processors.mixins
import datagrowth.configuration.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('wiki_feed', '0001_initial'), ('wiki_feed', '0002_auto_20170201_1741'), ('wiki_feed', '0003_wikifeedpublishcommunity'), ('wiki_feed', '0004_auto_20190402_0928'), ('wiki_feed', '0005_on_delete')]

    initial = True

    dependencies = [
        ('core', '0017_auto_20170315_1639'),
        ('core', '0016_auto_20160627_2118'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikiFeedCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(db_index=True, max_length=255)),
                ('config', datagrowth.configuration.fields.ConfigurationField()),
                ('kernel_id', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('purge_at', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('Aborted', 'Aborted'), ('Asynchronous', 'Asynchronous'), ('New', 'New'), ('Ready', 'Ready'), ('Retry', 'Retry'), ('Synchronous', 'Synchronous')], default='New', max_length=255)),
                ('current_growth', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Growth')),
                ('kernel_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Wiki feed',
                'verbose_name_plural': 'Wiki feeds',
            },
            bases=(models.Model, core.processors.mixins.ProcessorMixin),
        ),
        migrations.CreateModel(
            name='WikiFeedPublishCommunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(db_index=True, max_length=255)),
                ('config', datagrowth.configuration.fields.ConfigurationField()),
                ('kernel_id', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('purge_at', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('Aborted', 'Aborted'), ('Asynchronous', 'Asynchronous'), ('New', 'New'), ('Ready', 'Ready'), ('Retry', 'Retry'), ('Synchronous', 'Synchronous')], default='New', max_length=255)),
                ('current_growth', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Growth')),
                ('kernel_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Wiki feed publication',
                'verbose_name_plural': 'Wiki feed publications',
            },
            bases=(models.Model, core.processors.mixins.ProcessorMixin),
        ),
    ]
