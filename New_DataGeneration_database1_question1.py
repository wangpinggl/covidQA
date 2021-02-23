# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 00:22:43 2020

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

question_key = {}   
case_entity_list = ['confirmed cases', 'deaths', 'cases', 'daily cases', 'active cases', 'recovered cases', 'new cases', 'confirmed cases increased', 'cases increased', 'active cases incresased', 'deaths increased', 'recovered cases increased']
single_time_entity_total = ['as of yesterday', 'as of day before yesterday', 'as of today', 'as of (month), (date)', 'as of last (day)', 'up till yesterday', 'up till today', 'up till day before yesterday', 'up till last (day)', 'up till (month), (date)'] 
range_time_entity_total = ['today', 'yesterday', 'day before yesterday', 'last (day)', 'on (month), (date)', 'in the last (x) weeks', 'in the last (x) days)', 'since last (day)', 'in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month', 'since the last (x) days']
single_time_entity_daily = ['today', 'yesterday', 'last (day)', 'on (month), (date)', 'day before yesterday']
question_template = 'How many (Case Entity) occurred in (Location Entity) (Time Entity)?'
question_template_id = 'db1q1'
output = {}
month_day_dict = {'January' : 30, 'February' : 29, 'March' : 31, 'April' : 30, 'May' : 31, 'June' : 30, 'July' :31, 'August' : 31, 'September' : 30, 'October' : 31, 'November' : 30, 'December' : 31}
month_dict= {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7 , 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
day_map = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6}
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
count = 1


def caseQuery(case_entity, query):
    if case_entity == 'confirmed cases' or case_entity == 'cases' or case_entity == 'cases increased' or case_entity == 'confirmed cases increased':
        query = query.replace("Cases", "Confirmed")
    elif case_entity == 'daily cases' or case_entity == 'new cases': 
        query = query.replace("Cases", 'Confirmed')
    elif case_entity == 'deaths' or case_entity == 'deaths increased':
        query = query.replace("Cases", "Deaths")
    elif case_entity == 'active cases' or case_entity == 'active cases increased': 
        query = query.replace("Cases", "Active")
    elif case_entity == 'recovered cases' or case_entity == 'recovered cases increased': 
        query = query.replace("Cases", "Recovered")
    return query


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
    
    query = query.replace("end date", str(end_date.strftime("%m-%d-%Y")))
    query = query.replace("start date", str(start_date.strftime("%m-%d-%Y")))
    return query, output
    
while count <300: 
    output[count] = []
    question_template = 'How many (Case Entity) occurred in (Location Entity) (Time Entity)?'
    case_entity = random.choice(case_entity_list)
    location = random.choice(data['Location Entity'])
    while location == 'state' or location == 'county' or location == 'country' or location == 'province' or location == 'globally' or location == 'in the world/around the world': 
        location = random.choice(data['Location Entity'])
    real_question = question_template
    if case_entity.find("increased") >=0:
        time_entity = random.choice(range_time_entity_total)
        sql_template = "Select (Select SUM(Cases) from db1global where date = 'end date' and (Location)) - (Select SUM(Cases) from db1global where date = 'start date' and (Location))"
        query = sql_template 
        query, time_e = timeTotalQueryRange(query, time_entity)
    elif case_entity == 'new cases' or case_entity == 'daily cases':
        time_entity = random.choice(single_time_entity_daily)
        sql_template = "Select (Select SUM(Cases) from db1global where date = 'end date' and (Location)) -  (Select SUM(Cases) from db1global where date = 'start date' and (Location))"
        query = sql_template
        query, time_e = timeTotalQueryRange(query, time_entity)
    else:
        time_entity = random.choice(single_time_entity_total)
        sql_template = "Select SUM(Cases) from db1global where date = 'given date' and (Location)" 
        query = sql_template
        query, time_e = timeTotalQuerySingle(query, time_entity)
    real_question = real_question.replace('(Case Entity)', case_entity)
    real_question = real_question.replace("(Time Entity)", time_e)
    """if location == 'globally' or location == 'in the world/around the world': 
        query = query.replace("and (Location)", "")
        if location == 'in the world/around the world':
            real_question = real_question.replace("(Location Entity)", 'the world')
        else:
            real_question = real_question.replace("in (Location Entity)", "globally")
        entities = ['Case Entity', 'Location Entity', 'Time Entity']"""
    if location == '(State)' or location == '(State Abbreviation)' or location == '(State), (Country)' or location == 'in the state of (State)':
        sql_template = sql_template.replace("db1global", 'db1state')
        query = query.replace("db1global", 'db1state')
        if location == '(State)' or location == 'in the state of (State)': 
            state_name = random.choice(data2['State'])
            query = query.replace("(Location)", "Province_State = \"" + state_name + "\"")
            loc = location.replace("(State)", state_name)
            if location == 'in the state of (State)':
                loc = loc.replace("in ", "")
            populated_entities = [case_entity, state_name, time_e]
        elif location == '(State Abbreviation)': 
            state_abbreviation = random.choice(data2['State Abbreviation'])
            state_name = state_dict[state_abbreviation]
            query = query.replace("(Location)", "Province_State = \"" +state_name + "\"")
            loc = location.replace("(State Abbreviation)", state_abbreviation)
            populated_entities = [case_entity, state_abbreviation, time_e]
        else:
            state_name = random.choice(data2['State'])
            query = query.replace("(Location)", "Province_State = \"" + state_name + "\"")
            loc = location.replace("(State)", state_name)
            loc = loc.replace("(Country)", 'United States')
            populated_entities = [case_entity, state_name, time_e]
        real_question = real_question.replace("(Location Entity)", loc)
        question_template = "How many (Case Entity) occurred in (State Entity) (Time Entity)?"
        entities =  ['Case Entity', 'State Entity', 'Time Entity']
        
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
        question_template = "How many (Case Entity) occurred in (Province Entity) (Country Entity) (Time Entity)?"
        real_question = real_question.replace("(Location Entity)", loc)
        entities = ['Case Entity' ,'Province Entity', 'Country Entity', 'Time Entity']
        poulated_entities = [case_entity, province_name, country_name, time_e]
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
        real_question = real_question.replace("(Location Entity)", loc)
        question_template = "How many (Case Entity) occurred in (County Entity) (State Entity) (Time Entity)?"
        entities = ['Case Entity', 'County Entity', 'State Entity', 'Time Entity']
        populated_entities = [case_entity, county_name, state_name, time_e]
    elif location == '(Country)' or location == 'the country of (Country)': 
        country = random.choice(data2['Country'])
        if country == 'United States':
            query = query.replace("(Location)", "Country_Region = 'US' ")
        else: 
            query = query.replace("(Location)", "Country_Region = \"" + country + "\" ")
        loc = location.replace("(Country)", country)
        real_question = real_question.replace("(Location Entity)", loc)
        question_template = "How many (Case Entity) occurred in (Country Entity) (Time Entity)?"
        entities = ['Case Entity', 'Country Entity', 'Time Entity']
        populated_entities = [case_entity, country, time_e]
    query = caseQuery(case_entity, query)
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
        
#with open('db1q1data.json', 'w') as outfile: 
#    json.dump(output,outfile)
#print("done")