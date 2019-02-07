# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-02 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('open_data', '0003_officialannouncementsdocumentnetherlands_officialannouncementsnetherlands'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialannouncementsdocumentnetherlands',
            name='retainer_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='officialannouncementsdocumentnetherlands',
            name='retainer_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='officialannouncementsnetherlands',
            name='retainer_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='officialannouncementsnetherlands',
            name='retainer_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
