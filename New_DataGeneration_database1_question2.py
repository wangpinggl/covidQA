# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 00:22:48 2020

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


single_time_entity_total = ['as of yesterday', 'as of day before yesterday', 'as of today', 'as of (month), (date)', 'as of last (day)', 'up till yesterday', 'up till today', 'up till day before yesterday', 'up till last (day)', 'up till (month), (date)'] 
rate_entity_list = ['incidence rate', 'case-fatality rate', 'recovery rate', 'testing rate']
question_template_id = 'db1q2'
output = {}
month_day_dict = {'January' : 30, 'February' : 29, 'March' : 31, 'April' : 30, 'May' : 31, 'June' : 30, 'July' :31, 'August' : 31, 'September' : 30, 'October' : 31, 'November' : 30, 'December' : 31}
month_dict= {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7 , 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
day_map = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6}
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
count = 1
question_key = {}

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

    query = query.replace('given date', str(date1.strftime("%m-%d-%Y")))
    return query, output

def locationQuery(location, query, real_question, sql_template):
    """if location == 'globally' or location == 'in the world/around the world': 
        query = query.replace("and (Location)", "")
        if location == 'in the world/around the world':
            real_question = real_question.replace("(Location Entity)", 'the world', 1)
        else:
            real_question = real_question.replace("in (Location Entity)", "globally", 1)"""
    
    if location == '(State)' or location == '(State Abbreviation)' or location == '(State), (Country)' or location == 'in the state of (State)':
        sql_template = sql_template.replace("db1global", 'db1state')
        query = query.replace("db1global", 'db1state')
        if location == '(State)' or location == 'in the state of (State)': 
            state_name = random.choice(data2['State'])
            query = query.replace("(Location)", "Province_State = \"" + state_name + "\"")
            loc = location.replace("(State)", state_name)
            if location == 'in the state of (State)':
                loc = loc.replace("in ", "")
        elif location == '(State Abbreviation)': 
            state_abbreviation = random.choice(data2['State Abbreviation'])
            state_name = state_dict[state_abbreviation]
            query = query.replace("(Location)", "Province_State = \"" +state_name + "\"")
            loc = location.replace("(State Abbreviation)", state_abbreviation)
        else:
            state_name = random.choice(data2['State'])
            query = query.replace("(Location)", "Province_State = \"" + state_name + "\"")
            loc = location.replace("(State)", state_name)
            loc = loc.replace("(Country)", 'United States')
        real_question = real_question.replace("(Location Entity)", loc, 1)
        question_template = 'What is the (Rate Entity) in (State Entity) (Time Entity)?'
        entities = ['Rate Entity', 'State Entity', 'Time Entity']
        location_entity = [state_name]
    elif location == '(Province)' or location == '(Province), (Country)' or location == '(Province) in (Country)': 
        if location == '(Province)':
            province = random.choice(data2['Province'])
            while province.find("US") >=0:
                province = random.choice(data2['Province'])
            province_list = province.split(', ')
            province_name = province_list[0]
            country_name = province_list[1]
            query = query.replace("(Location)",  "Province_State = \"" +province_name + "\" and Country_Region = \"" + country_name + "\" ")
            loc = location.replace("(Province)", province_name)
        else: 
            province = random.choice(data2['Province'])
            while province.find("US") >=0:
                province = random.choice(data2['Province'])
            province_list = province.split(', ')
            province_name = province_list[0]
            country_name = province_list[1]
            query = query.replace("(Location)", "Province_State = \"" + province_name + "\" and Country_Region = \"" + country_name + "\" ")
            loc = location.replace("(Province)", province_name)
            loc = loc.replace("(Country)", country_name)
        real_question = real_question.replace("(Location Entity)", loc, 1)
        question_template = 'What is the (Rate Entity) in (Province Entity) (Country Entity) (Time Entity)?'
        entities = ['Rate Entity', 'Province Entity', 'Country Entity', 'Time Entity']
        location_entity = [province_name, country_name]
    elif location == '(County) in (State)' or location == '(County), (State)' or location == '(County), (State Abbreviation)':
        if location.find("State Abbreviation") <0:
            county_list = random.choice(data2['County']).split(', ')
            county_name = county_list[0]
            state_name = county_list[1]
            query = query.replace("(Location)", "Province_State = \"" + state_name + "\" and Admin2 = \"" + county_name + "\" ")
            loc = location.replace("(County)", county_name)
            loc = loc.replace("(State)", state_name)
        else: 
            county_list = random.choice(data2['County']).split(', ')
            county_name = county_list[0]
            state_name = county_list[1]
            key_list = list(state_dict.keys())
            val_list = list(state_dict.values())
            state_abbreviation = key_list[val_list.index(state_name)]
            query = query.replace("(Location)", "Province_State = \"" + state_name + "\" and Admin2 = \"" + county_name + "\" ")
            loc = location.replace("(County)", county_name)
            loc = loc.replace("(State Abbreviation)", state_abbreviation)
        real_question = real_question.replace("(Location Entity)", loc, 1)
        question_template = 'What is the (Rate Entity) in (County Entity) (State Entity) (Time Entity)?'
        entities = ['Rate Entity', 'County Entity','State Entity', 'Time Entity']
        location_entity = [county_name, state_name]
    elif location == '(Country)' or location == 'the country of (Country)': 
        country = random.choice(data2['Country'])
        if country == 'United States':
            query = query.replace("(Location)", "Country_Region = 'US' ")
        else: 
            query = query.replace("(Location)", "Country_Region = \"" + country + "\" ")
        loc = location.replace("(Country)", country)
        real_question = real_question.replace("(Location Entity)", loc, 1)
        question_template = 'What is the (Rate Entity) in (Country Entity) (Time Entity)?'
        entities = ['Rate Entity', 'Country Entity', 'Time Entity']
        location_entity = [country]
    return query, real_question, sql_template, question_template, entities, location_entity

while count <300:
    output[count] = []
    populated_entities = []
    question_template = "What is the (Rate Entity) in (Location Entity) (Time Entity)?"
    rate_entity = random.choice(rate_entity_list)
    time_entity = random.choice(single_time_entity_total)
    real_question = question_template 
    sql_template = "Select (Rate) * 100000 from db1global where date = 'given date' and (Location)"
    if rate_entity == 'incidence rate':
        location = random.choice(data['Location Entity'])
        while location == 'state' or location == 'county' or location == 'country' or location == 'province' or location == 'globally' or location == 'in the world/around the world':
            location = random.choice(data['Location Entity'])
        query = "Select SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000 from db1global where date = 'given date' and (Location)"
    elif rate_entity == 'case-fatality rate': 
        location = random.choice(data['Location Entity'])
        while location == 'state' or location == 'county' or location == 'country' or location == 'province' or location == 'globally' or location == 'in the world/around the world':
            location = random.choice(data['Location Entity'])
        query = "Select SUM(Deaths)*100.0/SUM(Confirmed) from db1global where date = 'given date' and (Location)" 
    elif rate_entity == 'recovery rate':
        location = random.choice(data['Location Entity'])
        while location == 'state' or location == 'county' or location == 'country' or location == 'province' or location == 'globally' or location == 'in the world/around the world':
            location = random.choice(data['Location Entity'])
        query = "Select SUM(Recovered)*100.0./SUM(Confirmed) from db1global where date = 'given date' and (Location)"
    else:
        location = random.choice(data['Location Entity'])
        while (location != '(State)' and location != "(State), (Country)" and location != "(State Abbreviation)" and location != "in the state of (State)"):
            location = random.choice(data['Location Entity'])
        query = "Select Testing_Rate from db1global where date = 'given date and (Location)"
    
    query, time_e = timeTotalQuerySingle(query, time_entity)
    print(location)
    query, real_question, sql_template, question_template, entities, location_entity= locationQuery(location, query, real_question, sql_template)
    real_question = real_question.replace("(Rate Entity)", rate_entity)
    real_question = real_question.replace("(Time Entity)", time_e)
    populated_entities.append(rate_entity)
    for i in range(len(location_entity)): 
        populated_entities.append(location_entity[i])
    populated_entities.append(time_e)
    if real_question in question_key.keys():
        continue
    else:
        question_key[real_question] = True
        output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
                 'entities' : entities, 'question' : real_question, 
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 4'})
        print(count)
        print(question_template)
        print(sql_template)
        print(real_question)
        print(entities)
        print(populated_entities)
        count = count + 1
        
#with open('db1q2data.json', 'w') as outfile: 
#    json.dump(output,outfile)
#print("done")