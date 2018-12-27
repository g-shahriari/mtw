# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import psycopg2
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    Age=models.IntegerField()

    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Profession=models.TextField(max_length=20,default='',blank=True)
    Email=models.EmailField(max_length=200,unique=True)
    Salary=models.DecimalField(max_digits=9, decimal_places=4,blank=True)
    User_longtitude_Coordinates=models.DecimalField(max_digits=10, decimal_places=6)
    User_latitude_Coordinates=models.DecimalField(max_digits=10, decimal_places=6)
    website = models.URLField(default='',blank=True)
    phone = models.TextField(max_length=20,default='',blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)

    class Meta:
        managed = True


    def __str__(self):
        return self.user.username





class Store(models.Model):
    store_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    address = models.TextField()


class NumericUserSearch(models.Model):
    user_id = models.IntegerField(primary_key=True, db_index=True)
    user_search_id = models.IntegerField()
    numeric_first_category = models.IntegerField(
        blank=True, null=True, db_index=True)
    numeric_second_category = models.IntegerField(blank=True, null=True)
    numeric_third_category = models.IntegerField(blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'numeric_user_search'
        unique_together = (('user_id', 'user_search_id'),)


class StoreProduct(models.Model):
    store_id = models.IntegerField(blank=True, null=True, db_index=True)
    first_category = models.IntegerField(blank=True, null=True, db_index=True)
    second_category = models.IntegerField(blank=True, null=True)
    third_category = models.IntegerField(blank=True, null=True)
    product_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_products'

class AllShoppingFromTaleqaniToFatemi(models.Model):
    gid = models.AutoField(primary_key=True)
    long = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    type = models.CharField(max_length=254, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    first_category = models.BigIntegerField(blank=True, null=True)
    second_category = models.IntegerField(blank=True, null=True)
    third_category = models.IntegerField(blank=True, null=True)
    product_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'all_shopping_from_taleqani_to__fatemi'
