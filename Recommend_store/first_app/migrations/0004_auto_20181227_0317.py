# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-26 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_auto_20181227_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='Profession',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Salary',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=9),
        ),
    ]
