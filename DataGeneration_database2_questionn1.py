# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 23:08:06 2020

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
question_template = 'What is the (Rate Entity) in (Location Entity)?'
question_template_id = 'db2q1'
output = {}
question_key = {}
location_entity_list = ['(State)', '(State Abbreviation)', 'the state of (State)']
rate_entity_list = ['daily percent positive rate', 'daily percent negative rate', 'percent positive rate', 'percent negative rate', 'hospitilization rate']
count = 1
entities = ['Rate Entity', 'Location Entity']

def rateQuery(query, rate_entity):
    date = datetime.date.today()-datetime.timedelta(days=1)
    date = str(date)
    date = date.replace("-", "")
    if rate_entity == 'daily percent positive rate':
        query = query.replace("Rate", "positiveIncrease * 100.0 /totalTestResultsIncrease")
    elif rate_entity == 'daily percent negative rate': 
        query = query.replace("Rate", "negativeIncrease * 100.0/totalTestResultsIncrease")
    elif rate_entity == 'percent positive rate':
        query = query.replace("Rate", "positive * 100.0/totalTestResults")
    elif rate_entity == 'percent negative rate':
        query = query.replace("Rate", "negative * 100.0/totalTestResults")
    else:
        query = query.replace("Rate", "hospitalizedCumulative * 100.0/positive")
    query = query.replace('current date', date)
    return query
while count <300:
    output[count] = []
    populated_entities = []
    
    rand_num = random.random()
    rate_entity = random.choice(rate_entity_list)
    if rand_num <0.025:
        location = 'United States' 
        sql_template = "Select Rate from db2US where date = 'current date'" 
        query = sql_template
        query = rateQuery(query, rate_entity)
        real_question = question_template.replace("(Location Entity)", location)
        real_question = real_question.replace("(Rate Entity)", rate_entity)
        populated_entities.append(rate_entity)
        populated_entities.append(location)
    else: 
        location = random.choice(location_entity_list)
        sql_template = "Select Rate from db2State where date = 'current date' and state = \"State Name\" "
        if location.find("(State)")>=0:
            state_name = random.choice(data2['State'])
            while state_name == 'Diamond Princess':
                state_name = random.choice(data2['State'])
            key_list = list(state_dict.keys())
            val_list = list(state_dict.values())
            state_abbreviation = key_list[val_list.index(state_name)]
            query = sql_template.replace("State Name", state_abbreviation)
            query = rateQuery(query, rate_entity)
            loc = location.replace("(State)", state_name)
            real_question = question_template.replace("(Location Entity)", loc)
            real_question = real_question.replace("(Rate Entity)", rate_entity)
        else:
            state_abbreviation = random.choice(data2['State Abbreviation'])
            query = sql_template.replace("State Name", state_abbreviation)
            query = rateQuery(query, rate_entity)
            loc = location.replace("(State Abbreviation)", state_abbreviation)
            real_question = question_template.replace("(Location Entity)", loc)
            real_question = real_question.replace("(Rate Entity)", rate_entity)
        populated_entities.append(rate_entity)
        populated_entities.append(loc)
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
        print(real_question)
        print(query)
        print(result)
        count = count+1
    
    

    