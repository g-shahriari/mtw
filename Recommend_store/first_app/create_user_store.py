import psycopg2
import sys
from data_analysis import SimilarityUserStores
from database_query import DataBaseQuery
import utm

class UserStoreTable():
    def __init__(self, user_id, first_category):
        self.user_id = user_id
        self.first_category = first_category





    db = psycopg2.connect(host="127.0.0.1",    # your host, usually localhost
                         user="postgres",         # your username
                         password="goshtasb",  # your password
                         database="thesis")        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()


    def calculate_weight_for_each_category(self):
        database_query=DataBaseQuery()
        user_id=self.user_id
        category=self.first_category
        count_all_searches= database_query.user_all_searches(user_id)
        each_category_searches=database_query.user_search_in_a_category(user_id,category)
        weight= each_category_searches / count_all_searches
        weight=round(weight,4)
        conn=self.db
        cur= self.cur
        cur.execute("INSERT INTO public.category_weight(user_id, category, weight) VALUES (%s, %s, %s)" %(user_id,category,weight))
        conn.commit()

    def create_user_store_similarity_table(self):
        database_query=DataBaseQuery()
        user_id=self.user_id
        category=self.first_category
        conn=self.db
        cur =self.cur
        similarity=SimilarityUserStores(user_id,category)
        # weight=self.calculate_weight_for_each_category()
        normalized_user= similarity.normalized_user_feature_space()
        sim=similarity.calcullate_euc_distance_between_user_store_based_first_category(normalized_user)
        store_id=[row[0] for row in sim ]

        similarity_dist=[row[1] for row in sim]
        # sim_multiple_weight= [round(i*weight,4) for i in similarity_dist]
        for i,j in zip(store_id,similarity_dist):
            store_coordinates_lat= database_query.get_coordinates_lat_based_store_id(i)
            store_coordinates_long=database_query.get_coordinates_long_based_store_id(i)
            store_coordinate_utm= utm.from_latlon(store_coordinates_lat,store_coordinates_long)
            store_coordinate_x = store_coordinate_utm[0]
            store_coordinate_y=store_coordinate_utm[1]

            cur.execute('INSERT INTO public.user_store(user_id, "search_category", store_id, store_coordinate_x,store_coordinate_y,similarity) VALUES (%s, %s, %s, %s, %s, %s)' %(user_id,category,i,store_coordinate_x,store_coordinate_y,j))

            conn.commit()




# for i in range(1,2):
    # for j in range(2,3):
    # x= UserStoreTable(i,11)
    # x.create_user_store_similarity_table()
