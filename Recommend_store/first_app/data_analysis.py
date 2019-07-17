# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from database_query import DataBaseQuery
from ant_colony import AntColony
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
from sklearn import preprocessing
from pandas import DataFrame


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
                math.sqrt(2)) - (euc_distance_user_and_store)
            euc_distance_user_and_store = euc_distance_user_and_store / \
                math.sqrt(2)
            euc_distance_user_and_store = euc_distance_user_and_store * 100
            if 30<euc_distance_user_and_store<=40:
                euc_distance_user_and_store=euc_distance_user_and_store*2
            elif euc_distance_user_and_store<=30:
                euc_distance_user_and_store=euc_distance_user_and_store*2.5
            euc_distance_user_and_store = round(
                euc_distance_user_and_store, ndigits=2)
            df_store_id_and_euc_dist_user_store.loc[store_i,
                                                    'b'] = euc_distance_user_and_store
            sorted_dataframe = df_store_id_and_euc_dist_user_store.sort_values([
                                                                               'b'], ascending=False)
        df_list = list()
        df_tuple = tuple()
        for i, j in zip(sorted_dataframe.ix[:, 'a'], (sorted_dataframe.ix[:, 'b'])):
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
        if distance.euclidean(lst_user,0)==0:
            normalized_user=0
        else:
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




class AreaDetermine():

    def __init__(self, user_id):
        self.user_id = user_id

    database_query= DataBaseQuery()

    def get_store_id_coordinates_similarity(self,first_category):
        database_query=self.database_query
        user_id =self.user_id
        stores= database_query.get_stores_id_coordinates_similarity(user_id,first_category)
        return stores

    def create_category_layer(self,first_category):
        import numpy as np
        from scipy.spatial import distance_matrix
        g_x= np.arange(535000,537000,20)
        g_y=np.arange(3951000,3954000,20)

        grid_x,grid_y=np.meshgrid(g_x,g_y)

        points=[]
        x=list()
        y=list()
        values=[]
        for items in self.get_store_id_coordinates_similarity(first_category):
            x.append(items[1])
            y.append(items[2])
            points.append([items[1],items[2]])

            values.append([items[3],])
        values=np.asarray(values)
        points=np.asarray(points)

        def simple_idw(x, y,radius,values):
            dist = distance_matrix(x, y)

    # In IDW, weights are 1 / distance
            len(dist)
            upper=0
            down=0
            for i in range(len(dist)):
                upper += values[i]/((dist[i])**2)
                down += 1.0/((dist[i])**2)

    # # Make weights sum to one
    # weights /= weights.sum(axis=0)

    # Multiply the weights for each interpolated point by all observed Z-values
            if down!=0:
                zi = upper/down
            else:
                zi=0
            return zi

        idw_interpolation=list()
        for i in g_x:
            for j in g_y:
                idw_interpolation.append(simple_idw(points,[[i,j]],500,values))

        cluster_factor= (float(max(idw_interpolation)))/20
        max_c=float(max(idw_interpolation))
        idw=list()
        for i in range(0,len(idw_interpolation)):
            if (max_c-cluster_factor*1)<idw_interpolation[i]<max_c:
                idw.append(1)
            elif (max_c-cluster_factor*2)<idw_interpolation[i]<(max_c-cluster_factor*1):
                idw.append(2)
            elif (max_c-cluster_factor*3)<idw_interpolation[i]<(max_c-cluster_factor*2):
                idw.append(3)
            elif (max_c-cluster_factor*4)<idw_interpolation[i]<(max_c-cluster_factor*3):
                idw.append(4)
            elif (max_c-cluster_factor*5)<idw_interpolation[i]<(max_c-cluster_factor*4):
                idw.append(5)


        # idw_value= np.reshape(idw_interpolation,(100,150)).T
        # from matplotlib import cm
        # import matplotlib.pyplot as plt
        # # # from scipy.interpolate import LinearNDInterpolator
        # # # from sklearn.ensemble import RandomForestRegressor
        # # # regressor = RandomForestRegressor(n_estimators=10,random_state=0)
        # # # regressor.fit(points,values.ravel())
        # # # reg_value=list()
        # # # for i in g_x:
        # # #     for j in g_y:
        # # #         reg_value.append(regressor.predict([[i,j]]))
        # # # re_value= np.reshape(reg_value,(100,150)).T
        # #
        # #
        # #
        # plt.pcolor(grid_x, grid_y,idw_value , cmap=cm.jet)
        # plt.colorbar()
        # plt.scatter(x, y, color='black', cmap=cm.jet)
        # plt.show()
        # # # plt.subplot(222)
        # # # plt.scatter(x, y,100, values, cmap=cm.jet)
        # # # plt.colorbar()
        # # plt.show()
        # # #
        #
        # myInterpolator = LinearNDInterpolator(points, values,fill_value=0)
        # inter_value=list()
        # for i in g_x:
        #     for j in g_y:
        #         inter_value.append(myInterpolator(i,j))
        # in_value= np.reshape(inter_value,(100,150)).T
        #
        #
        # plt.subplot(222)
        #
        # plt.pcolor(grid_x, grid_y, in_value, cmap=cm.jet)
        # plt.colorbar()
        # plt.scatter(x, y, color='black', cmap=cm.jet)
        #
        # # plt.subplot(222)
        # # plt.scatter(x, y, 100, values, cmap=cm.jet)
        # # plt.colorbar()
        # plt.show()
        # plt.savefig('linear.png')

        return idw
    def overlay_all_layer(self):
        import numpy as np
        x=list()
        y=list()
        values=list()
        for items in self.get_store_id_coordinates_similarity(2):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])

        for items in self.get_store_id_coordinates_similarity(3):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])
        for items in self.get_store_id_coordinates_similarity(4):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])
        for items in self.get_store_id_coordinates_similarity(5):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])

        for items in self.get_store_id_coordinates_similarity(6):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])

        for items in self.get_store_id_coordinates_similarity(7):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])
        for items in self.get_store_id_coordinates_similarity(8):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])
        for items in self.get_store_id_coordinates_similarity(9):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])

        for items in self.get_store_id_coordinates_similarity(10):
            x.append(items[1])
            y.append(items[2])
            values.append(items[3])
            x1=list()
            y1=list()
        for items in self.get_store_id_coordinates_similarity(12):

            x1.append(items[1])
            y1.append(items[2])
            values.append(items[3])
        g_x= np.arange(535000,537000,20)
        g_y=np.arange(3951000,3954000,20)
        grid_x,grid_y=np.meshgrid(g_x,g_y)
        user_id=self.user_id
        database_query=self.database_query
        layer_1=self.create_category_layer(1)
        layer_2=self.create_category_layer(2)
        layer_3=self.create_category_layer(3)
        layer_4=self.create_category_layer(4)
        layer_5=self.create_category_layer(5)
        layer_6=self.create_category_layer(6)
        layer_7=self.create_category_layer(7)
        layer_8=self.create_category_layer(8)
        layer_9=self.create_category_layer(9)
        layer_10=self.create_category_layer(10)
        # # layer_11=self.create_category_layer(11)
        layer_12=self.create_category_layer(12)
        items= database_query.get_weights(user_id)
        layer_1=layer_1*items[0]
        layer_2=layer_2*items[1]
        layer_3=layer_3*items[2]
        layer_4=layer_4*items[3]
        layer_5=layer_5*items[4]
        layer_6=layer_6*items[5]
        layer_7=layer_7*items[6]
        layer_8=layer_8*items[7]
        layer_9=layer_9*items[8]
        layer_10=layer_10*items[9]
        layer_12=layer_12*items[11]
        combine_layer= layer_1+layer_2+layer_3+layer_4+layer_5+layer_6+layer_7+layer_8+layer_9+layer_10+layer_12

        from matplotlib import cm
        import matplotlib.pyplot as plt

        plt.pcolor(grid_x, grid_y, combine_layer, cmap=cm.jet)
        plt.colorbar()
        plt.scatter(x1, y1,color='blue', cmap=cm.jet)
        plt.show()

    def extract_stores_from_database(self):
        database_query=self.database_query
        user_id=self.user_id


        best_store_based_sorted=database_query.sorted_100_stores_in_all_category(user_id)
        return best_store_based_sorted





class Similarity_based_search_by_search():

    data_query = DataBaseQuery()
    def __init__(self,user_id,first_category):
        self.user_id=user_id
        self.first_category=first_category


    def user_searches(self):
        data_query=self.data_query
        user_id=self.user_id
        first_category=self.first_category
        user_search= data_query.user_searches(user_id=user_id,first_category=first_category)
        output=DataFrame.from_records(user_search)
        return output

    def store_features(self):
        data_query=self.data_query
        first_category=self.first_category
        store_feature_name_lat_long_id= data_query.store_features(first_category=first_category)
        output =DataFrame.from_records(store_feature_name_lat_long_id)
        return output


    def store_available_goods(self,store_id):
        data_query=self.data_query
        first_category=self.first_category
        store_available_good=data_query.store_available_goods(first_category=first_category,store_id=store_id)
        output=DataFrame.from_records(store_available_good)
        return output

    def similarity(self):
        user_search=self.user_searches()
        output=[]
        count_user_search=len(user_search[1])

        store_feature=self.store_features()

        for row in range(0,len(store_feature)):

            store_goods=self.store_available_goods(store_id=store_feature.iloc[row,0])
            match_goods_list=[]
            for i in range(0,count_user_search):

                for j in range(0,len(store_goods)):

                    if user_search.iloc[i,2]==store_goods.iloc[j,1] and user_search.iloc[i,3]==store_goods.iloc[j,2] and user_search.iloc[i,4]==store_goods.iloc[j,3] and user_search.iloc[i,5]==store_goods.iloc[j,4] and user_search.iloc[i,6]==store_goods.iloc[j,5]:
                        match_goods_list.append(user_search.iloc[i,6])

            count_match_goods=len(match_goods_list)
            similarity= (float(count_match_goods)/count_user_search)*100
            similarity= "{0:.2f}".format(similarity)
            output.append([store_feature.iloc[row,0],store_feature.iloc[row,1],store_feature.iloc[row,2],store_feature.iloc[row,3],count_user_search,count_match_goods,similarity])
        out_dataframe=DataFrame.from_records(output)
        out_dataframe=out_dataframe.sort_values(out_dataframe.columns[6],ascending=False)
        return out_dataframe






class AreaBasedAntColony():

        def __init__(self, user_id):
            self.user_id = user_id

        database_query= DataBaseQuery()

        def get_category_and_weights_order_by_weight(self):
            user_id=self.user_id
            database_query=self.database_query
            category_weight=database_query.get_category_and_weight_order_by_weight(user_id)
            return category_weight

        def store_id_for_each_max_category(self,each_category_from_end):
            user_id=self.user_id
            database_query=self.database_query
            max_category=self.get_category_and_weights_order_by_weight()[-each_category_from_end][0]
            stores_id=database_query.get_stores_id_and_coordinate_and_similarity(search_category=max_category,user_id=user_id)
            return stores_id

        def distance_from_max_category(self,category_from_end):
            import numpy as np
            from sklearn.metrics.pairwise import euclidean_distances
            first_max_category=self.store_id_for_each_max_category(each_category_from_end=1)
            first_category_store_location=[[i[1],i[2]] for i in first_max_category]
            second_max_category=self.store_id_for_each_max_category(each_category_from_end=category_from_end)
            second_category_store_location=[[i[1],i[2]] for i in second_max_category]
            second_category_store_code=[i[0] for i in second_max_category]
            second_category_similarity=[i[3] for i in second_max_category]
            x= euclidean_distances(first_category_store_location,second_category_store_location)

            list_of_store_code_coordinates_similarity_separated_by_each_first_max_category=list()
            for i in range(0,np.shape(x)[0]):
                list_of_store_code_coordinates_similarity=list()
                for j in range(0,np.shape(x)[1]):
                    list_of_store_code_coordinates_similarity.append([x[i][j],second_category_store_code[j],second_category_store_location[j][0],second_category_store_location[j][1],second_category_similarity[j]])
                list_of_store_code_coordinates_similarity_separated_by_each_first_max_category.append(list_of_store_code_coordinates_similarity)
            return list_of_store_code_coordinates_similarity_separated_by_each_first_max_category

        def stores_within_disance_buffer(self,buffer,category,row_number):
            import numpy as np
            distance_mat=self.distance_from_max_category(category_from_end=category)
            list_of_store_code_coordinates_similarity_buffer=list()
            for j in range(0,np.shape(distance_mat)[1]):
                if distance_mat[row_number][j][0]<buffer:
                    list_of_store_code_coordinates_similarity_buffer.append(distance_mat[row_number][j][0:5])
            return list_of_store_code_coordinates_similarity_buffer

        def combine_all_category_plus_store_code_position_similarity(self,row_number):
            import numpy as np
            first_category_store_code_position_similarity=list()
            first_category_store_code_position_similarity.append(0)
            first_max_category=list(self.store_id_for_each_max_category(1)[row_number])
            first_category_store_code_position_similarity.append(first_max_category[0])
            first_category_store_code_position_similarity.append(first_max_category[1])
            first_category_store_code_position_similarity.append(first_max_category[2])
            first_category_store_code_position_similarity.append(first_max_category[3])
            second_category_store_code_position_similarity_buffer=self.stores_within_disance_buffer(buffer=500,row_number=row_number,category=2)
            second_category_initial_pheromone=[1]*(np.shape(second_category_store_code_position_similarity_buffer)[0])
            third_category_store_code_position_similarity_buffer=self.stores_within_disance_buffer(buffer=500,row_number=row_number,category=3)
            third_category_initial_pheromone=[1]*(np.shape(third_category_store_code_position_similarity_buffer)[0])
            fourth_category_store_code_position_similarity_buffer=self.stores_within_disance_buffer(buffer=500,row_number=row_number,category=4)
            fourth_category_initial_pheromone=[1]*(np.shape(fourth_category_store_code_position_similarity_buffer)[0])
            combined_pheromone=[1,second_category_initial_pheromone,third_category_initial_pheromone,fourth_category_initial_pheromone]
            combined=[first_category_store_code_position_similarity,second_category_store_code_position_similarity_buffer,third_category_store_code_position_similarity_buffer,fourth_category_store_code_position_similarity_buffer]
            return combined,combined_pheromone

        def ant_colony(self,row_number):
            ant=AntColony()
            points= self.combine_all_category_plus_store_code_position_similarity(row_number)[0]
            pheromone=self.combine_all_category_plus_store_code_position_similarity(row_number)[1]
            x= ant.repeated_ant_colony(number_of_repeat=10,points=points,points_pheromone=pheromone)

            return x

# x= AreaBasedAntColony(1)
# print x.ant_colony(row_number=5
x= SimilarityUserStores(user_id=1,first_category=4)
print x.calcullate_euc_distance_between_user_store_based_first_category(x.normalized_user_feature_space())
# x= AreaBasedAntColony(1)
# y=x.store_id_for_each_max_category(each_category_from_end=1)
# import numpy as np
#
#
# dist_len=np.shape(x.distance_from_max_category(category_from_end=2))[0]
#
#
#
# # print (x.combine_all_category_plus_store_code_position_similarity(1)[0])[1]
# # print np.shape(x.combine_all_category_plus_store_code_position_similarity(0)[2])
# # print x.combine_all_category_plus_store_code_position_similarity(0)[0]
# # for i in range(0,dist_len):
# # e.append([x.stores_within_disance_buffer(buffer=200,row_number=0,category=2),x.stores_within_disance_buffer(buffer=200,row_number=0,category=3),x.stores_within_disance_buffer(buffer=200,row_number=0,category=4)])
# print (x.combine_all_category_plus_store_code_position_similarity(0)[0])[1][1]
#
# print x.ant_colony(row_number=5)
#





# print first_max_category
# print '#################*****************##############'
# print(second_max_category)
# print '#################*****************##############'
# print(third_max_category)
# print '#################*****************##############'
# print(forth_max_category)

# x= AreaBasedAntColony(1)
#
# print x.store_id_for_each_max_category(1)
