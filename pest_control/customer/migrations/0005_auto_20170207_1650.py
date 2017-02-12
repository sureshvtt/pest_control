# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20170202_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquiry',
            name='service_required',
        ),
        migrations.AddField(
            model_name='enquiry',
            name='service_required',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.EnquiryService'),
        ),
    ]