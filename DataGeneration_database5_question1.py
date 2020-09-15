# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 19:03:00 2020

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

question_template = "What percentage of Covid-19 deaths in (County Entity) (State Entity) are from (Race Entity)?"
question_template_id = 'db5q1'
output = {}

count = 1
question_key = {}
entities = ['County Entity','State Entity', 'Race Entity']

def generateQuery(race): 
    specific_race = ''
    if race == "people of color":
        race_input = "Non_Hispanic_Black"
    else: 
        specific_race = random.choice(data2['Race'])
        while specific_race.find("multiracial") >=0 or specific_race.find("mixed") >=0 or specific_race.find("Pacific Islander") >=0 or specific_race.find("Native Hawaiian") >=0 or specific_race.find("Pacific Islander and Native Hawaiian") >=0 or ((specific_race.find("Hispanic")>=0 or specific_race.find("Latino")>=0) and race.find("Non-Hispanic") >=0):
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
    query = sql_template.replace("Race Entity Column", race_input)
    query = query.replace("County Entity", county_name + " County")
    query = query.replace("State Entity", state_abbreviation)
    return real_question, query, real_sub
while count < 300: 
    populated_entities = []
    output[count] = []
    location = random.choice(data['Location Entity'])
    while location.find("County")<0:
        location = random.choice(data['Location Entity'])
    entity = re.findall('\(([^)]+)', location)
    query = ""
    populated_entities = []
    sql_template = "Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and County_Name = \"County Entity\" and State = \"State Entity\""
    if entity[1] == 'State': 
        county_list = county_list = random.choice(data2['County']).split(', ')
        county_name = county_list[0]
        state_name = county_list[1]
        loc = location.replace("(County)", county_name + " County")
        loc = loc.replace("(State)", state_name)
        key_list = list(state_dict.keys())
        val_list = list(state_dict.values())
        state_abbreviation = key_list[val_list.index(state_name)]
        race = random.choice(data['Race'])
        while race.find("people of mixed color") >= 0 or race.find("mixed")  >= 0 or race.find("multiracial")>=0 or race.find("people of two or more races") >=0: 
            race = random.choice(data['Race'])
        real_question, query, real_sub = generateQuery(race)
        real_question = real_question.replace("(County Entity) (State Entity)",loc)
        populated_entities.append(loc)
        populated_entities.append(real_sub)
    else:
        county_list = county_list = random.choice(data2['County']).split(', ')
        county_name = county_list[0]
        state_name = county_list[1]
        key_list = list(state_dict.keys())
        val_list = list(state_dict.values())
        state_abbreviation = key_list[val_list.index(state_name)]
        loc = location.replace("(County)", county_name + " County")
        loc = loc.replace("(State Abbreviation)", state_abbreviation)
        race = random.choice(data['Race'])
        while race.find("people of mixed color") >= 0 or race.find("mixed")  >= 0 or race.find("multiracial")>=0 or race.find("people of two or more races") >=0: 
            race = random.choice(data['Race'])
        real_question, query, real_sub = generateQuery(race)
        real_question = real_question.replace("(County Entity) (State Entity)",loc)
        populated_entities.append(loc)
        populated_entities.append(real_sub)
    c.execute(query)
    result = c.fetchall()
    if len(result) == 0:
        continue
    elif real_question in question_key.keys():
        continue
    else:
        question_key[real_question] = True
        output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
                 'entities' : entities, 'question' : real_question, 
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 5'})
        count = count + 1
        print(count)
        print(question_template)
        print(sql_template)
        print(real_question)
        print(query)
        print(result)
with open('db5q1data.json', 'w') as outfile: 
    json.dump(output,outfile)
print("done")