# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 02:38:15 2020

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

"""print(data)
print("")
print(data2)"""

conn = sqlite3.connect('testQ.db')
c = conn.cursor()
question_key = {}
question_template = 'What is the racial breakdown of Covid-19 deaths in (Location Entity)?'
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
output = {}
question_template_id = 'db5q4'
entities = ['Location Entity']
count = 1
key_county = {}
while count < 300:
    output[count] = []
    location = random.choice(data["Location Entity"])
    while location.find("County")<0: 
        location = random.choice(data["Location Entity"])
    entity = re.findall('\(([^)]+)', location)
    query = ""
    populated_entities = []
    sql_template  = """Select Deaths, Non_Hispanic_White, Non_Hispanic_Black, Non_Hispanic_AIAN, Non_Hispanic_Asian, Other, Hispanic from db5 where Indicator = \"Distribution of COVID-19 deaths (%)\" and State = \"State_Abbreviation\" and County_Name = \"given county\""""
    if entity[1] == 'State': 
        county_list = random.choice(data2['County']).split(', ')
        county_name = county_list[0]
        state_name = county_list[1]
        loc = location.replace("(County)", county_name + " County")
        loc = loc.replace("(State)", state_name)
        key_list = list(state_dict.keys())
        val_list = list(state_dict.values())
        state_abbreviation = key_list[val_list.index(state_name)]
        query = sql_template.replace("State_Abbreviation", state_abbreviation)
        query = query.replace("given county", county_name + " County")
        populated_entities.append(county_name + ", " + state_name)
        real_question = question_template.replace("(Location Entity)", loc)
        
        
        
    else:
        county_list = random.choice(data2['County']).split(', ')
        county_name = county_list[0]
        state_name = county_list[1]
        key_list = list(state_dict.keys())
        val_list = list(state_dict.values())
        state_abbreviation = key_list[val_list.index(state_name)]
        loc = location.replace("(County)", county_name + " County   ")
        loc = loc.replace("(State Abbreviation)", state_abbreviation)
        query = sql_template.replace("State_Abbreviation", state_abbreviation)
        query = query.replace("given county", county_name + " County")
        populated_entities.append(county_name + ", " + state_name)
        real_question = question_template.replace("(Location Entity)", loc)
    c.execute(query)
    result = c.fetchall()
    if len(result) == 0 or result[0][0] == None:
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
        count = count + 1
