# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from django.contrib import admin
from models import Store,NumericUserSearch,StoreProduct,AllShoppingFromTaleqaniToFatemi,UserProfile,Customer,Seller,Comments
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Comments)
admin.site.register(Store)
admin.site.register(NumericUserSearch)
admin.site.register(StoreProduct)
admin.site.register(AllShoppingFromTaleqaniToFatemi)
