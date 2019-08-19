# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-02 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('future_fashion', '0010_auto_20181202_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothingdatacommunity',
            name='views',
        ),
        migrations.RemoveField(
            model_name='clothinginventorycommunity',
            name='views',
        ),
        migrations.AlterField(
            model_name='clothingdatacommunity',
            name='state',
            field=models.CharField(choices=[('Aborted', 'Aborted'), ('Asynchronous', 'Asynchronous'), ('New', 'New'), ('Ready', 'Ready'), ('Retry', 'Retry'), ('Synchronous', 'Synchronous')], default='New', max_length=255),
        ),
        migrations.AlterField(
            model_name='clothinginventorycommunity',
            name='state',
            field=models.CharField(choices=[('Aborted', 'Aborted'), ('Asynchronous', 'Asynchronous'), ('New', 'New'), ('Ready', 'Ready'), ('Retry', 'Retry'), ('Synchronous', 'Synchronous')], default='New', max_length=255),
        ),
    ]