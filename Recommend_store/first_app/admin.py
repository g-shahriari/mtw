# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from django.contrib import admin
from models import Customer,Store,NumericUserSearch,StoreProduct,AllShoppingFromTaleqaniToFatemi
# Register your models here.
admin.site.register(Customer)
admin.site.register(Store)
admin.site.register(NumericUserSearch)
admin.site.register(StoreProduct)
admin.site.register(AllShoppingFromTaleqaniToFatemi)
