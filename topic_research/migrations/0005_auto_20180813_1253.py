# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-13 12:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topic_research', '0004_auto_20171119_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crosscombinetermsearchcommunity',
            name='current_growth',
        ),
        migrations.RemoveField(
            model_name='crosscombinetermsearchcommunity',
            name='kernel_type',
        ),
        migrations.DeleteModel(
            name='CrossCombineTermSearchCommunity',
        ),
    ]