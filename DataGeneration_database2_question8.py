# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 05:47:12 2020

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
question_template = "How many (Race Entity) (Case Entity) occurred in (State Entity) (Time Entity)?"
question_template_id = 'db2q8'
output = {}
question_key = {}
entities = ['Race Entity', 'Case Entity', 'State Entity', 'Time Entity']
case_entity_list = ['confirmed cases', 'cases', 'deaths', 'confirmed cases increased', 'cases increased', 'deaths increased']
single_time_entity_total = ['as of yesterday', 'as of day before yesterday', 'as of today', 'as of (month), (date)', 'as of last (day)', 'up till yesterday', 'up till today', 'up till day before yesterday', 'up till last (day)', 'up till (month), (date)']
range_time_entity_total = ['today', 'yesterday', 'day before yesterday', 'last (day)', 'on (month), (date)', 'in the last (x) weeks', 'in the last (x) days)', 'since last (day)', 'in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month', 'since the last (x) days']
range_time_entity = ['in the last (x) weeks', 'in the last (x) months', 'in the last (x) days', 'since last (day)','in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month', 'since the last (x) days']
month_day_dict = {'January' : 30, 'February' : 29, 'March' : 31, 'April' : 30, 'May' : 31, 'June' : 30, 'July' :31, 'August' : 31, 'September' : 30, 'October' : 31, 'November' : 30, 'December' : 31}
month_dict= {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7 , 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
day_map = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6}
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
location_entity_list = ['(State)', 'the state of (State)', '(State Abbreviation)']
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
    elif race_entity == '(race) only':
        specific_race = random.choice(data2['Race'])
        race_input = genRaceInput(specific_race)
    elif race_entity == '(race) people':
        specific_race = random.choice(data2['Race'])
        race_input = genRaceInput(specific_race)
        output = output.replace("(race)", specific_race)
    elif race_entity == '(race)':
        specific_race = random.choice(data2['Race'])
        race_input = genRaceInput(specific_race)
    output = output.replace("(race)", specific_race)
    query = query.replace("Race Entity Column",race_input)
    return query, output
def timeTotalQuerySingle(query, time_entity):
    output = time_entity
    if time_entity.find('today')>=0: 
        date1 = datetime.date.today()
    elif time_entity.find('yesterday')>=0 and time_entity.find("day before yesterday") <0:
        date1 = datetime.date.today() - datetime.timedelta(days=1)
    elif time_entity.find('day before yesterday') >=0: 
        date1 = datetime.date.today() - datetime.timedelta(days=2)
    elif time_entity.find('last (day)') >=0:
        chosen_date = random.choice(day)
        today = datetime.date.today()
        offset = (today.weekday() - day_map[chosen_date]) %7
        if offset == 0: 
            date1 = (today-datetime.timedelta(days=7))
           
        else: 
            date1 =(today-datetime.timedelta(days=offset))
        output = output.replace("(day)", chosen_date)
    else:
        month = random.choice(data2['Month'])
        date = random.choice(data2['Day'])
        
        while date in day: 
            date = random.choice(data2['Day'])
        if len(date) == 3: 
            date_num = date[0]
                            
        else:
            date_num = date[0:2]
        
        while int(date_num) > month_day_dict[month]:
            date = random.choice(data2['Day'])
            while date in day: 
                date = random.choice(data2['Day'])
            if len(date) == 3: 
                date_num = date[0]
            else:
                date_num = date[0] + date[1]
        date1 = datetime.date(2020, month_dict[month], int(date_num))
     
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
    if date1.weekday() == 1 or date1.weekday() == 0:
        final = date1-datetime.timedelta(days=date1.weekday()+1)
    elif date1.weekday() == 6 or date1.weekday() == 2:
        final = date1
    else:
        final = date1 - datetime.timedelta(days=date1.weekday()-2)
    query = query.replace('Time Entity', str(final).replace("-", ""))
    return query, output
def timeTotalQueryRange(query, time_entity):
    output = time_entity
    if time_entity == 'today': 
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=1)
    elif time_entity == 'yesterday':
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        start_date = end_date - datetime.timedelta(days=1)
    elif time_entity == 'day before yesterday':
        end_date = datetime.date.today() - datetime.timedelta(days=2)
        start_date = end_date - datetime.timedelta(days=1)
    elif time_entity == 'last (day)': 
        chosen_date = random.choice(day)
        today = datetime.date.today()
        offset = (today.weekday()-day_map[chosen_date])%7
        if offset == 0:
            end_date = today-datetime.timedelta(days =7)
        else: 
            end_date = today-datetime.timedelta(days=offset)
        start_date = end_date - datetime.timedelta(days = 1)
        output = output.replace("(day)", chosen_date)
    elif time_entity == 'on (month), (date)': 
        month = random.choice(data2['Month'])
        date = random.choice(data2['Day'])
        while date in day:
            date = random.choice(data2['Day'])
        if len(date) == 3: 
            date_num = date[0]
        else:
            date_num = date[0:2]
        
        while int(date_num) > month_day_dict[month]:
            date = random.choice(data2['Day'])
            while date in day: 
                date = random.choice(data2['Day'])
            if len(date) == 3: 
                date_num = date[0]
            else:
                date_num = date[0] + date[1]
        end_date = datetime.date(2020, month_dict[month], int(date_num))
    
        start_date = end_date - datetime.timedelta(days=1)
        ###start_date = end_date - datetime.timedelta(days=1)
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
        
    elif time_entity == 'in the month of (month)' or time_entity == 'in (month)':
        month = random.choice(data2['Month'])
        year = 2020
        month_num = month_dict[month]
        start_date = datetime.date(year, month_num, 1)
        end_date = datetime.date(year, month_num, calendar.monthrange(year,month_num)[1])
        output = output.replace("(month)", month)
    elif time_entity == 'since last (day)':
        chosen_date = random.choice(day)
        today = datetime.date.today()
        offset = (today.weekday()-day_map[chosen_date])%7
        if offset == 0:
            start_date = today-datetime.timedelta(days =7)
        else: 
            start_date = today-datetime.timedelta(days=offset)
        end_date = today
        output = output.replace("(day)", chosen_date)
    elif time_entity == 'since last week' or time_entity == 'since last month':
        if time_entity == 'since last month':
            end_date = datetime.date.today()
            start_date = datetime.date.today() - relativedelta(months=1)
        else:
            end_date = datetime.date.today()
            start_date = datetime.date.today() - datetime.timedelta(days=7)
    else:
        if time_entity.find('months') >=0: 
            num_month = random.randint(1,5)
            end_date = datetime.date.today()
            start_date = end_date - relativedelta(months=num_month)
            output = output.replace("(x)", str(num_month))
        elif time_entity.find('days') >=0: 
            num_days = random.randint(1,30)
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=num_days)
            output = output.replace("(x)", str(num_days))

        else:
            num_weeks = random.randint(1,10)
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=7*num_weeks)
            output = output.replace("(x)", str(num_weeks))
    if end_date.weekday() == 1 or end_date.weekday() == 0:
        final = end_date-datetime.timedelta(days=end_date.weekday()+1)
    elif end_date.weekday() == 6 or end_date.weekday() == 2:
        final = end_date
    else:
        final = end_date - datetime.timedelta(days=end_date.weekday()-2)
    if start_date.weekday() == 1 or start_date.weekday() == 0:
        final2 = start_date-datetime.timedelta(days=start_date.weekday()+1)
    elif start_date.weekday() == 6 or start_date.weekday() == 2:
        final2 = start_date
    else:
        final2 = start_date - datetime.timedelta(days=start_date.weekday()-2)
    query = query.replace("Time Entity", str(final).replace("-", ""),1)
    query = query.replace("Time Entity", str(final2).replace("-", ""),1)
    return query, output
while count <300:
    output[count] = []
    populated_entities = []
    isNull = False
    race_entity = random.choice(data['Race'])
    while race_entity == 'mixed' or race_entity == 'multiracial' or race_entity.find("people") >=0:
        race_entity = random.choice(data['Race'])
    location = random.choice(location_entity_list)
    case_entity = random.choice(case_entity_list)
    if case_entity.find("increased") <0:
        sql_template = "Select Case Entity Column_Race Entity Column from db2race where date = 'Time Entity' and state = \"State Entity\" "
        time_entity = random.choice(single_time_entity_total)
        if location.find("(State)") >=0:
            state_name = random.choice(data2['State'])
            while state_name == 'Diamond Princess':
                state_name = random.choice(data2['State'])
            key_list = list(state_dict.keys())
            val_list = list(state_dict.values())
            state_abbreviation = key_list[val_list.index(state_name)]
            query = sql_template.replace("State Entity", state_abbreviation)
            loc = location.replace("(State)", state_name)
        else:
            state_abbreviation = random.choice(data2['State Abbreviation'])
            query = sql_template.replace("State Entity", state_abbreviation)
            loc = location.replace("(State Abbreviation)", state_abbreviation)
        query, race_e = raceQuery(query, race_entity)
        if random.random()<0.2:
            isNull = True
        else:
            isNull = False
        if isNull:
            query, time_e = timeTotalQuerySingle(query, 'today')
            time_e = 'Null'
        else:
            query, time_e = timeTotalQuerySingle(query, time_entity)
    else: 
        sql_template = "Select(Select Case Entity Column_Race Entity Column from db2race where date = 'Time Entity' and state = \"State Entity\") - (Select Case Entity Column_Race Entity Column from db2race where date = 'Time Entity' and state = \"State Entity\") "
        time_entity = random.choice(range_time_entity_total)
        if location.find("(State)") >=0:
            state_name = random.choice(data2['State'])
            while state_name == 'Diamond Princess':
                state_name = random.choice(data2['State'])
            key_list = list(state_dict.keys())
            val_list = list(state_dict.values())
            state_abbreviation = key_list[val_list.index(state_name)]
            query = sql_template.replace("State Entity", state_abbreviation)
            loc = location.replace("(State)", state_name)
        else:
            state_abbreviation = random.choice(data2['State Abbreviation'])
            query = sql_template.replace("State Entity", state_abbreviation)
            loc = location.replace("(State Abbreviation)", state_abbreviation)
        query, race_e = raceQuery(query, race_entity)
        query, time_e = timeTotalQueryRange(query,time_entity)
    if case_entity.find("cases")>=0:
        query = query.replace("Case Entity Column", "Cases")
    else:
        query = query.replace("Case Entity Column", "Deaths")
    real_question = question_template.replace("(Case Entity)", case_entity)
    real_question = real_question.replace("(Race Entity)", race_e)
    real_question = real_question.replace("(State Entity)", loc)
    populated_entities.append(race_e)
    populated_entities.append(case_entity)
    populated_entities.append(loc)
    populated_entities.append(time_e)
    if isNull:
        real_question = real_question.replace(" (Time Entity)", "")
    else:
        real_question = real_question.replace("(Time Entity)", time_e)
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

with open('db2q8data.json', 'w') as outfile: 
    json.dump(output,outfile)
    
print("done")