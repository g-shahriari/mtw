# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-27 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0004_auto_20181227_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='Profession',
            field=models.TextField(blank=True, default='', max_length=20),
        ),
    ]
