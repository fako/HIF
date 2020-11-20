# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-20 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup_utrecht', '0007_alter_data_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redditscrapecommunity',
            name='current_growth',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Growth'),
        ),
        migrations.AlterField(
            model_name='redditscrapecommunity',
            name='kernel_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='uniformimagescommunity',
            name='current_growth',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Growth'),
        ),
        migrations.AlterField(
            model_name='uniformimagescommunity',
            name='kernel_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType'),
        ),
    ]
