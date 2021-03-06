# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_contractinvoice_customercontractfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractinvoice',
            name='cheque_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contractinvoice',
            name='cheque_no',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contractinvoice',
            name='paid_bank',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contractinvoice',
            name='ref_no',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contractinvoice',
            name='remarks',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contractinvoice',
            name='transfer_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contractinvoice',
            name='status',
            field=models.CharField(choices=[('p', 'Pending'), ('b', 'Billed'), ('snp', 'Service Not Provided')], default='p', max_length=3),
        ),
    ]
