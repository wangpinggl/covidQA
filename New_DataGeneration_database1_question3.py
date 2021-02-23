# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 01:28:20 2020

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
location_entity_list = ['county', 'state', 'province', 'country']
question_template_id = 'db1q3'
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

def genLocQuery(location_entity, rangeQ):
    if location_entity == 'county':
        if rangeQ == True:
            query = "Select t1.Admin2, t1.Province_State from (Select Admin2, Province_State, SUM(Cases) as Value1 from db1global where date = 'end date' and Admin2 != 'Unassigned' and Admin2 is not null and Province_State is not null Group by Admin2, Province_State) as t1 Inner Join(Select Admin2, Province_State, SUM(Cases) as Value2 from db1global where date = 'start date' and Admin2 != 'Unassigned' and Admin2 is not null and Province_State is not null Group by Admin2, Province_State) as t2 on t1.Admin2 = t2.Admin2 and t1.Province_State=t2.Province_State order by t1.Value1-t2.Value2 asc/desc limit X,1"
        else:
            query = "Select Admin2, Province_State from db1global where date = 'given date' and Admin2 != 'Unassigned' and Admin2 is not null and Province_State is not null Group by Admin2, Province_State order by SUM(Cases) asc/desc limit X,1" 
    elif location_entity == 'state': 
        if rangeQ == True: 
            query = "Select t1.Province_State from (Select Province_State, SUM(Cases) as Value1 from db1state where date = 'end date' and Province_State is not null Group by Province_State) as t1 Inner Join(Select Province_State, SUM(Cases) as Value2 from db1state where date = 'start date' and Province_State is not null Group by Province_State) on t1.Province_State = t2.Province_State order by asc/desc limit X,1"
        else:
            query = "Select Province_State from db1state where date = 'given date' and Province_State is not null Group by Province_State order by SUM(Cases) asc/desc limit X,1"
    elif location_entity == 'province':
        if rangeQ == True:
            query = "Select t1.Province_State, t1.Country_Region from (Select Province_State, Country_Region, SUM(Cases) as Value1 from db1global where date = 'end date' and Country_Region != 'US' and Country_Region is not null and Province_State is not null Group by Province_State, Country_Region) as t1 Inner Join (Select Province_State, Country_Region, SUM(Cases) as Value2 from db1global where date = 'start date' and Country_Region != 'US' and Country_Region is not null and Province_State is not null Group by Province_State, Country_Region) as t2 on t1.Province_State=t2.Province_State and t1.Country_Region = t2.Country_Region order by t1.Value1-t2.Value2 asc/desc limit X,1"
        else:
            query = "Select Province_State, Country_Region from db1global where date = 'given date' and Country_Region is not null and Province_State is not null and Country_Region != 'US' Group by Province_State, Country_Region order by SUM(Cases) asc/desc limit X,1"
    else: 
        if rangeQ == True: 
            query = "Select t1.Country_Region from (Select Country_Region, SUM(Cases) as Value1 from db1global where date = 'end date' and Country_Region is not null Group by Country_Region) as t1 Inner Join(Select Country_Region, SUM(Cases) as value2 from db1global where date = 'start date' and Country_Region is not null Group by Country_Region) as t2 on t1.Country_Region = t2.Country_Region order by t1.Value1-t2.Value2 asc/desc limit X,1"
        else:
            query = "Select Country_Region from db1global where date = 'given date' and Country_Region is not null group by Country_Region order by SUM(Cases) asc/desc limit X,1"
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
    question_template = 'What (Location Entity) has the (Value Entity) number of (Case Entity) (Time Entity)?'
    case_entity = random.choice(case_entity_list)
    location = random.choice(location_entity_list)
    real_question = question_template
    val = random.choice(data['Value Entity'])
    if val.find("(x)") >= 0:
        order = random.randint(2,10)
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
    if case_entity.find("increased") >=0:
        time_entity = random.choice(range_time_entity_total)
        sql_template = "Select t1.(Location) from (Select (Location) from db1global, SUM(Cases) as Value1 from db1global where date = 'end date' and (Null) Group by (Location)) as t1 Inner Join (Select (Location), SUM(Cases) as Value2 from db1global where date = 'start date' and (Null) Group by (Location)) as t2 on t1.(Location) = t2.(Location) order by t1.Value1-t2.Value2 asc/desc limit X,1"
        rangeQ = True
        query = genLocQuery(location, rangeQ)
        query, time_e = timeTotalQueryRange(query, time_entity)
    elif case_entity == 'new cases' or case_entity == 'daily cases':
        time_entity = random.choice(single_time_entity_daily)
        sql_template = "Select t1.(Location) from (Select (Location) from db1global, SUM(Cases) as Value1 from db1global where date = 'end date' and (Null) Group by (Location)) as t1 Inner Join (Select (Location), SUM(Cases) as Value2 from db1global where date = 'start date' and (Null) Group by (Location)) as t2 on t1.(Location) = t2.(Location) order by t1.Value1-t2.Value2 asc/desc limit X,1"
        rangeQ = True
        query = genLocQuery(location, rangeQ)
        query, time_e = timeTotalQueryRange(query, time_entity)
    else: 
        time_entity = random.choice(single_time_entity_total)
        sql_template = "Select (Location) from db1global where date = 'given date' and (Null) Group by (Location) order by SUM(Cases) asc/desc limit X,1"
        rangeQ = False
        query = genLocQuery(location, rangeQ)
        query, time_e = timeTotalQuerySingle(query, time_entity)
    query = caseQuery(case_entity, query)
    if ascending == False:
        query = query.replace('asc/desc','desc')
        query = query.replace('X', str(order-1))
    else:
        query = query.replace('asc/desc','asc')
        query = query.replace('X', str(order-1))
    real_question = real_question.replace("(Value Entity)", val)
    real_question = real_question.replace("(Location Entity)", location)
    real_question = real_question.replace("(Case Entity)", case_entity)
    real_question = real_question.replace("(Time Entity)", time_e)
    question_template = question_template.replace("(Location Entity)", location)
    entities = ['Value Entity', 'Case Entity', 'Time Entity']
    populated_entities = [val, case_entity, time_e]
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
        
#with open('db1q3data.json', 'w') as outfile: 
#    json.dump(output,outfile)
#print("done")
        