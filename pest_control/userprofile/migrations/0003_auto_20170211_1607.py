# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20170126_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
