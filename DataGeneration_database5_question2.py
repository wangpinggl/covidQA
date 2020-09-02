# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 16:22:34 2020

@author: Srikar Balusu
"""

import json
import pandas as pd
import numpy as np
import re
import random
import sqlite3


with open('lookup1.json') as json_file: 
    data = json.load(json_file)

with open('uniquelookup.json') as json_file:
    data2 = json.load(json_file)


conn = sqlite3.connect('testQ.db')
c = conn.cursor()
question_key = {}
state_dict = {'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'}

question_template = "Which county in (Location Entity) has the (Value Entity) percentage of deaths from (Race Entity)?"
question_template_id = 'db5q2'
output = {}

count = 1

entities = ['Location Entity', 'Value Entity', 'Race Entity']
location_entity = ['the state of (State)', '(State Abbreviation)', '(State)']


def generateQuery(race, ascending): 
    specific_race = ''
    if race == "people of color":
        race_input = "Non_Hispanic_Black"
    else: 
        specific_race = random.choice(data2['Race'])
        while specific_race.find("multiracial") >=0 or specific_race.find("mixed") >=0 or specific_race.find("Pacific Islander") >=0 or specific_race.find("Native Hawaiian") >=0 or specific_race.find("Pacific Islander and Native Hawaiian") >=0 or ((specific_race.find("Hispanic")>=0 or specific_race.find("Latino") >=0) and race.find("Non-Hispanic") >=0):
            specific_race = random.choice(data2['Race'])
        if specific_race.find("African-American") >=0 or specific_race.find("Black")>=0: 
            race_input = "Non_Hispanic_Black"
        elif specific_race.find("Hispanic") >=0 or specific_race.find("Latino") >=0:
            race_input = "Hispanic"
        elif specific_race.find("Asian")>=0:
            race_input = "Non_Hispanic_Asian"
        elif specific_race.find("Alaska Native") >= 0 or specific_race.find("American Indian or Alaska Native") >=0 or specific_race.find("American Indian") >=0:
            race_input = "Non_Hispanic_AIAN"
        else:
            race_input = "Non_Hispanic_White"
  
    if race.find("people of color") >=0:
        real_question = question_template.replace("(Race Entity)", race)
        real_sub = race
    elif race.find("people") <0:
        if specific_race == 'American Indian or Alaska Native':
            real_sub = race.replace("(race)",  'American Indians or Alaska Natives')
        else:
            real_sub = race.replace("(race)", specific_race + 's')
        real_question = question_template.replace("(Race Entity)", real_sub)
    else:
        real_sub = race.replace("(race)", specific_race)
        real_question = question_template.replace("(Race Entity)", real_sub)
    
    query = sql_template.replace("(State Abbreviation)", state_abbreviation)
    query = query.replace("(given race)", race_input)
    if ascending ==False:
        query = query.replace("asc/desc", "desc")
        query = query.replace("X",  str(order-1))
    else:
        query = query.replace("asc/desc", "asc")
        query = query.replace("X", str(order-1))
    return real_question, query, real_sub

while count < 300: 
    output[count] = []
    populated_entities = []
    if count%3 == 0:
        location = location_entity[0]
    elif count%3==1:
        location = location_entity[1]
    else:
        location = location_entity[2]
    
    val = random.choice(data['Value Entity'])
    if val.find("(x)") >= 0:
        order = random.randint(1,5)
        val = val.replace("(x)", str(order))
        if order == 2: 
            val = val.replace("th", "nd")
        if order == 3: 
            val = val.replace("th", "rd")
        if order == 1: 
            val = val.replace("th", "st")
    else:
        order = 1
    if val.find("most") >= 0 or val.find("highest") >=0 or val.find("Highest") >=0:
        ascending = False
    else:
        ascending = True
    entity = re.findall('\(([^)]+)', location)
    query = ""
    sql_template = "Select County_Name from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = '(State Abbreviation)' order by (given race) asc/desc limit X,1"
    if entity[0] == 'State': 
        state_name = random.choice(data2['State'])
        while state_name == 'Diamond Princess':
            state_name = random.choice(data2['State'])
        key_list = list(state_dict.keys())
        val_list = list(state_dict.values())
        state_abbreviation = key_list[val_list.index(state_name)]
      
        race = random.choice(data['Race'])
        while race.find("people of mixed color") >= 0 or race.find("mixed")  >= 0 or race.find("multiracial")>=0 or race.find("people of two or more races") >=0: 
            race = random.choice(data['Race'])
        real_question, query, real_sub = generateQuery(race,ascending)
        real_question = real_question.replace("(Location Entity)", state_name)
        real_question = real_question.replace("(Value Entity)", val)
        location = location.replace("(State)", state_name)
        populated_entities.append(location)
        populated_entities.append(val)
        populated_entities.append(real_sub)
        
    else:
        state_abbreviation = random.choice(data2['State Abbreviation'])
        race = random.choice(data['Race'])
        while race.find("people of mixed color") >= 0 or race.find("mixed")  >= 0 or race.find("multi") >=0 or race.find("people of two or more races") >=0: 
            race = random.choice(data['Race'])
        real_question, query, real_sub= generateQuery(race,ascending)
        real_question = real_question.replace("(Location Entity)", state_abbreviation)
        real_question = real_question.replace("(Value Entity)", val)
        location = location.replace("(State Abbreviation)", state_abbreviation)
        populated_entities.append(location)
        populated_entities.append(val)
        populated_entities.append(real_sub)
   
    c.execute(query)
    result = c.fetchall()
    if len(result) == 0:
        continue
    elif real_question in question_key.keys():
        continue
    else:
        output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
                 'entities' : entities, 'question' : real_question, 
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 5'})
        question_key[real_question] = True
        print(count)
        print(real_question)
        print(query)
        print(result)
        count = count  + 1

