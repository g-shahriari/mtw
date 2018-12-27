# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from database_query import DataBaseQuery
import sys
import unicodedata
import numpy as np
import pandas as pd
import json
import math
import time
from operator import itemgetter
import re
from scipy.spatial import distance
from urllib2 import Request as url_request
from urllib2 import urlopen


class SimilarityUserStores():


    def __init__(self, user_id, first_category):
        self.user_id = user_id
        self.first_category = first_category


    def calcullate_euc_distance_between_user_store_based_first_category(self, normalize_user):
        data_query = DataBaseQuery()

        first_category = self.first_category

        create_first_category_zero_for_list = int(
            data_query.create_first_category_zero_for_list_query(first_category))

        get_store_id_based_first_category = data_query. get_store_id_based_first_category(
            first_category)

        get_store_id_based_first_category = map(
            int, get_store_id_based_first_category)

        df_0 = pd.DataFrame()

        for stores in get_store_id_based_first_category:
            lst_store_feaure = [0] * create_first_category_zero_for_list
            df_0.loc[stores, 0] = stores
            for second_cat in range(1, (create_first_category_zero_for_list + 1)):
                count_second_category_type_for_each_store_based_first_category = data_query.count_second_category_type_for_each_store_based_first_category(
                    store_id=stores, first_category=first_category, second_category=second_cat)
                df_0.loc[stores, second_cat] = count_second_category_type_for_each_store_based_first_category

        df_store_id_and_euc_dist_user_store = pd.DataFrame(columns=['a', 'b'])
        for store_i, i in zip(get_store_id_based_first_category, range(0, len(get_store_id_based_first_category))):
            lst_store_feature = []
            df_store_id_and_euc_dist_user_store.loc[store_i, 'a'] = store_i
            for j in range(1, (create_first_category_zero_for_list + 1)):
                lst_store_feature.append(df_0.iat[i, j])
            lst_norm = np.linalg.norm(lst_store_feature)
            normalize_store_feature = lst_store_feature / lst_norm
            euc_distance_user_and_store = distance.euclidean(
                normalize_store_feature, normalize_user)
            euc_distance_user_and_store = (
                math.sqrt(create_first_category_zero_for_list)) - (euc_distance_user_and_store)
            euc_distance_user_and_store = euc_distance_user_and_store / \
                math.sqrt(create_first_category_zero_for_list)
            euc_distance_user_and_store = euc_distance_user_and_store * 100
            euc_distance_user_and_store = round(
                euc_distance_user_and_store, ndigits=2)
            df_store_id_and_euc_dist_user_store.loc[store_i,
                                                    'b'] = euc_distance_user_and_store
            sorted_dataframe = df_store_id_and_euc_dist_user_store.sort_values([
                                                                               'b'], ascending=False)
        df_list = list()
        df_tuple = tuple()
        for i, j in zip(sorted_dataframe.ix[:, 'a'], sorted_dataframe.ix[:, 'b']):
            df_list.append(i)
            df_list.append(j)
        it = iter(df_list)
        df_tuple = zip(it, it)
        # df_list = sorted_dataframe.ix[:, 'a']
        return df_tuple

    def normalized_user_feature_space(self):

        data_query = DataBaseQuery()
        user_id = self.user_id
        first_category = self.first_category
        create_first_category_zero_for_list = int(
            data_query.create_first_category_zero_for_list_query(first_category))

        distinct_second_category_for_user_base_first_categor = data_query. distinct_second_category_for_user_base_first_category(
            first_category, user_id)
        distinct_second_category_for_user_base_first_category = map(
            int, distinct_second_category_for_user_base_first_categor)
        lst_user = [0] * create_first_category_zero_for_list
        for second_cat in distinct_second_category_for_user_base_first_category:
            count_each_second_category_for_each_first_category_based_user = int(data_query.count_each_second_category_for_each_first_category_based_user(
                user_id=user_id, numeric_first_category=first_category, numeric_second_category=second_cat))
            lst_user[second_cat -
                     1] = count_each_second_category_for_each_first_category_based_user
        lst_norm_user = np.linalg.norm(lst_user)
        normalized_user = lst_user / lst_norm_user
        return normalized_user




class GeoDistanceUSerStores():
    data_query = DataBaseQuery()
    def __init__(self,user_id,first_category):
        self.user_id=user_id
        self.first_category=first_category




    def distance_geographic_between_store_and_user(self,start_id_store_id_with_first_category, end_id_store_id_with_first_category):
        data_query=self.data_query
        user_id=self.user_id
        first_category=self.first_category


        get_user_latitude=data_query.user_latitude_Coordinates(user_id=user_id)
        get_user_latitude_str=str(get_user_latitude[0])

        get_user_longtitude=data_query.user_longtitude_Coordinates(user_id=user_id)
        get_user_longtitude_str=str(get_user_longtitude[0])

        # this query: extract stores coordinates that stores have this first category type
        get_store_coordinates=data_query.get_store_coordinates_for_this_first_category(first_category)
        # get_store_coordinates = shopping.objects.filter(
        #     first_category=num).values_list('gid', 'long', 'lat').order_by('gid')


        headers = {
            'Accept': 'application/json; charset=utf-8'
        }

        str_url = str()
        user_coordinates = get_user_longtitude_str+','+get_user_latitude_str
        for i in range(start_id_store_id_with_first_category, end_id_store_id_with_first_category):
            long = str(get_store_coordinates[i][1])
            comma = ','
            lat = str(get_store_coordinates[i][2])
            append_sign_each_point = '%7C'
            str_url += long + comma + lat + append_sign_each_point
        request_distance = url_request('https://api.openrouteservice.org/matrix?api_key=5b3ce3597851110001cf624855704328a35746098c6f6f287a22cd66&profile=driving-car&locations='
                                       + user_coordinates + '%7C' + str_url + '&metrics=distance', headers=headers)
        response_body = json.loads(urlopen(request_distance).read())
        distance_result_with_0 = list(response_body['distances'][0])
        distance_result_remove_dist_between_user_and_user = distance_result_with_0[1:]
        return distance_result_remove_dist_between_user_and_user


    def calculate_distance_between_store_and_user_for_all_stores(self):
        # first_category=self.first_category
        # user_coordinate=self.user_coordinate
        #
        first_category=self.first_category
        data_query=self.data_query
        get_store_id_based_first_category = data_query. get_store_id_based_first_category(
            first_category)

        get_store_id_based_first_category = map(
            int, get_store_id_based_first_category)
        if 0 < len(get_store_id_based_first_category) <= 40:
            dist_between_user_and_stores = self.distance_geographic_between_store_and_user(0,len(get_store_id_based_first_category))

        if 40 < len(get_store_id_based_first_category) < 80:
            dist_between_user_and_stores_part_1 =self.distance_geographic_between_store_and_user(0,40)
            dist_between_user_and_stores_part_2 =self.distance_geographic_between_store_and_user(40, len(get_store_id_based_first_category))
            dist_between_user_and_stores = dist_between_user_and_stores_part_1 + \
                dist_between_user_and_stores_part_2

        if 80 < len(get_store_id_based_first_category) < 120:
            dist_between_user_and_stores_part_1 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=40)
            dist_between_user_and_stores_part_2 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=40, end_id_store_id_with_first_category=80)
            dist_between_user_and_stores_part_3 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=80, end_id_store_id_with_first_category=len(get_store_id_based_first_category))
            dist_between_user_and_stores = dist_between_user_and_stores_part_1 + \
                dist_between_user_and_stores_part_2 + dist_between_user_and_stores_part_3

        if 120 < len(get_store_id_based_first_category) < 160:
            dist_between_user_and_stores_part_1 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=40)
            dist_between_user_and_stores_part_2 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=40, end_id_store_id_with_first_category=80)
            dist_between_user_and_stores_part_3 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=80, end_id_store_id_with_first_category=120)
            dist_between_user_and_stores_part_4 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=120, end_id_store_id_with_first_category=len(get_store_id_based_first_category))
            dist_between_user_and_stores = dist_between_user_and_stores_part_1 + dist_between_user_and_stores_part_2 + \
                dist_between_user_and_stores_part_3 + dist_between_user_and_stores_part_4

        if 160 < len(get_store_id_based_first_category) < 200:
            dist_between_user_and_stores_part_1 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=40)
            dist_between_user_and_stores_part_2 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=40, end_id_store_id_with_first_category=80)
            dist_between_user_and_stores_part_3 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=80, end_id_store_id_with_first_category=120)
            dist_between_user_and_stores_part_4 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=120, end_id_store_id_with_first_category=160)
            dist_between_user_and_stores_part_5 = self.distance_geographic_between_store_and_user(start_id_store_id_with_first_category=160, end_id_store_id_with_first_category=len(get_store_id_based_first_category))
            dist_between_user_and_stores = dist_between_user_and_stores_part_1 + dist_between_user_and_stores_part_2 + \
                dist_between_user_and_stores_part_3 + \
                dist_between_user_and_stores_part_4 + dist_between_user_and_stores_part_5

        return dist_between_user_and_stores


    def sorted_geographic_distance(self):
        user_id=self.user_id
        first_category=self.first_category
        data_query=self.data_query
        get_user_latitude=data_query.user_latitude_Coordinates(user_id=user_id)[0]
        get_user_longtitude=data_query.user_longtitude_Coordinates(user_id=user_id)[0]
        dist_between_user_and_stores=self.calculate_distance_between_store_and_user_for_all_stores()
        get_store_coordinates=data_query.get_store_coordinates_for_this_first_category(first_category)
        query_order_by_gid=data_query.query_order_by_gid(first_category)

        list_with_gid_and_dist=list()
        for i,j,k, in zip(dist_between_user_and_stores, query_order_by_gid,get_store_coordinates):
            list_with_gid_and_dist.append(j)
            list_with_gid_and_dist.append(i)
            list_with_gid_and_dist.append(k[1])
            list_with_gid_and_dist.append(k[2])
            list_with_gid_and_dist.append(get_user_longtitude)
            list_with_gid_and_dist.append(get_user_latitude)

        it = iter(list_with_gid_and_dist)
        tuple_with_gid_and_dist = zip(it, it,it,it,it,it)

        sort_geographic_distance = tuple(sorted(tuple_with_gid_and_dist, key=itemgetter(1)))

        return sort_geographic_distance
