# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-14 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nautilus', '0004_auto_20190402_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locaforalogin',
            name='data_hash',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='locaforaorders',
            name='data_hash',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255),
        ),
    ]
