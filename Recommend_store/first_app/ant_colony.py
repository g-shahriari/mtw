from __future__ import division
# -*- coding: utf-8 -*-
import sys
import itertools
import bisect
import random






count_category=4
category_with_max_frequency=10
cat_1_points=[(1199, 630), (2151, 2435), (1792, 1119), (1025, 1737), (2166, 1844), (2393, 872), (1510, 1467), (1893, 2143), (185, 780), (826, 973)]
cat_2_points=[(1634, 297), (1561, 1980), (636, 1349), (1869, 548), (751, 475), (2182, 722), (1486, 1565), (400, 644), (514, 340), (2464, 1644)]
cat_3_points=[[228, 78], [2342, 1129], [791, 775], [1994, 1553], [1605, 500], [2051, 852], [1960, 198], [1912, 2411], [1287, 142], [1328, 1195]]
cat_4_points=[(219, 687), (965, 1918), (2012, 872), (2367, 501), (1239, 1539), (156, 2279), (1526, 865), (2450, 2478), (1311, 663), (1729, 548)]
cat_1_weights=[0.78, 0.48, 0.45, 0.05, 0.95, 0.45, 0.25, 0.67, 0.22, 0.39]
cat_2_weights=[0.47, 0.31, 0.2, 0.23, 0.15, 0.68, 0.19, 0.32, 0.36, 0.81]
cat_3_weights=[0.07, 0.12, 0.99, 0.52, 0.55, 0.85, 0.06, 0.34, 0.32, 0.01]
cat_4_weights=[0.19, 0.03, 0.96, 0.36, 0.96, 0.69, 0.42, 0.37, 0.85, 0.4]

points= [[[0,1,54,86,0.1],[0,2,371,142,0.2],[0,3,187,274,0.7],[0,4,430,420,0.3]],[[0,5,187,38,0.2],[0,6,497,153,0.4],[0,7,152,274,0.7],[0,8,343,490,0.2]],[[0,9,5,207,0.1],[0,10,471,24,0.3],[0,11,233,291,0.5],[0,12,515,494,0.2]],[[0,13,11,11,0.1],[0,14,359,36,0.3],[0,15,219,236,0.6],[0,16,503,340,0.2]]]
poimt_pheromone=[[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
class AntColony():



    def calculate_fitness_function(self,distances,weights,max_distance):



        sum_weights=0
        for j in range(0,len(weights)):
            sum_weights += weights[j]


            fit_func=distances/sum_weights
        # else:
        #     fit_func=-9999
        return fit_func

    def sum_pheromone(self,pheromones):

        sum_pheromones=0
        for i in range(0,len(pheromones)):
            sum_pheromones += pheromones[i]
        return sum_pheromones

    def calculate_probability(self,points_code,points_pheromone):

        sum_pheromone = self.sum_pheromone(points_pheromone)

        probabilty=list()
        for i in range(0,len(points_pheromone)):
            point_phero=float(points_pheromone[i]/sum_pheromone)
            probabilty.append([points_code[i],point_phero])
        return probabilty

    def update_pheromone(self,point_pheromone,point_code):
        pheromone= point_pheromone+0.1
        return pheromone

    def evaporation_pheromone(self,points_pheromone,ro_value):

        # evap_pheromone=list()
        # for i in range(0,len(points_code)):
        evap_pheromone =(1-ro_value)*points_pheromone
            # evap_pheromone.append([points_code[i],pheromone])

        return evap_pheromone

    def distance_sum(self,points_position):
        from scipy.spatial import distance_matrix
        matrix_lenght=len(points_position)
        dist_matrix= distance_matrix(points_position,points_position)
        x=0
        for i in range(0,matrix_lenght-1):
            x +=dist_matrix[i][i+1]
        return x

    def select_point(self,points_code,points_pheromone):
        import numpy as np
        import random
        probability= self.calculate_probability(points_code=points_code,points_pheromone=points_pheromone)
        point_sector_prob=list()
        point_code_sector=list()
        for i in range(0,len(points_code)):
            point_sector_prob.append(probability[i][1]*360)

        points_sector= np.cumsum(point_sector_prob)
        for i in range (0,len(points_code)):
            point_code_sector.append([points_code[i],points_sector[i]])

        rand= random.random()*360


        selected_point=()

        if rand<point_code_sector[0][1] :
            selected_point=point_code_sector[0][0]

        for i in range(0,len(points_code)-1):

            if point_code_sector[i][1]<rand<point_code_sector[i+1][1] :
                selected_point=point_code_sector[i+1][0]

        return selected_point

    def selected_points_weights_and_max_distance(self,points,points_pheromone):
        from scipy.spatial import distance


        import numpy as np
        size_category_1=np.shape((points[0]))[0]
        size_category_2=np.shape((points[1]))[0]
        size_category_3=np.shape((points[2]))[0]
        size_category_4=np.shape((points[3]))[0]

        points_code_1=[points[0][i][1] for i in range(0,size_category_1)]
        points_pheromone_1=[points_pheromone[0][i] for i in range(0,size_category_1)]
        points_position_1=[[points[0][i][2],points[0][i][3]] for i in range(0,size_category_1)]
        points_weights_1=[points[0][i][4] for i in range(0,size_category_1)]

        points_code_2=[points[1][i][1] for i in range(0,size_category_2)]
        points_pheromone_2=[points_pheromone[1][i] for i in range(0,size_category_2)]
        points_position_2=[[points[1][i][2],points[1][i][3]] for i in range(0,size_category_2)]
        points_weights_2=[points[1][i][4] for i in range(0,size_category_2)]

        points_code_3=[points[2][i][1] for i in range(0,size_category_3)]
        points_pheromone_3=[points_pheromone[2][i] for i in range(0,size_category_3)]
        points_position_3=[[points[2][i][2],points[2][i][3]] for i in range(0,size_category_3)]
        points_weights_3=[points[2][i][4] for i in range(0,size_category_3)]

        points_code_4=[points[3][i][1] for i in range(0,size_category_4)]
        points_pheromone_4=[points_pheromone[3][i] for i in range(0,size_category_4)]
        points_position_4=[[points[3][i][2],points[3][i][3]] for i in range(0,size_category_4)]
        points_weights_4=[points[3][i][4] for i in range(0,size_category_4)]

        points_code_candidate=list()
        points_code_candidate.append(self.select_point(points_code_1,points_pheromone_1))
        points_code_candidate.append(self.select_point(points_code_2,points_pheromone_2))
        points_code_candidate.append(self.select_point(points_code_3,points_pheromone_3))
        points_code_candidate.append(self.select_point(points_code_4,points_pheromone_4))

        points_code_selected=list()
        points_code_selected=random.sample(points_code_candidate,4)




        point_code_position_x=list()
        point_code_position_y=list()
        point_code_weight=list()
        point_position=list()

        for k in range(0,4):
            for i in range (0,len(points_code_1)):
                if points_code_selected[k]==points_code_1[i]:
                    point_code_position_x.append(points_position_1[i][0])
                    point_code_position_y.append(points_position_1[i][1])
                    point_position.append([points_position_1[i][0],points_position_1[i][1]])
                    point_code_weight.append([points_code_1[i],points_weights_1[i],points_pheromone_1[i]])


            for i in range (0,len(points_code_2)):
                if points_code_selected[k]==points_code_2[i]:
                    point_code_position_x.append(points_position_2[i][0])
                    point_code_position_y.append(points_position_2[i][1])
                    point_position.append([points_position_2[i][0],points_position_2[i][1]])
                    point_code_weight.append([points_code_2[i],points_weights_2[i],points_pheromone_2[i]])


            for i in range (0,len(points_code_3)):
                if points_code_selected[k]==points_code_3[i]:
                    point_code_position_x.append(points_position_3[i][0])
                    point_code_position_y.append(points_position_3[i][1])
                    point_position.append([points_position_3[i][0],points_position_3[i][1]])
                    point_code_weight.append([points_code_3[i],points_weights_3[i],points_pheromone_3[i]])


            for i in range (0,len(points_code_4)):
                if points_code_selected[k]==points_code_4[i]:
                    point_code_position_x.append(points_position_4[i][0])
                    point_code_position_y.append(points_position_4[i][1])
                    point_position.append([points_position_4[i][0],points_position_4[i][1]])
                    point_code_weight.append([points_code_4[i],points_weights_4[i],points_pheromone_4[i]])

        min_x=min(point_code_position_x)
        max_x=max(point_code_position_x)
        min_y=min(point_code_position_y)
        max_y=max(point_code_position_y)
        edge_min=(min_x,min_y)
        edge_max=(max_x,max_y)


        dist =self.distance_sum(point_position)
        point_code_weight.append([-999,-999,dist])
        return point_code_weight

    def ant(self,points,points_pheromone):


        point_code_weight_max_dist=self.selected_points_weights_and_max_distance(points,points_pheromone)
        for i in range(0,len(point_code_weight_max_dist)):
            import numpy as np
            size_category_1=np.shape((points[0]))[0]
            size_category_2=np.shape((points[1]))[0]
            size_category_3=np.shape((points[2]))[0]
            size_category_4=np.shape((points[3]))[0]
            points_code_1=[points[0][i][1] for i in range(0,size_category_1)]
            points_code_2=[points[1][i][1] for i in range(0,size_category_2)]
            points_code_3=[points[2][i][1] for i in range(0,size_category_3)]
            points_code_4=[points[3][i][1] for i in range(0,size_category_4)]

            points_pheromone_1=[points_pheromone[0][i] for i in range(0,size_category_2)]
            points_pheromone_2=[points_pheromone[1][i] for i in range(0,size_category_2)]
            points_pheromone_3=[points_pheromone[2][i] for i in range(0,size_category_3)]
            points_pheromone_4=[points_pheromone[3][i] for i in range(0,size_category_4)]

            max_dist=point_code_weight_max_dist.pop()[2]
            selected_weights=[row[1] for row in point_code_weight_max_dist]
            print selected_weights
            selected_point = [row[0] for row in point_code_weight_max_dist]
            fit_func = self.calculate_fitness_function(max_dist,selected_weights,max_distance=20000)
            if fit_func !=-9999:
                break

            for j in range(0,len(points_code_1)):
                if points_code_1==point_code_weight_max_dist[i][0]:
                    points_pheromone_1=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])

            for j in range(0,len(points_code_2)):
                if points_code_2[j]==point_code_weight_max_dist[i][0]:
                    points_pheromone_2[j]=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])

            for j in range(0,len(points_code_3)):
                if points_code_3[j]==point_code_weight_max_dist[i][0]:
                    points_pheromone0_3[j]=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])

            for j in range(0,len(points_code_4)):
                if points_code_4[j]==point_code_weight_max_dist[i][0]:
                    points_pheromone_4[j]=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])

            points_pheromone=[points_pheromone_1,points_pheromone_2,points_pheromone_3,points_pheromone_4]
                # points_pheromone[j]=self.evaporation_pheromone(points_pheromone=points_pheromone[j],ro_value=0.1)

        for i in range(0,100):
            point_code_weight_max_dist=self.selected_points_weights_and_max_distance(points,points_pheromone)
            size_category_1=np.shape((points[0]))[0]
            size_category_2=np.shape((points[1]))[0]
            size_category_3=np.shape((points[2]))[0]
            size_category_4=np.shape((points[3]))[0]
            points_code_1=[points[0][i][1] for i in range(0,size_category_1)]
            points_code_2=[points[1][i][1] for i in range(0,size_category_2)]
            points_code_3=[points[2][i][1] for i in range(0,size_category_3)]
            points_code_4=[points[3][i][1] for i in range(0,size_category_4)]

            points_pheromone_1=[points_pheromone[0][i] for i in range(0,size_category_1)]
            points_pheromone_2=[points_pheromone[1][i] for i in range(0,size_category_2)]
            points_pheromone_3=[points_pheromone[2][i] for i in range(0,size_category_3)]
            points_pheromone_4=[points_pheromone[3][i] for i in range(0,size_category_4)]


            max_dist=point_code_weight_max_dist.pop()[2]
            selected_weights=[row[1] for row in point_code_weight_max_dist]
            # selected_point = [row[0] for row in point_code_weight_max_dist]
            fit_func_candidate = self.calculate_fitness_function(max_dist,selected_weights,max_distance=2000)

            if fit_func_candidate<fit_func and fit_func_candidate != -9999:
                fit_func=fit_func_candidate
                selected_point=  [row[0] for row in point_code_weight_max_dist]
                for i in range(0,len(selected_weights)):
                    for x,k,n,m in zip(range(0,len(points_code_1)),range(0,len(points_code_2)),range(0,len(points_code_3)),range(0,len(points_code_4))):
                        if points_code_1[x]==point_code_weight_max_dist[i][0]:
                            points_pheromone_1[x]=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])
                            # points_pheromone_1[j]=self.evaporation_pheromone(points_pheromone=points_pheromone[j],ro_value=0.1)

                        elif points_code_2[k]==point_code_weight_max_dist[i][0]:
                            points_pheromone_2[k]=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])
                            # points_pheromone_2[k]=self.evaporation_pheromone(points_pheromone=points_pheromone_2[k],ro_value=0.1)

                        elif points_code_3[m]==point_code_weight_max_dist[i][0]:
                            points_pheromone_3[m]=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])
                            # points_pheromone_3[m]=self.evaporation_pheromone(points_pheromone=points_pheromone_3[m],ro_value=0.1)

                        elif points_code_4[n]==point_code_weight_max_dist[i][0]:
                            points_pheromone_4[n]=self.update_pheromone(point_pheromone=point_code_weight_max_dist[i][2],point_code=point_code_weight_max_dist[i][0])
                            # points_pheromone_4[n]=self.evaporation_pheromone(points_pheromone=points_pheromone_4[n],ro_value=0.1)

                        # else:
                        #     points_pheromone_1[j]=self.evaporation_pheromone(points_pheromone=points_pheromone_1[j],ro_value=0.1)
                        #     points_pheromone_2[k]=self.evaporation_pheromone(points_pheromone=points_pheromone_2[k],ro_value=0.1)
                        #     points_pheromone_3[m]=self.evaporation_pheromone(points_pheromone=points_pheromone_3[m],ro_value=0.1)
                        #     points_pheromone_4[n]=self.evaporation_pheromone(points_pheromone=points_pheromone_4[n],ro_value=0.1)

                points_pheromone=[points_pheromone_1,points_pheromone_2,points_pheromone_3,points_pheromone_4]


            for x,k,n,m in zip(range(0,len(points_code_1)),range(0,len(points_code_2)),range(0,len(points_code_3)),range(0,len(points_code_4))):
                points_pheromone_1[x]=self.evaporation_pheromone(points_pheromone=points_pheromone_1[x],ro_value=0.1)
                points_pheromone_2[k]=self.evaporation_pheromone(points_pheromone=points_pheromone_2[k],ro_value=0.1)
                points_pheromone_3[m]=self.evaporation_pheromone(points_pheromone=points_pheromone_3[m],ro_value=0.1)
                points_pheromone_4[n]=self.evaporation_pheromone(points_pheromone=points_pheromone_4[n],ro_value=0.1)

            points_pheromone=[points_pheromone_1,points_pheromone_2,points_pheromone_3,points_pheromone_4]





        # for i in range(0,100):
        #     if fit_func_candidate< fit_func and fit_func_candidate !=-9999:
        #         fit_func= fit_func_candidate


        return fit_func,selected_point

    def repeated_ant_colony(self,number_of_repeat,points,points_pheromone):
        t=list()
        for i in range(0,number_of_repeat):
             t.append(x.ant(points=points,points_pheromone=points_pheromone))
        return min(t)

x= AntColony()
#print x.calculate_fitness_function(distances=1300,weights=[0.1,0.3,0.1,0.4],max_distance=500)
#print x.sum_pheromone(pheromones=[1,2,3,4])
#print x.calculate_probability(points_code=[1,2,3,4],points_pheromone=[1,2,3,5])
# # print x.evaporation_pheromone(points_code=[1,2,3,4],points_pheromone=[1,2,3,5],ro_value=0.1)
#print x.select_point(points_code=[1,2,3,4],points_pheromone=[1,2,3,5])
#print(x.repeated_ant_colony(number_of_repeat=10,points_code=[1,2,3,4,5,6,7,8,9,10],points_pheromone=[1,1,1,1,1.1,1,1,1,1,1],points_position=[[711,371], [285,179], [787,391], [1103,109], [819,469], [763,465], [235,625], [681,833], [749,95], [1329,385]],points_weights=[0.74, 0.31, 0.65, 0.23, 0.80, 0.68, 0.19, 0.32, 0.36, 0.32]))
#print x.selected_points_weights_and_max_distance(points_code=[1,2,3,4,5,6,7,8,9,10],points_pheromone=[1,1,1,1,1,1,1,1,1,1],points_position=[[228, 78], [2342, 1129], [791, 775], [1994, 1553], [1605, 500], [2051, 852], [1960, 198], [1912, 2411], [1287, 142], [1328, 1195]],points_weights=[0.47, 0.31, 0.2, 0.23, 0.15, 0.68, 0.19, 0.32, 0.36, 0.81])
print(x.repeated_ant_colony(number_of_repeat=2,points=points,points_pheromone=poimt_pheromone))
