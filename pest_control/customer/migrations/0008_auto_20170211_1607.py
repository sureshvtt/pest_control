# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-11 16:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_customer_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enquiry',
            options={'ordering': ['-enquiry_date']},
        ),
    ]
