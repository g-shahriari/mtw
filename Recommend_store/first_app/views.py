# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

import unicodedata
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render
from models import Store, NumericUserSearch, StoreProduct, AllShoppingFromTaleqaniToFatemi
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponse
import numpy as np
import pandas as pd
from scipy.spatial import distance
from urllib2 import Request as url_request
from urllib2 import urlopen
import json
import math
import time
from operator import itemgetter
import re
from first_app.signin_form import CustomerForm,SellerForm,UserForm,PollForm
from data_analysis import SimilarityUserStores,GeoDistanceUSerStores,Similarity_based_search_by_search
from database_query import DataBaseQuery
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.





class AboutView(TemplateView):
    template_name = 'about.html'


class BaseView(TemplateView):
    template_name = 'base.html'

class CreateNewCustomer(TemplateView):
    template_name='createnewcustomer.html'

class CreateNewSeller(TemplateView):
    template_name='createnewseller.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

longtitude=0

def lat_ajax(request):
        global longitude

        return HttpResponse(longitude)

@login_required
def qet_queryset(request, num):
    user_id = request.user.id
    first_category = int(num)
    user_coordinates = "51.4042800000" + ',' + "35.7014014000"

    longitude = request.GET.get('longtitude')
    store_id_code=request.GET.get('store_id')

    #create instance from data_analysis classes
    similarity_user_store_analysis=SimilarityUserStores(user_id,first_category)
    geographic_distance_user_stores=GeoDistanceUSerStores(user_id=user_id,first_category=first_category)

    # this func: normalized user feature space for example: user_feature_space=[1,0,2,0] => all item between 0,1 => [0.2***,0,.5***,0]
    normalized_user = similarity_user_store_analysis.normalized_user_feature_space()

    # this func: calculate euclidean distances between normalized user feature space and all noramlized store(with this first category) feature space
    df_list = similarity_user_store_analysis.calcullate_euc_distance_between_user_store_based_first_category(normalize_user=normalized_user)

    sort_geographic_distance=geographic_distance_user_stores.sorted_geographic_distance()

    store_code= [x[0] for x in sort_geographic_distance]
    store_distance=[x[1] for x in sort_geographic_distance]
    store_coordinates_longtitude=[x[2] for x in sort_geographic_distance]
    store_coordinates_latitude=[x[3] for x in sort_geographic_distance]
    store_code_and_distance = zip(store_code, store_distance)
    store_coordinates=zip(store_coordinates_latitude,store_coordinates_longtitude)
    user_coordinates_longtitude=[x[4] for x in sort_geographic_distance]
    user_coordinates_latitude=[x[5] for x in sort_geographic_distance]
    user_coordinates=zip(user_coordinates_latitude,user_coordinates_longtitude)
    return render(request, 'test.html', context={'store_code_distance':store_code_and_distance,'store_coordinates': store_coordinates,'user_coordinates':user_coordinates,'similarity_dist':df_list})

@login_required
def similarity_list_based_search_by_search_check(request,num):
    user_id=request.user.id
    first_category=int(num)
    similarity_based_search_by_search_check=Similarity_based_search_by_search(user_id=user_id,first_category=first_category)
    geographic_distance_user_stores=GeoDistanceUSerStores(user_id=user_id,first_category=first_category)
    similarity_result= similarity_based_search_by_search_check.similarity()
    sort_geographic_distance=geographic_distance_user_stores.sorted_geographic_distance()
    store_code= [x[0] for x in sort_geographic_distance]
    store_distance=[x[1] for x in sort_geographic_distance]
    store_coordinates_longtitude=[x[2] for x in sort_geographic_distance]
    store_coordinates_latitude=[x[3] for x in sort_geographic_distance]
    store_code_and_distance = zip(store_code, store_distance)
    store_coordinates=zip(store_coordinates_latitude,store_coordinates_longtitude)
    user_coordinates_longtitude=[x[4] for x in sort_geographic_distance]
    user_coordinates_latitude=[x[5] for x in sort_geographic_distance]
    user_coordinates=zip(user_coordinates_latitude,user_coordinates_longtitude)
    store_id= [similarity_result.iloc[row,0] for row in similarity_result]
    longtitude= [similarity_result.iloc[row,1] for row in similarity_result]
    latitude= [similarity_result.iloc[row,2] for row in similarity_result]
    sim_percentage= [similarity_result.iloc[row,6] for row in similarity_result]
    number_of_matches_goods_user_by_store= [similarity_result.iloc[row,4] for row in similarity_result]
    number_of_user_searches= [similarity_result.iloc[row,5] for row in similarity_result]
    name= [similarity_result.iloc[row,3] for row in similarity_result]
    store_feature=zip(store_id,sim_percentage,number_of_matches_goods_user_by_store,number_of_user_searches)
    return render(request, 'sim_search_by_search.html',context={'store_code_distance':store_code_and_distance,'store_coordinates': store_coordinates,'user_coordinates':user_coordinates,'store_feature':store_feature})




def customer_register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        customer_form = CustomerForm(request.POST,request.FILES)
        # Check to see both forms are valid
        if user_form.is_valid() and customer_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # # Hash the password
            user.set_password(user.password)
            #
            # # Update with Hashed password
            user.save()
            #
            # # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            profile = customer_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user
            if 'History' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.History = request.FILES['History']

            # Now save model
            profile.save()

            # Check if they provided a profile picture

            # Registration Successful!
            registered = True
            return render(request,'blog/base.html')
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,customer_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        customer_form = CustomerForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'blog/createnewcustomer.html',
                          {'user_form':user_form,
                           'customer_form':customer_form,
                           'registered':registered})


def seller_register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        seller_form = SellerForm(request.POST,request.FILES)

        # Check to see both forms are valid
        if user_form.is_valid() and seller_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # # Hash the password
            user.set_password(user.password)
            #
            # # Update with Hashed password
            user.save()
            #
            # # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = seller_form.save(commit=False)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user
            if 'goods' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.goods = request.FILES['goods']

            # Now save model
            profile.save()

            # Check if they provided a profile picture

            # Registration Successful!
            registered = True
            return render(request,'blog/base.html')
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,seller_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        seller_form = SellerForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'blog/createnewseller.html',
                          {'user_form':user_form,
                           'seller_form':seller_form,
                           'registered':registered})



@login_required
def poll(request):
    form = PollForm()


    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return render(request,'blog/about.html')

        else:
            print("ERROR!")

    return render(request,'blog/poll.html',{'form':form})


def show_store_products(request,pk):
    def get_queryset(self):
        pk=self.pk


# @login_required
# def get_queryset(request):
#     user_id = request.user.id
#     first=request.get_full_path()
#     dict_list={}
#     distinct_first_category_for_user = list(NumericUserSearch.objects.filter(user_id=user_id).values_list(
#         'numeric_first_category').distinct('numeric_first_category').order_by('numeric_first_category'))
#     for item in distinct_first_category_for_user:
    # first_category = int(item[0])
    # create_first_category_zero_for_list= NumericUserSearch.objects.filter(numeric_first_category=first_category).distinct('numeric_second_category').count()
    # distinct_second_category_for_user_base_first_category = list(NumericUserSearch.objects.filter(user_id=user_id, numeric_first_category=first_category).values_list(
    #     'numeric_second_category').distinct('numeric_second_category').order_by('numeric_second_category'))
    # lst = [0]*create_first_category_zero_for_list
    # for second_cat in distinct_second_category_for_user_base_first_category:
    #
    #     count_each_second_category_for_each_first_category_based_user= NumericUserSearch.objects.filter(user_id=user_id,numeric_first_category=first_category,numeric_second_category=second_cat[0]).values_list('numeric_second_category').count()
    #
    #     lst[second_cat[0]-1]= count_each_second_category_for_each_first_category_based_user
#
#
#
#         if first_category==1:
#             dict_list['cat_1']=lst
#         if first_category==2:
#             dict_list['cat_2']=lst
#         if first_category==3:
#             dict_list['cat_3']=lst
#         if first_category==4:
#             dict_list['cat_4']=lst
#         if first_category==5:
#             dict_list['cat_5']=lst
#         if first_category==6:
#             dict_list['cat_6']=lst
#         if first_category==7:
#             dict_list['cat_7']=lst
#         if first_category==8:
#             dict_list['cat_8']=lst
#         if first_category==9:
#             dict_list['cat_9']=lst
#         if first_category==10:
#             dict_list['cat_10']=lst
#         if first_category==11:
#             dict_list['cat_11']=lst
#         if first_category==12:
#             dict_list['cat_12']=lst
#     return render(request, 'test.html', context=dict_list)


def my_custom_sql(self):
    user_id = 2
    category_type = 2
    with connection.cursor() as cursor:
        cursor.execute("SELECT  numeric_second_category,count (numeric_second_category) FROM public.numeric_user_search where user_id=1 and numeric_first_category=12 group by numeric_second_category")

        row = cursor.fetchone()

    return row
