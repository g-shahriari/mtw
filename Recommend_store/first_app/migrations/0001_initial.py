# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-07-03 22:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllShoppingFromTaleqaniToFatemi',
            fields=[
                ('gid', models.AutoField(primary_key=True, serialize=False)),
                ('long', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('type', models.CharField(blank=True, max_length=254, null=True)),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('geom', models.TextField(blank=True, null=True)),
                ('first_category', models.BigIntegerField(blank=True, null=True)),
                ('second_category', models.IntegerField(blank=True, null=True)),
                ('third_category', models.IntegerField(blank=True, null=True)),
                ('product_code', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'all_shopping_from_taleqani_to__fatemi',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NumericUserSearch',
            fields=[
                ('user_id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('user_search_id', models.IntegerField()),
                ('numeric_first_category', models.IntegerField(blank=True, db_index=True, null=True)),
                ('numeric_second_category', models.IntegerField(blank=True, null=True)),
                ('numeric_third_category', models.IntegerField(blank=True, null=True)),
                ('price', models.CharField(blank=True, max_length=50, null=True)),
                ('product_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'numeric_user_search',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StoreProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('first_category', models.IntegerField(blank=True, db_index=True, null=True)),
                ('second_category', models.IntegerField(blank=True, null=True)),
                ('third_category', models.IntegerField(blank=True, null=True)),
                ('product_code', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'store_products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('Gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('Address', models.CharField(max_length=264)),
                ('Image', models.ImageField(blank=True, upload_to='profile_image')),
                ('History', models.ImageField(blank=True, upload_to='uploads')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Search_cost_geo', models.DecimalField(blank=True, decimal_places=4, max_digits=9)),
                ('Search_cost_sim', models.DecimalField(blank=True, decimal_places=4, max_digits=9)),
                ('Best_decision_geo', models.DecimalField(blank=True, decimal_places=4, max_digits=9)),
                ('Best_decision_sim', models.DecimalField(blank=True, decimal_places=4, max_digits=9)),
                ('Accuracy', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_type', models.CharField(max_length=128)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('address', models.CharField(max_length=264)),
                ('goods', models.FileField(upload_to=b'')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Age', models.IntegerField()),
                ('Gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('Profession', models.TextField(blank=True, default='', max_length=20)),
                ('Email', models.EmailField(max_length=200, unique=True)),
                ('Salary', models.DecimalField(blank=True, decimal_places=4, max_digits=9)),
                ('User_longtitude_Coordinates', models.DecimalField(decimal_places=6, max_digits=10)),
                ('User_latitude_Coordinates', models.DecimalField(decimal_places=6, max_digits=10)),
                ('website', models.URLField(blank=True, default='')),
                ('phone', models.TextField(blank=True, default='', max_length=20)),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
