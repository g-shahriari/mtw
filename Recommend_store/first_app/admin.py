# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from django.contrib import admin
from models import Store,NumericUserSearch,StoreProduct,AllShoppingFromTaleqaniToFatemi,UserProfile
# Register your models here.


admin.site.register(UserProfile)

admin.site.register(Store)
admin.site.register(NumericUserSearch)
admin.site.register(StoreProduct)
admin.site.register(AllShoppingFromTaleqaniToFatemi)
