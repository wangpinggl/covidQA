# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 00:17:48 2020

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
    
question_template = 'What state has the (Value Entity) (Rate Entity)'

question_template_id = 'db2q9' 
output = {}
question_key = {}
entities = ['Value Entity', 'Rate Entity']
rate_entity_list = ['daily percent positive rate', 'daily percent negative rate', 'percent positive rate', 'percent negative rate', 'hospitilization rate']
count = 1


def rateQuery(query, rate_entity):
    date = datetime.date.today()-datetime.timedelta(days=1)
    date = str(date)
    date = date.replace("-", "")
    if rate_entity == 'daily percent positive rate':
        query = query.replace("Rate", "positiveIncrease * 100.0 /totalTestResultsIncrease")
        query = query.replace("(Null)", "positiveIncrease is not null and totalTestResultsIncrease is not null")
    elif rate_entity == 'daily percent negative rate':
        query = query.replace("Rate", "negativeIncrease *100.0/totalTestResultsIncrease")
        query = query.replace("(Null)", "negativeIncrease is not null and totalTestResultsIncrease is not null")
    elif rate_entity == 'percent positive rate':
        query = query.replace("Rate", "positive *100.0/totalTestResults")
        query = query.replace("(Null)", "positive is not null and totalTestResults is not null")
    elif rate_entity == 'percent negative rate':
        query = query.replace("Rate", "negative * 100.0/totalTestResults")
        query = query.replace("(Null)", "negative is not null and totalTestResults is not null")
    else:
        query = query.replace("Rate", "hospitalizedCumulative * 100.0/positive")
        query = query.replace("(Null)", "hospitalizedCumulative is not null and positive is not null")
    query = query.replace("current date", date)
    return query
while count <110: 
    output[count] = []
    populated_entities = []
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
    rate_entity = random.choice(rate_entity_list)
    sql_template = "Select state from db2state where date = 'current date' and (Null) order by Rate asc/desc limit X,1"
    query = sql_template
    if ascending == False:
        query = query.replace('asc/desc','desc')
        query = query.replace('X', str(order-1))
    else:
        query = query.replace('asc/desc','asc')
        query = query.replace('X', str(order-1))
    query = rateQuery(query, rate_entity)
    real_question =  question_template.replace("(Rate Entity)", rate_entity)
    real_question = real_question.replace("(Value Entity)", val)
    populated_entities.append(val)
    populated_entities.append(rate_entity)
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
    
        count = count +1