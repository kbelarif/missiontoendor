#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 2 11:09:20 2019

@author: kamel
"""
import planet 
from operator import attrgetter
import numpy as np
import sqlite3
import json
import pandas as pd
import os

arrival_planet = str()
autonomy_spaceship = int()
bounty_hunters = list()
countdown = int()
data_frame = pd.DataFrame()
departure_planet = str()
planets_list = list()

def CreateVariables():
    with open('empire.json') as empire_data:
        empire_data_dict = json.load(empire_data)
    with open('millenium-falcon.json') as millenium_falcon:
        millenium_falcon_dict = json.load(millenium_falcon)
        countdown = empire_data_dict.get("countdown")                                   
        bounty_hunters = empire_data_dict.get('bounty_hunters')
        autonomy_spaceship = millenium_falcon_dict.get("autonomy")
        departure_planet = millenium_falcon_dict.get("departure")
        arrival_planet = millenium_falcon_dict.get("arrival")
        del empire_data_dict
#connection to the data base and creation of an np.array containing all the 
#informations
    connexion = sqlite3.connect(millenium_falcon_dict.get("routes_db"))
    cursor = connexion.cursor()
    cursor.execute("""SELECT ORIGIN, DESTINATION, TRAVEL_TIME FROM routes""")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        rows[i] = list(rows[i])
        connexion.close()
    del millenium_falcon_dict
#creation of a list of planets
    index = []
    columns = []
    for i in range(len(rows)):
        index.append(list(rows[i])[1])
        columns.append(list(rows[i])[0])
    planets_list = list(set(list(set(index)) + list(set(columns))))
    del index
    del columns

#matrix containing the travel time between planets
    data = np.eye(len(planets_list))
    data_frame = pd.DataFrame(data,planets_list,planets_list)
    del data
    for i in range(len(rows)):
        data_frame.loc[rows[i][0],rows[i][1]] = data_frame.loc[rows[i][1],
                   rows[i][0]] = rows[i][2]
    del rows
    del i
    return [arrival_planet,autonomy_spaceship,bounty_hunters, countdown,data_frame,departure_planet,planets_list]  

def CanITravel(li,elt,time):
    if  time >= countdown or data_frame[li[-1]][elt] == 0 or\
    time + data_frame[li[-1]][elt] > countdown or\
    (time == countdown and li[-1] != arrival_planet ):
        return False
    else:
        return True
    
def NeedToRefuel(li,elt,autonomy,time):
    if autonomy < data_frame[li[-1]][elt]:
        return True
    else:
        return False  

def PassPath(li):
    if li[-1] == arrival_planet:
        return True
    else:
        return False

def CreatePaths(path_list,autonomy_list,time_list):
    new_path_list=list()
    new_autonomy_list=list()
    new_time_list=list()
    for elt in planets_list:
        for li in path_list:
            if li not in new_path_list:
                if PassPath(li):
                    L = list(li)
                    new_path_list.append(li)
                    new_autonomy_list.append(autonomy_list[path_list.index(li)])
                    new_time_list.append(time_list[path_list.index(li)])
                elif not CanITravel(li,elt,time_list[path_list.index(li)][-1]):
                    continue
                elif NeedToRefuel(li,elt,autonomy_list[path_list.index(li)][-1],time_list[path_list.index(li)][-1]):
                    L=list(li)
                    L.append(li[-1])
                    new_path_list.append(L)
                    L=list(autonomy_list[path_list.index(li)])
                    L.append(autonomy_spaceship)
                    new_autonomy_list.append(L)
                    L=list(time_list[path_list.index(li)])
                    L.append(time_list[path_list.index(li)][-1] + 1 )
                    new_time_list.append(L)
                elif li[-1] == elt:
                    L=list(li)
                    L.append(elt)
                    new_path_list.append(L)
                    L=list(autonomy_list[path_list.index(li)])
                    L.append(autonomy_list[path_list.index(li)][-1])
                    new_autonomy_list.append(L)
                    L=list(time_list[path_list.index(li)])
                    L.append(time_list[path_list.index(li)][-1] +1)
                    new_time_list.append(L)            
                else:
                    L=list(li)
                    L.append(elt)
                    new_path_list.append(L)
                    L=list(autonomy_list[path_list.index(li)])
                    L.append(autonomy_list[path_list.index(li)][-1] - data_frame[path_list[path_list.index(li)][-1]][elt])
                    new_autonomy_list.append(L)
                    L=list(time_list[path_list.index(li)])
                    L.append(time_list[path_list.index(li)][-1] + data_frame[path_list[path_list.index(li)][-1]][elt])
                    new_time_list.append(L)
            else:
                continue     
    return (new_path_list, new_autonomy_list, new_time_list)


def EndingCondition(path_list):
    cond=True
    if len(path_list) == 0:
        return cond
    else:
        for elt in path_list:
         if elt[-1]==arrival_planet:
             continue
         else:
             cond= False
             break
        return cond

def CreateAdmissiblePaths():
    admissible_path = [[[departure_planet]],[[autonomy_spaceship]] ,[[0]]] 
    while not EndingCondition(admissible_path[0]): 
        admissible_path = CreatePaths(admissible_path[0],admissible_path[1],admissible_path[2])
    return list(admissible_path)

def BountyHunterCount(path,time_path):
    k=0
    for elt in bounty_hunters:
        if elt['day'] in time_path and elt['planet'] == path[time_path.index(elt['day'])]:
            k +=1
    return k

def ProbaOfSuccess(path,time_path):
    k = BountyHunterCount(path,time_path)
    proba=0
    if k == 0:
        return 0
    else:
        for i in range(k):
            proba += 9**i/10**(i+1)                             
        return proba

def PathProbaOfSuccess():
    admissible_path = CreateAdmissiblePaths()
    path_list = admissible_path[0]
    autonomy_list = admissible_path[1]
    time_list = admissible_path[2]
    proba_list=list()
    if len(path_list) == 0:
        return False
    else:
        for li in path_list:
            proba_list.append(1 - ProbaOfSuccess(li,time_list[path_list.index(li)]))
        return[path_list,autonomy_list,time_list,proba_list]

def CreateDataList():
    if os.path.exists('empire.json'):
        variable = CreateVariables()
        global arrival_planet
        global autonomy_spaceship
        global bounty_hunters
        global countdown
        global data_frame
        global departure_planet
        global planets_list
        arrival_planet = variable[0]
        autonomy_spaceship = variable[1]
        bounty_hunters = variable[2]
        countdown = variable[3]
        data_frame = variable[4]
        departure_planet = variable[5]
        planets_list = variable[6]
        os.remove('empire.json')
    li = PathProbaOfSuccess()
    data_path_list = list()
    if li == False:
        return False
    else:
        for elt in range(len(li[0])):
            new_data = planet.DataPath()
            new_data.path = li[0][elt]
            new_data.autonomy = li[1][elt]
            new_data.time = li[2][elt]
            new_data.proba = li[3][elt]
            data_path_list.append(new_data)
        return sorted(data_path_list, key=attrgetter("proba"))