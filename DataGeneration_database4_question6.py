# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 20:21:08 2020

@author: Srikar Balusu
"""

import json
import pandas as pd
import numpy as np
import re
import random
import sqlite3
import time

import datetime

with open('lookup1.json') as json_file: 
    data = json.load(json_file)

with open('uniquelookup.json') as json_file:
    data2 = json.load(json_file)

with open('state_dict.json') as json_file:
    state_dict = json.load(json_file)

conn = sqlite3.connect('testQ.db')
c = conn.cursor()

question_template = 'What is the percentage change in (Mobility Entity) in (Location Entity) (Time Entity)?'
question_template_id = 'db4q6'
output = {}
entities = ['Mobility Entity', 'Location Entity', 'Time Entity']
question_key ={}

single_time_entity = ['on (month), (date)', 'today', 'yesterday', 'day before yesterday', 'as of (month), (date)','as of today', 'as of yesterday', 'as of last (day)', 'last (day)']
range_time_entity = ['in the last (x) weeks', 'in the last(x) months', 'in the last (x) days', 'since last (day)','in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month']

count = 1
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



def mobilityQuerySingle(mobility, query):
    if mobility == 'retail and recreation':
        query = query.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
    elif mobility == 'grocery and pharmacy':
        query = query.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
    elif mobility == 'parks':
        query = query.replace("(Mobility)", "parks_percent_change_from_baseline")
    elif mobility == 'transit stations':
        query = query.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
    elif mobility == 'workplaces':
        query = query.replace("(Mobility)", "workplaces_percent_change_from_baseline")
    else:
        query = query.replace("(Mobility)", "residential_percent_change_from_baseline")
    return query 
        

def timeQuerySingle(time_entity, query):
    output = time_entity
    if time_entity == 'yesterday' or time_entity == 'as of yesterday': 
      
        
        query = query.replace("given date", str(datetime.date.today()-datetime.timedelta(days=1)))
    elif time_entity == 'today' or time_entity == 'as of today': 
      
        query = query.replace("given date", str(datetime.date.today()))
    elif time_entity == 'day before yesterday': 
      
        query = query.replace("given date", str(datetime.date.today()-datetime.timedelta(days=2)))
    elif time_entity.find("last (day)") >=0: 
        chosen_date = random.choice(day)
      
      
        if chosen_date == 'Monday':
            today = datetime.date.today()
            if today.weekday() % 7 == 0:
                query = query.replace("given date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("given date", str(today-datetime.timedelta(days=today.weekday()%7)))
        elif chosen_date == 'Tuesday':
            today = datetime.date.today()
            offset = (today.weekday()-1)%7
            if offset == 0:
                query = query.replace("given date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("given date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Wednesday': 
            today = datetime.date.today()
            offset = (today.weekday()-2)%7
            if offset == 0:
                query = query.replace("given date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("given date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Thursday': 
            today = datetime.date.today()
            offset = (today.weekday()-3)%7
            if offset == 0:
                query = query.replace("given date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("given date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Friday': 
            today = datetime.date.today()
            offset = (today.weekday()-4)%7
            if offset == 0:
                query = query.replace("given date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("given date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Saturday': 
            today = datetime.date.today()
            offset = (today.weekday()-5)%7
            if offset == 0:
                query = query.replace("given date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("given date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Sunday': 
            today = datetime.date.today()
            offset = (today.weekday()-6)%7
            if offset == 0:
                query = query.replace("given date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("given date", str(today-datetime.timedelta(days=offset)))
        output = output.replace("(day)", chosen_date)
    else: 
        month = random.choice(data2['Month'])
        while month == 'September' or month == 'October' or month == 'November' or month == 'December':
            month = random.choice(data2['Month'])
        date = random.choice(data2['Day'])
        while date in day: 
            date = random.choice(data2['Day'])
        month_dict= {'January' : '01', 'February' : '02', 'March' : '03', 'April' : '04', 'May' : '05', 'June' : '06', 'July' : '07' , 'August' : '08', 'September' : '09', 'October' : '10', 'November' : '11', 'December' : '11'}
        month_num = month_dict[month]
        if len(date) == 3: 
            date_num = '0' + date[0]
        else:
            date_num = date[0] + date[1]
        query = query.replace("given date", '2020-'+month_num+'-'+date_num)
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
    return query, output
                

while count < 200:
    output[count] = []
    populated_entities = []
    mobility = random.choice(data['Mobility Entity'])
    location = random.choice(data['Location Entity'])
    if random.random()<0.2: 
        isNull = True
    else:
        isNull = False
    while location.find('Country') >= 0 or location.find('Province') >= 0 or location.find('(') < 0: 
        location = random.choice(data['Location Entity'])
    if location == 'in the state of (State)': 
        location = 'the state of (State)'
    entity = re.findall('\(([^)]+)', location)
    sql_template = "Select (Mobility) FROM db4mobility WHERE date = \"given date\" AND country_region = \"United States\" AND sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\""
    query = ""
    if len(entity) ==1:
        if entity[0] == 'State':
            state_name = random.choice(data2['State'])
            while state_name == 'Guam' or state_name == 'Virgin Islands' or state_name == 'Diamond Princess' or state_name == 'Northern Mariana Islands':
                state_name = random.choice(data2['State'])
            query = sql_template.replace("State name", state_name)
            query = mobilityQuerySingle(mobility,query)
            time_entity = random.choice(single_time_entity)
            if isNull:
                query, time_e = timeQuerySingle('today', query)
                time_e = 'Null'
            else:
                query, time_e = timeQuerySingle(time_entity, query)
            loc = location.replace("(State)", state_name)
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
            if isNull:
                real_question = real_question.replace(" (Time Entity)", "")
            else:
                real_question = real_question.replace("(Time Entity)", time_e)
            
        else: 
            state_abbreviation = random.choice(data2['State Abbreviation'])
            while state_abbreviation  == 'PR' or state_abbreviation == 'GU' or state_abbreviation == 'VI':
                state_abbreviation = random.choice(data2['State Abbreviation'])
            state_name = state_dict[state_abbreviation]
            query = sql_template.replace("State name", state_name)
            query = mobilityQuerySingle(mobility, query)
            time_entity = random.choice(single_time_entity)
            if isNull:
                query, time_e = timeQuerySingle('today', query)
                time_e = 'Null'
            else:
                query, time_e = timeQuerySingle(time_entity, query)
            loc = location.replace("(State Abbreviation)", state_abbreviation)
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
            if isNull:
                real_question = real_question.replace(" (Time Entity)", "")
            else:
                real_question = real_question.replace("(Time Entity)", time_e)
            
    else: 
        if entity[1] == 'State':
            county_list = random.choice(data2['County']).split(', ')
            county_name = county_list[0]
            state_name = county_list[1]
            loc = location.replace("(County)", county_name)
            loc = loc.replace("(State)", state_name)
            query = sql_template.replace("State name", state_name + "\" AND sub_region_2 = \"" + county_name+ " County")
            query = mobilityQuerySingle(mobility,query)
            
            time_entity = random.choice(single_time_entity)
            if isNull:
                query, time_e = timeQuerySingle('today', query)
                time_e = 'Null'
            else:
                query, time_e = timeQuerySingle(time_entity, query)
            query = query.replace("and iso_3166_2_code LIKE \"US-%\"", "")
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
            if isNull:
                real_question = real_question.replace(" (Time Entity)", "")
            else:
                real_question = real_question.replace("(Time Entity)", time_e)
            
          
        else:
            county_list = random.choice(data2['County']).split(', ')
            county_name = county_list[0]
            state_name = county_list[1]
            key_list = list(state_dict.keys())
            val_list = list(state_dict.values())
            state_abbreviation = key_list[val_list.index(state_name)]
            loc = location.replace("(County)", county_name)
            loc = loc.replace("(State Abbreviation)", state_abbreviation)
            query = sql_template.replace("State name", state_name + "\" AND sub_region_2 = \"" + county_name+ " County")
            query = mobilityQuerySingle(mobility,query)
            time_entity = random.choice(single_time_entity)
            if isNull:
                query, time_e = timeQuerySingle('today', query)
                time_e = 'Null'
            else:
                query, time_e = timeQuerySingle(time_entity, query)
            query = query.replace("and iso_3166_2_code LIKE \"US-%\"", "")
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
            if isNull:
                real_question = real_question.replace(" (Time Entity)", "")
            else:
                real_question = real_question.replace("(Time Entity)", time_e)
    populated_entities.append(mobility)
    populated_entities.append(loc)
    populated_entities.append(time_e)
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
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 4'})
        print(count)
        print(real_question)
        print(query)
        print(result)
        count = count + 1
        