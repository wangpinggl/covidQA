# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 00:46:54 2020

@author: Srikar Balusu
"""




import json
import pandas as pd
import numpy as np
import re
import random
import sqlite3
import datetime
import calendar 
from dateutil.relativedelta import * 

with open('lookup1.json') as json_file: 
    data = json.load(json_file)

with open('uniquelookup.json') as json_file:
    data2 = json.load(json_file)

with open('state_dict.json') as json_file:
    state_dict = json.load(json_file)
    
question_template = 'How many people are (Hospitalization Entity) in (Location Entity)?'
question_template_id = 'db2q3'
output = {}
conn = sqlite3.connect('testQ.db')
c = conn.cursor()
question_key = {}
location_entity = ['(State)', 'the state of (State)', '(State Abbreviation)']
count = 1
entities = ['Hospitalization Entity', 'Location Entity']
def hospitalizationQuery(query, hospitalization):
    date = datetime.date.today()-datetime.timedelta(days=1)
    date = str(date)
    date = date.replace("-", "")
    if hospitalization == 'Currently in ICU':
        query = query.replace("Hospitalization", "inICUCurrently")
    elif hospitalization == 'Cumulatively in ICU':
        query = query.replace("Hospitalization", "inICUCumulative")
    elif hospitalization == 'Currently on ventilators':
        query = query.replace("Hospitalization", "onVentilatorCurrently")
    elif hospitalization == 'Cumulatively on ventilators':
        query = query.replace("Hospitalization", "onVentilatorCumulative")
    elif hospitalization == 'Cumulatively hospitalized':
        query = query.replace("Hospitalization", "hospitalizedCumulative")
    else:
        query = query.replace("Hospitalization", "hospitalizedCurrently")
    query = query.replace("current date", date)
    return query
while count < 300:
    output[count] = []
    populated_entities = []
    hospitalization = random.choice(data['Hospitalization Entity'])
    if random.random() <= 0.025: 
        location = 'United States'
        sql_template = "Select Hospitalization from db2US where date = 'current date'"
        query = sql_template
        query = hospitalizationQuery(query, hospitalization)
        real_question = question_template.replace("(Location Entity)", location)
        real_question = real_question.replace("(Hospitalization Entity)", hospitalization)
        populated_entities.append(hospitalization)
        populated_entities.append(location)
    else: 
        location = random.choice(location_entity)
        sql_template = "Select Hospitalization from db2State where date = 'current date' and state = \"State Name\" "
        if location.find("(State)") >=0:
            state_name = random.choice(data2['State'])
            while state_name == 'Diamond Princess':
                state_name = random.choice(data2['State'])
            key_list = list(state_dict.keys())
            val_list = list(state_dict.values())
            state_abbreviation = key_list[val_list.index(state_name)]
            query = sql_template.replace("State Name", state_abbreviation)
            query = hospitalizationQuery(query, hospitalization)
            loc = location.replace("(State)", state_name)
            real_question = question_template.replace("(Location Entity)", loc)
            real_question = real_question.replace("(Hospitalization Entity)", hospitalization)
        
        else: 
            state_abbreviation = random.choice(data2['State Abbreviation'])
            query = sql_template.replace("State Name", state_abbreviation)
            query = hospitalizationQuery(query, hospitalization)
            loc = location.replace("(State Abbreviation)", state_abbreviation)
            real_question = question_template.replace("(Location Entity)", loc)
            real_question = real_question.replace("(Hospitalization Entity)", hospitalization)
        populated_entities.append(hospitalization)
        populated_entities.append(loc)
        c.execute(query)
        result = c.fetchall()
        #if len(result) == 0 or result[0][0]:
        #    continue
        if real_question in question_key.keys():
            continue
        else:
            question_key[real_question] = True
            output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
                     'entities' : entities, 'question' : real_question, 
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 2'})
            print(count)
            print(real_question)
            print(query)
            print(result)
    
            count = count +1
    