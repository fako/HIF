# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-02 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20190131_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communitymock',
            name='views',
        ),
        migrations.AlterField(
            model_name='communitymock',
            name='state',
            field=models.CharField(choices=[('Aborted', 'Aborted'), ('Asynchronous', 'Asynchronous'), ('New', 'New'), ('Ready', 'Ready'), ('Retry', 'Retry'), ('Synchronous', 'Synchronous')], default='New', max_length=255),
        ),
    ]
