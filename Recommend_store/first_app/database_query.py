import psycopg2
from faker import Faker
import random
class DataBaseQuery():
    db = psycopg2.connect(host="127.0.0.1",    # your host, usually localhost
                         user="postgres",         # your username
                         password="goshtasb",  # your password
                         database="thesis")        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()


    def sorted_100_stores_in_all_category(self,user_id):
        cur=self.cur
        cur.execute('SELECT "Search_category", store_id, similarity_with_category_weight FROM public.user_store where user_id=%s order by similarity_with_category_weight DESC fetch first 100 rows only' %user_id)
        store_id_and_similarity=[]
        for row in cur.fetchall():
            store_id_and_similarity.append(int(row[1]))
            store_id_and_similarity.append(float(row[2]))

        return store_id_and_similarity


    def userprofile(self):
        conn=self.db
        fake =Faker()
        cur =self.cur
        for i in range(1000,1001):
            Age= random.randint(15,65)
            Gender=fake.profile(fields=None,sex=None)['sex']
            Gender="'"+Gender+"'"
            Profession=fake.profile(fields=None,sex=None)['job']
            Profession = "'"+'Teacher'+"'"
            Email=fake.profile(fields=None,sex=None)['mail']
            Email ="'"+Email+"'"
            salary=0
            longtitude=float(random.randrange(5139000,5141300))/100000
            latitude= float(random.randrange(357013,357233))/10000

            Website=fake.profile(fields=None,sex=None)['website'][0]
            Website="'"+Website+"'"

            user_id=i


            cur.execute('INSERT INTO first_app_userprofile("Age", "Gender", "Profession", "Email", "Salary", "User_longtitude_Coordinates", "User_latitude_Coordinates","website",phone,image,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0,0,%s)' %(Age,Gender,Profession,Email,salary,longtitude,latitude,Website,user_id))
            conn.commit()

    # Use all the SQL you like
    def create_first_category_zero_for_list_query(self,first_category):
        cur = self.cur
        cur.execute("SELECT count(distinct(numeric_second_category)) FROM numeric_user_search where numeric_first_category=%s" %first_category)

        # print all the first cell of all the rows
        count_second_category= [row[0] for row in cur.fetchall()][0]
        return count_second_category

    def distinct_second_category_for_user_base_first_category(self,first_category,user_id):
        cur = self.cur
        cur.execute("select distinct(numeric_second_category) from numeric_user_search where user_id=%s and numeric_first_category=%s order by numeric_second_category" %(user_id,first_category))
        count_second_category_for_user= [row[0] for row in cur.fetchall()]
        return count_second_category_for_user

    def get_store_id_based_first_category(self,first_category):
        cur=self.cur
        cur.execute("SELECT distinct(store_id) from store_products where first_category=%s" %first_category)
        store_id_for_this_first_category= [row[0] for row in cur.fetchall()]
        return store_id_for_this_first_category

    def get_store_coordinates_for_this_first_category(self,first_category):
        cur=self.cur
        cur.execute("SELECT gid,long,lat from all_shopping_from_taleqani_to__fatemi where first_category=%s order by gid" %first_category)
        store_coordinates_for_store_by_this_first_category= [row for row in cur.fetchall()]
        return store_coordinates_for_store_by_this_first_category

    def query_order_by_gid(self,first_category):
        cur=self.cur
        cur.execute("SELECT gid from all_shopping_from_taleqani_to__fatemi where first_category=%s order by gid" %first_category)
        store_id_ordered= [row[0] for row in cur.fetchall()]
        return store_id_ordered

    def count_second_category_type_for_each_store_based_first_category(self,store_id,first_category,second_category):
        cur=self.cur
        cur.execute("SELECT count(second_category) from store_products where store_id=%s and first_category=%s and second_category=%s" %(store_id,first_category,second_category))
        second_category_count=[row[0] for row in cur.fetchall()][0]
        return second_category_count

    def count_each_second_category_for_each_first_category_based_user(self,user_id, numeric_first_category, numeric_second_category):
        cur=self.cur
        cur.execute("SELECT count(numeric_second_category) from numeric_user_search where user_id=%s and numeric_first_category=%s and numeric_second_category=%s" %(user_id, numeric_first_category, numeric_second_category))
        second_category_count=[row[0] for row in cur.fetchall()][0]
        return second_category_count


    def get_store_name_order_by_gid(self,first_category):
        cur=self.cur
        cur.execute('SELECT  gid,name FROM public.all_shopping_from_taleqani_to__fatemi where first_category=%s order by gid' %first_category)
        get_store_name_order_by_gid=[row[0] for row in cur.fetchall()]
        return get_store_name_order_by_gid

    def user_latitude_Coordinates(self,user_id):
        cur=self.cur
        cur.execute('SELECT "User_latitude_Coordinates" from first_app_userprofile where user_id=%s' %user_id)
        latitude=[row[0] for row in cur.fetchall()]
        return latitude


    def user_longtitude_Coordinates(self,user_id):
        cur=self.cur
        cur.execute('SELECT "User_longtitude_Coordinates" from first_app_userprofile where user_id=%s' %user_id)
        longtitude=[row[0] for row in cur.fetchall()]
        return longtitude

    def user_all_searches(self,user_id):
        cur=self.cur
        cur.execute('SELECT count(numeric_first_category) FROM public.numeric_user_search where user_id=%s' %user_id)
        count__searches=float(cur.fetchone()[0])
        return count__searches


    def user_search_in_a_category(self,user_id,category):
        cur=self.cur
        cur.execute('SELECT count(numeric_first_category) FROM public.numeric_user_search where user_id=%s and numeric_first_category=%s' %(user_id,category))
        count_each_category_search= float(cur.fetchone()[0])

        return count_each_category_search

    def get_coordinates_lat_based_store_id(self,store_id):
        cur= self.cur
        cur.execute("SELECT  lat FROM public.all_shopping_from_taleqani_to__fatemi where gid=%s" %store_id)
        store_id_lat= float(cur.fetchone()[0])
        return store_id_lat

    def get_coordinates_long_based_store_id(self,store_id):
        cur= self.cur
        cur.execute('SELECT  "long" FROM public.all_shopping_from_taleqani_to__fatemi where gid=%s' %store_id)
        store_id_long= float(cur.fetchone()[0])
        return store_id_long


    def get_stores_id_coordinates_similarity(self,user_id,search_category):
        cur = self.cur
        cur.execute('SELECT  store_id, store_coordinate_x, store_coordinate_y, similarity FROM public.user_store where user_id=%s and search_category=%s' %(user_id,search_category))
        x=cur.fetchall()
        stores_id=[int(row[0]) for row in x]
        stores_x=[float(row[1]) for row in x]
        stores_y=[float(row[2]) for row in x]
        similarity=[float(row[3]) for row in x]
        y= zip(stores_id,stores_x,stores_y,similarity)
        return y

    def get_category_and_weight_order_by_weight(self,user_id):
        cur=self.cur
        cur.execute('SELECT category, weight FROM public.category_weight where user_id=%s order by weight' %user_id)
        x=cur.fetchall()
        category_id=[int(row[0]) for row in x]
        category_weight=[float(row[1]) for row in x]
        result=[]
        for i in range(0,len(category_id)):
            if category_weight[i]!=0:
                result.append([category_id[i],category_weight[i]])


        return result

    def get_stores_id_and_coordinate_and_similarity(self,search_category):
        cur = self.cur
        cur.execute('SELECT  store_id, store_coordinate_x, store_coordinate_y,similarity FROM public.user_store where search_category=%s' %(search_category))
        x=cur.fetchall()
        stores_id=[int(row[0]) for row in x]
        stores_x=[float(row[1]) for row in x]
        stores_y=[float(row[2]) for row in x]
        similarity=[float(row[3]) for row in x]
        y= zip(stores_id,stores_x,stores_y,similarity)
        return y

# x = DataBaseQuery()
# print x.get_category_and_weight_order_by_weight(1)
