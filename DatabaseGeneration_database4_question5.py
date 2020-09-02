# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 05:31:09 2020

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
conn = sqlite3.connect('testQ.db')
c = conn.cursor()    
question_template = "What state will have the (Value Entity) total forecasted number of deaths (Time Entity)?"
question_template_id = 'db4q5'
output = {}
question_key = {}
entities = ['Value Entity', 'Time Entity']
time_values =  ['in the next (x) days', 'in the next (x) weeks', 'in the next week', 'tomorrow', 'day after tomorrow']

count = 1 

def queryEndDate(query, time_entity):
    today = datetime.date.today()
    output = time_entity
    if time_entity == 'in the next (x) days':
        num_day = random.randint(1,20)
        future_date = today + datetime.timedelta(days = num_day)
        output = output.replace("(x)", str(num_day))
    elif time_entity == 'in the next (x) weeks':
        num_week = random.randint(2,3)
        future_date = today + datetime.timedelta(days=num_week * 7)
        output = output.replace("(x)", str(num_week))
    elif time_entity == 'in the next week':
        future_date = today + datetime.timedelta(days=7)
    elif time_entity == 'tomorrow': 
        future_date = today + datetime.timedelta(days=1)
    elif time_entity == 'day after tomorrow': 
        future_date = today + datetime.timedelta(days=2)
    if future_date.weekday() == 5: 
        query = query.replace("given date", str(future_date))
    elif future_date.weekday() ==6:
        query = query.replace("given date", str(future_date + datetime.timedelta(days=6)))
    else:
        query = query.replace("given date", str(future_date + datetime.timedelta(days=5-future_date.weekday())))
    return query, output


while count < 250: 
    output[count] = []
    populated_entities = []
    time_entity = random.choice(time_values)
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
    
    sql_template = "Select location_name, Max(point) from db4forecaststate WHERE target_week_end_date = 'given date' and location_name != 'National' group by location_name order by Max(point) asc/desc limit X,1" 
    query = sql_template
    query, time_e = queryEndDate(query,time_entity)
    if ascending == False:
        query = query.replace("asc/desc", "desc")
        query = query.replace("X", str(order-1))
    else:
        query = query.replace("asc/desc", "asc")
        query = query.replace("X", str(order-1))
    real_question = question_template.replace("(Time Entity)", time_e)
    real_question = real_question.replace("(Value Entity)", val)
    populated_entities.append(val)
    populated_entities.append(time_e)
    c.execute(query)
    result = c.fetchall()
    if len(result) == 0 or result[0][0] == None: 
        continue
    elif real_question in question_key.keys():
        continue
    else:
        question_key[real_question] = True
        output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
                 'entities' : entities, 'question' : real_question, 
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 4'})
        print(count)
        print(real_question)
        print(query)
        print(result)
        count = count + 1