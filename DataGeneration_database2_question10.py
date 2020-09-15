# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 03:58:02 2020

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

conn = sqlite3.connect('testQ.db')
c = conn.cursor()   
with open('lookup1.json') as json_file: 
    data = json.load(json_file)

with open('uniquelookup.json') as json_file:
    data2 = json.load(json_file)

with open('state_dict.json') as json_file:
    state_dict = json.load(json_file)
    
question_template = "What is the racial breakdown of (Case Entity) in (State Entity)?"
question_template_id = 'db2q10' 

question_key = {}
output = {}
case_entity_list= ['cases', 'confirmed cases', 'deaths']
location_entity_list = ['(State)', '(State Abbreviation)', 'the state of (State)']
count = 1
entities = ['Case Entity', 'State Entity']
sql_template = "Select Case Entity Column_Total,Case Entity Column_White, Case Entity Column_Black,Case Entity Column_LatinX, Case Entity Column_Asian,Case Entity Column_NHPI, Case Entity Column_Multiracial, Case Entity Column_Other, Case Entity Column_Unknown from db2race where date = 'given date' and state = \"State Entity\" "
for i in case_entity_list:
    for j in location_entity_list: 
        for k in range(50):
            output[count] = []
            populated_entities = []
            case_e = i
            if j.find("(State)")>=0: 
                state_name = random.choice(data2['State'])
                while state_name == 'Diamond Princess': 
                    state_name = random.choice(data2['State'])
                key_list = list(state_dict.keys())
                val_list = list(state_dict.values())
                state_abbreviation = key_list[val_list.index(state_name)]
                if i == 'cases' or i == 'confirmed cases':
                    query = sql_template.replace("Case Entity Column", "Cases")
                else:
                    query = sql_template.replace("Case Entity Column", "Deaths")
                loc = j.replace("(State)", state_name)
                query = query.replace("State Entity", state_abbreviation)
            else:
                state_abbreviation = random.choice(data2['State Abbreviation'])
                if i == 'cases' or i == 'confirmed cases':
                    query = sql_template.replace("Case Entity Column", "Cases")
                else:
                    query = sql_template.replace("Case Entity Column", "Deaths")
                loc = j.replace("(State Abbreviation)", state_abbreviation)
                query = query.replace("State Entity", state_abbreviation)
            today = datetime.date.today()-datetime.timedelta(days=2)
            if today.weekday() == 1 or today.weekday() == 0:
                date = today-datetime.timedelta(days=today.weekday()+1)
            elif today.weekday() == 6 or today.weekday() == 2:
                date = today
            else:
                date = today - datetime.timedelta(days=today.weekday()-2)
            query = query.replace("given date", str(date).replace("-", ""))
            real_question = question_template.replace("(State Entity)", loc)
            real_question = real_question.replace("(Case Entity)", case_e)
            populated_entities.append(loc)
            populated_entities.append(case_e)
            c.execute(query)
            result = c.fetchall()
            #if len(result) == 0 or result[0][0] == None:
            #    continue
            if real_question in question_key.keys():
                continue
            else:
                question_key[real_question] = True
                output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
                     'entities' : entities, 'question' : real_question, 
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 2'})
                print(count)
                print(question_template)
                print(sql_template)
                print(real_question)
                print(query)
                print(result)
    
                count = count +1
with open('db2q10data.json', 'w') as outfile: 
    json.dump(output,outfile)
            
print("done")
                