# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 01:30:30 2020

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
    

question_template = 'What state has the (Value Entity) number of people (Hospitalization Entity)?'
question_template_id = 'db2q2'
output = {}
entities = ['Value Entity', 'Hospitalization Entity']
conn = sqlite3.connect('testQ.db')
c = conn.cursor()
question_key = {}
count = 1

def hospitalizationQuery(query, hospitalization):
    date = datetime.date.today()-datetime.timedelta(days=1)
    date = str(date)
    date = date.replace("-", "")
    if hospitalization == 'Currently in ICU':
        query = query.replace("Hospitalization", "inICUCurrently")
        query = query.replace("(Null)", "inICUCurrently is not null")
    elif hospitalization == 'Cumulatively in ICU':
        query = query.replace("Hospitalization", "inICUCumulative")
        query = query.replace("(Null)", "inICUCumulative is not null")
    elif hospitalization == 'Currently on ventilators':
        query = query.replace("Hospitalization", "onVentilatorCurrently")
        query = query.replace("(Null)", "onVentilatorCurrently is not null")
    elif hospitalization == 'Cumulatively on ventilators':
        query = query.replace("Hospitalization", "onVentilatorCumulative")
        query = query.replace("(Null)", "onVentilatorCumulative is not null")
    elif hospitalization == 'Cumulatively hospitalized':
        query = query.replace("Hospitalization", "hospitalizedCumulative")
        query = query.replace("(Null)", "hospitalizedCumulative is not null")
    else:
        query = query.replace("Hospitalization", "hospitalizedCurrently")
        query = query.replace("(Null)", "hospitalizedCurrently is not null") 
    query = query.replace("given date", date)
    return query

while count <100: 
    populated_entities = []
    output[count] = []
    val = random.choice(data['Value Entity'])
    if val.find("(x)") >= 0:
        order = random.randint(1,10)
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
    hospitalization = random.choice(data['Hospitalization Entity'])
    sql_template = "Select state from db2state where date = 'given date' and (Null) order by Hospitalization asc/desc limit X,1"
    query = sql_template
    if ascending == False:
        query = query.replace('asc/desc','desc')
        query = query.replace('X', str(order-1))
    else:
        query = query.replace('asc/desc','asc')
        query = query.replace('X', str(order-1))
    query = hospitalizationQuery(query, hospitalization)
    real_question = question_template.replace("(Hospitalization Entity)", hospitalization)
    real_question = real_question.replace("(Value Entity)", val)
    populated_entities.append(val)
    populated_entities.append(hospitalization)
    c.execute(query)
    result = c.fetchall()
    #if len(result) == 0 or result[0][0] = None:
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