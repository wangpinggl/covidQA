# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 19:39:04 2020

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
question_template = 'How many (Race Entity) deaths occured in (Location Entity)?'
question_template_id = 'db5q3'
output = {}

count = 1
entities = ['Race Entity', 'Location Entity']

def generateQuery(race):
    specific_race = ''
    #if race == "people of color":
     #   race_input = "Non_Hispanic_Black"

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
  
    real_sub = race.replace("(race)", specific_race)
    real_question = question_template.replace("(Race Entity)", real_sub)
    query = sql_template.replace("(given race)", race_input)
    query = query.replace("Given County", county_name + " County")
    query = query.replace("State Abbreviation", state_abbreviation)
    return real_question, query, real_sub
while count < 300: 
    output[count] = []
    populated_entities = []
    location = random.choice(data['Location Entity'])
    while location.find("County") <0:
        location = random.choice(data['Location Entity'])
    entity = re.findall('\(([^)]+)', location)
    query = ""
    sql_template = "Select Round((Select (given race) from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Abbreviation\" and County_Name = \"Given County\") * (Select Deaths from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Abbreviation\" and County_Name = \"Given County\"))"
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
        while race.find("people of mixed color") >= 0 or race.find("mixed")  >= 0 or race.find("multiracial")>=0 or race.find("people of two or more races") >=0 or race.find("people of color") >=0 or race.find("(race) people") >=0: 
            race = random.choice(data['Race'])
        real_question, query, real_sub = generateQuery(race)
        real_question = real_question.replace("(Location Entity)", loc)
        
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
        while race.find("people of mixed color") >= 0 or race.find("mixed")  >= 0 or race.find("multiracial")>=0 or race.find("people of two or more races") >=0 or race.find("people of color") >=0 or race.find("(race) people") >=0: 
            race = random.choice(data['Race'])
        real_question, query, real_sub = generateQuery(race)
        real_question = real_question.replace("(Location Entity)",loc)
    populated_entities.append(real_sub)
    populated_entities.append(loc)
    c.execute(query)
    result = c.fetchall()
    if result[0][0] == None or len(result) == 0:
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