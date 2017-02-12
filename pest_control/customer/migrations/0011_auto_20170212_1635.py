# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_contract_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='tax_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contract',
            name='tax_percentage',
            field=models.IntegerField(default=15),
        ),
    ]