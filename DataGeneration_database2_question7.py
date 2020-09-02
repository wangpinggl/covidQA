# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 05:32:13 2020

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
question_key = {}
question_template = "What state has the (Value Entity) percentage of (Case Entity) from (Race Entity)?"
question_template_id = 'db2q7'
output = {}
entities = ['Value Entity', 'Case Entity', 'Race Entity']
case_entity_list = ['confirmed cases', 'cases', 'deaths']
count = 1
def genRaceInput(specific_race):
    if specific_race == 'African-Americans' or specific_race == 'Black': 
        race_input = 'Black'
    elif specific_race == 'Asian':
        race_input = 'Asian'
    elif specific_race == 'White' or specific_race == 'Caucasian':
        race_input = 'White'
    elif specific_race == 'American Indian' or specific_race == 'Alaska Native' or specific_race == 'American Indian or Alaska Native':
        race_input = 'AIAN'
    elif specific_race == 'Pacific Islander' or specific_race == 'Native Hawaiian' or specific_race == 'Pacific Islander and Native Hawaiian': 
        race_input = 'NHPI'
    elif specific_race == 'multiracial' or specific_race == 'mixed':
        race_input = 'Multiracial'
    else:
        race_input = 'LatinX'
    return race_input
def raceQuery(query, race_entity):
    output = race_entity
    if race_entity == 'people of color':
        race_input = 'Black'
    elif race_entity == 'people of mixed color' or race_entity == 'people of two or more races':
        race_input = 'Multiracial'
    elif race_entity.find('Non-Hispanic') >=0:
        specific_race = random.choice(data2['Race'])
        while specific_race == 'multiracial' or specific_race == 'mixed' or specific_race == 'Latino' or specific_race == 'Hispanic':
            specific_race = random.choice(data2['Race'])
        race_input = genRaceInput(specific_race)
        if specific_race == 'Pacific Islander and Native Hawaiian':
            output = output.replace("(race)", 'Pacific Islanders and Native Hawaiians')
        elif specific_race == 'American Indian or Alaska Native':
            output = output.replace("(race)", 'American Indians or Alaska Natives')
        else:
            output = output.replace("(race)", specific_race + 's')
    elif race_entity == '(race) only':
        specific_race = random.choice(data2['Race'])
        race_input = genRaceInput(specific_race)
        if specific_race == 'Pacific Islander and Native Hawaiian':
            output = output.replace("(race)", 'Pacific Islanders and Native Hawaiians')
        elif specific_race == 'American Indian or Alaska Native':
            output = output.replace("(race)", 'American Indians or Alaska Natives')
        else:
            output = output.replace("(race)", specific_race + 's')
    elif race_entity == '(race) people':
        specific_race = random.choice(data2['Race'])
        race_input = genRaceInput(specific_race)
        output = output.replace("(race)", specific_race)
    elif race_entity == '(race)':
        specific_race = random.choice(data2['Race'])
        race_input = genRaceInput(specific_race)
        if specific_race == 'Pacific Islander and Native Hawaiian':
            output = output.replace("(race)", 'Pacific Islanders and Native Hawaiians')
        elif specific_race == 'American Indian or Alaska Native':
            output = output.replace("(race)", 'American Indians or Alaska Natives')
        else:
            output = output.replace("(race)", specific_race + 's')
    query = query.replace("(Race)",race_input)
    return query, output

while count < 300: 
    output[count] = []
    populated_entities = []
    sql_template = "Select state from db2race where date = 'given date' and (Case)_(Race) is not null order by (Case)_(Race) asc/desc limit (X),1"
    race_entity = random.choice(data['Race'])
    case_entity = random.choice(case_entity_list)
    while race_entity == 'mixed' or race_entity =='multiracial':
        race_entity  = random.choice(data['Race'])
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
    if case_entity.find('cases')>=0: 
        query = sql_template.replace("(Case)", "Cases")
    else:
        query = sql_template.replace("(Case)", "Deaths")
    query, race_e = raceQuery(query, race_entity)
    if ascending == False:
        query = query.replace('asc/desc','desc')
        query = query.replace('(X)', str(order-1))
    else:
        query = query.replace('asc/desc','asc')
        query = query.replace('(X)', str(order-1))
    today = datetime.date.today() - datetime.timedelta(days=2)
    if today.weekday() == 1 or today.weekday() == 0:
        date = today-datetime.timedelta(days=today.weekday()+1)
    elif today.weekday() == 6 or today.weekday() == 2:
        date = today
    else:
        date = today - datetime.timedelta(days=today.weekday()-2)
    query = query.replace('given date', str(date).replace("-", ""))
    real_question = question_template.replace("(Value Entity)", val)
    real_question = real_question.replace("(Race Entity)", race_e)
    real_question = real_question.replace("(Case Entity)", case_entity)
    populated_entities.append(val)
    populated_entities.append(case_entity)
    populated_entities.append(race_e)
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

