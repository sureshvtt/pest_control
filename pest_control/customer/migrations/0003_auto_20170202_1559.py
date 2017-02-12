# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20170126_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='pincode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='landline',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
