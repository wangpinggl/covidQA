# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 04:31:15 2020

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
question_template = "What is the total forecasted number of deaths in (Location Entity) (Time Entity)?"
question_template_id = 'db4q4'
output = {}
entities = ['Location Entity', 'Time Entity']
time_values =  ['in the next (x) days', 'in the next (x) weeks']
loc_entity = ['(State)', '(State Abbreviation)','the state of (State)']
count = 1 
question_key = {}
def queryEndDate(query, time_entity):
    today = datetime.date.today()
    output = time_entity
    if time_entity == 'in the next (x) days':
        num_day = random.randint(1,20)
        future_date = today + datetime.timedelta(days = num_day)
        if future_date.weekday() == 5: 
            query = query.replace("given date", str(future_date))
        elif future_date.weekday() ==6:
            query = query.replace("given date", str(future_date + datetime.timedelta(days=6)))
        else:
            query = query.replace("given date", str(future_date + datetime.timedelta(days=5-future_date.weekday())))
        output = output.replace("(x)", str(num_day))
    elif time_entity == 'in the next (x) weeks':
        num_week = random.randint(1,3)
        future_date = today + datetime.timedelta(days=num_week * 7)
        if future_date.weekday() == 5: 
            query = query.replace("given date", str(future_date))
        elif future_date.weekday() ==6:
            query = query.replace("given date", str(future_date + datetime.timedelta(days=6)))
        else:
            query = query.replace("given date", str(future_date + datetime.timedelta(days=5-future_date.weekday())))
        output = output.replace("(x)", str(num_week))
    return query, output


while count < 300:
    output[count] = []
    populated_entities = []
    sql_template = "Select Max(point) from db4forecaststate where target_week_end_date = 'given date' and location_name = \"input\""
    rand_num = random.randint(1,3)
    if rand_num ==1:
        time_entity = 'in the next (x) days'
    else:
        time_entity = 'in the next (x) weeks'
    if(random.random()<0.025):
        state_name = 'United States'
        query = sql_template.replace("input", "National")
        query, time_e = queryEndDate(query, time_entity)
        real_question = question_template.replace("(Location Entity)", "United States")
        real_question = real_question.replace("(Time Entity)", time_e)
        populated_entities.append("United States")
        populated_entities.append(time_e)
    else: 
        location = random.choice(loc_entity)
        if location.find('(State)')>=0: 
            state_name = random.choice(data2['State'])
            query = sql_template.replace("input", state_name)
            query, time_e = queryEndDate(query, time_entity)
            loc = location.replace("(State)", state_name)
            real_question = question_template.replace("(Location Entity)", loc)
            real_question = real_question.replace("(Time Entity)", time_e)
            populated_entities.append(loc)
            populated_entities.append(time_e)
        elif location == '(State Abbreviation)':
            state_abbreviation = random.choice(data2['State Abbreviation'])
            state_name = state_dict[state_abbreviation]
            query = sql_template.replace("input", state_name)
            query, time_e = queryEndDate(query, time_entity)
            real_question = question_template.replace("(Location Entity)", state_abbreviation)
            real_question = real_question.replace("(Time Entity)", time_e)
            populated_entities.append(state_abbreviation)
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
        
            


    
    
    
