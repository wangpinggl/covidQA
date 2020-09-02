# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 04:43:44 2020

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
question_template = "What percentage of (Case Entity) in (Location Entity) are from (Race Entity)?"
question_template_id = 'db2q6'
output = {}
entities = ['Case Entity', 'Location Entity', 'Race Entity']
case_entity_list = ['confirmed cases', 'cases', 'deaths']
location_entity_list = ['(State)', "(State Abbreviation)", 'the state of (State)']
count = 1
question_key = {}

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
    location = random.choice(location_entity_list)
    sql_template = "Select (Case)_(Race) from db2race where date = 'given date' and state = \"State Name\" " 
    race_entity = random.choice(data['Race'])
    case_entity = random.choice(case_entity_list)
    while race_entity == 'mixed' or race_entity =='multiracial':
        race_entity  = random.choice(data['Race'])
    
    if location.find("(State)") >= 0: 
        state_name = random.choice(data2['State'])
        while state_name == 'Diamond Princess':
            state_name = random.choice(data2['State'])
        key_list = list(state_dict.keys())
        val_list = list(state_dict.values())
        state_abbreviation = key_list[val_list.index(state_name)]
        query = sql_template.replace("State Name", state_abbreviation)
        query, race_e = raceQuery(query, race_entity)
        loc = location.replace("(State)", state_name)
    else:
        state_abbreviation = random.choice(data2['State Abbreviation'])
        query = sql_template.replace("State Name", state_abbreviation)
        query, race_e = raceQuery(query,race_entity)
        loc = location.replace("(State Abbreviation)", state_abbreviation)
    if case_entity.find("cases") >=0: 
        query = query.replace("(Case)", 'Cases')
    else:
        query = query.replace("(Case)", "Deaths")
    today = datetime.date.today()-datetime.timedelta(days=2)
    if today.weekday() == 1 or today.weekday() == 0:
        date = today-datetime.timedelta(days=today.weekday()+1)
    elif today.weekday() == 6 or today.weekday() == 2:
        date = today
    else:
        date = today - datetime.timedelta(days=today.weekday()-2)
    query = query.replace('given date', str(date).replace("-", ""))
    real_question = question_template.replace("(Location Entity)", loc)
    real_question = real_question.replace("(Case Entity)", case_entity)
    real_question = real_question.replace("(Race Entity)", race_e)
    populated_entities.append(case_entity)
    populated_entities.append(loc)
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