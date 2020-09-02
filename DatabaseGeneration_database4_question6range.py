# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 02:48:28 2020

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
question_template = 'What is the percentage change in (Mobility Entity) in (Location Entity) (Time Entity)?'
question_template_id = 'db4q6'
output = {}
entities = ['Mobility Entity', 'Location Entity', 'Time Entity']

range_time_entity = ['in the last (x) weeks', 'in the last (x) months', 'in the last (x) days', 'since last (day)','in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month', 'since the last (x) days', 'since (month), (date)']
count = 1

month_day_dict = {'January' : 30, 'February' : 29, 'March' : 31, 'April' : 30, 'May' : 31, 'June' : 30, 'July' :31, 'August' : 31, 'September' : 30, 'October' : 31, 'November' : 30, 'December' : 31}
month_dict= {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7 , 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
day_map = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6}
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

question_key = {}
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

def timeQueryRange(query, time_entity):
    output = time_entity
    if time_entity.find("(x)") >=0: 
        if time_entity.find("weeks")>=0:
            num_week = random.randint(1,10)
            end_date = datetime.date.today()
            start_date = datetime.date.today() - datetime.timedelta(days=7*num_week)
            query = query.replace("end date", str(end_date))
            query = query.replace("start date", str(start_date))
            output = output.replace("(x)", str(num_week))
        elif time_entity.find("days") >= 0: 
            num_days = random.randint(1,30)
            end_date = datetime.date.today()
            start_date = datetime.date.today()-datetime.timedelta(days=num_days)
            query = query.replace("end date", str(end_date))
            query = query.replace("start date", str(start_date))
            output = output.replace("(x)", str(num_days))
        elif time_entity.find("months") >=0:
            num_month = random.randint(1,5)
            end_date = datetime.date.today() 
            start_date = datetime.date.today() - relativedelta(months=num_month)
            query = query.replace("end date", str(end_date))
            query = query.replace("start date", str(start_date))
            output = output.replace("(x)", str(num_month))
    elif time_entity == 'in the month of (month)' or time_entity == 'in (month)':
        month = random.choice(data2['Month'])
        year = 2020
        month_num = month_dict[month]
        start_date = datetime.date(year, month_num, 1)
        end_date = datetime.date(year, month_num, calendar.monthrange(year,month_num)[1])
        query = query.replace("end date", str(end_date))
        query = query.replace("start date", str(start_date))
        output = output.replace("(month)", month)
    elif time_entity == 'since (month), (date)': 
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
        start_date = datetime.date(2020, month_dict[month], int(date_num))
    
        end_date = datetime.date.today()
        query = query.replace("end date", str(end_date))
        query = query.replace("start date", str(start_date))
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
    elif time_entity == 'since last month' or time_entity  == 'since last week': 
        if time_entity == 'since last month': 
            end_date = datetime.date.today()
            start_date = end_date - relativedelta(months=1)
            query = query.replace("end date", str(end_date))
            query = query.replace("start date", str(start_date))
        else: 
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=7)
            query = query.replace("end date", str(end_date))
            query = query.replace("start date", str(start_date))
    else: 
        chosen_date = random.choice(day)
        today = datetime.date.today()
        query = query.replace('end date', str(today))
        if chosen_date == 'Monday':
            if today.weekday() % 7 == 0:
                query = query.replace("start date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("start date", str(today-datetime.timedelta(days=today.weekday()%7)))
        elif chosen_date == 'Tuesday':
            offset = (today.weekday()-1)%7
            if offset == 0:
                query = query.replace("start date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("start date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Wednesday': 
            offset = (today.weekday()-2)%7
            if offset == 0:
                query = query.replace("start date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("start date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Thursday': 
            offset = (today.weekday()-3)%7
            if offset == 0:
                query = query.replace("start date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("start date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Friday': 
            offset = (today.weekday()-4)%7
            if offset == 0:
                query = query.replace("start date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("start date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Saturday': 
            offset = (today.weekday()-5)%7
            if offset == 0:
                query = query.replace("start date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("start date", str(today-datetime.timedelta(days=offset)))
        elif chosen_date == 'Sunday': 
            offset = (today.weekday()-6)%7
            if offset == 0:
                query = query.replace("start date", str(today-datetime.timedelta(days=7)))
            else:
                query = query.replace("start date", str(today-datetime.timedelta(days=offset)))
        output = output.replace("(day)", chosen_date)
    return query, output 


while count < 100: 
    output[count] = []
    populated_entities = []
    mobility = random.choice(data['Mobility Entity'])
    location = random.choice(data['Location Entity'])
    while location.find('Country') >=0 or location.find('Province') >= 0 or location.find("(") < 0: 
        location = random.choice(data['Location Entity'])
    if location == 'in the state of (State)': 
        location = 'the state of (State)'
    entity = re.findall('\(([^)]+)', location)
    sql_template = "Select (Select (Mobility) from db4mobility where date = 'end date' and country_region = 'United States' and sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\") - (Select (Mobility) from db4mobility where date = 'start date' and country_region = 'United States' and sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\")" 
    query = ""
    if len(entity) == 1:
        if entity[0] == 'State': 
            state_name = random.choice(data2['State'])
            while state_name == 'Guam' or state_name == 'Virgin Islands' or state_name == 'Diamond Princess' or state_name == 'Northern Mariana Islands':
                state_name = random.choice(data2['State'])
            query = sql_template.replace("State name", state_name)
            query = mobilityQuerySingle(mobility,query)
            time_entity = random.choice(range_time_entity)
            query, time_e = timeQueryRange(query, time_entity)
            loc = location.replace("(State)", state_name)
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
            real_question = real_question.replace("(Time Entity)", time_e)
          
        else: 
            state_abbreviation = random.choice(data2['State Abbreviation'])
            while state_abbreviation  == 'PR' or state_abbreviation == 'GU' or state_abbreviation == 'VI':
                state_abbreviation = random.choice(data2['State Abbreviation'])
            state_name = state_dict[state_abbreviation]
            query = sql_template.replace("State name", state_name)
            query = mobilityQuerySingle(mobility, query)
            time_entity = random.choice(range_time_entity)
            query, time_e = timeQueryRange(query, time_entity)
            loc = location.replace("(State Abbreviation)", state_abbreviation)
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
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
            time_entity = random.choice(range_time_entity)
            query, time_e = timeQueryRange(query, time_entity)
            query = query.replace("and iso_3166_2_code LIKE \"US-%\"", "")
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
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
            time_entity = random.choice(range_time_entity)
            query, time_e = timeQueryRange(query, time_entity)
            query = query.replace("and iso_3166_2_code LIKE \"US-%\"", "")
            real_question = question_template.replace("(Location Entity)",loc)
            real_question = real_question.replace("(Mobility Entity)", mobility)
            real_question = real_question.replace("(Time Entity)", time_e)
    populated_entities.append(mobility)
    populated_entities.append(loc)
    populated_entities.append(time_e)
    c.execute(query)
    result = c.fetchall()
    #if len(result) == 0 or result[0][0] == None:
    #   continue
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
            
            