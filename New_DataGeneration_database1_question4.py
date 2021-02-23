# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 02:28:18 2020

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
question_template_id = 'db1q4'
single_time_entity_total = ['as of yesterday', 'as of day before yesterday', 'as of today', 'as of (month), (date)', 'as of last (day)', 'up till yesterday', 'up till today', 'up till day before yesterday', 'up till last (day)', 'up till (month), (date)'] 
output = {}
month_day_dict = {'January' : 30, 'February' : 29, 'March' : 31, 'April' : 30, 'May' : 31, 'June' : 30, 'July' :31, 'August' : 31, 'September' : 30, 'October' : 31, 'November' : 30, 'December' : 31}
month_dict= {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7 , 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
day_map = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6}
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
count = 1
location_entity_list = ['county', 'state', 'province', 'country']
rate_entity_list = ['incidence rate', 'case-fatality rate', 'recovery rate', 'testing rate']
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

while count<300: 
    output[count] = []
    question_template = 'What (Location Entity) has the (Value Entity) (Rate Entity) (Time Entity)?'
    location = random.choice(location_entity_list)
    rate_entity = random.choice(rate_entity_list)
    if rate_entity == 'testing entity':
        location = 'state'
    sql_template = "Select (Location) from db1global where date = 'given date' and (Null) group by (Location) having (Rate) is not null order by (Rate) asc/desc limit X,1"
    
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
    if location == 'county':
        query = "Select Admin2, Province_State from db1global where date = 'given date' and Admin2 is not null and Province_State is not null group by Admin2, Province_State having (Rate) is not null order by (Rate) asc/desc limit X,1"
    elif location == 'state':
        query = "Select Province_State from db1state where date = 'given date' and Province_State is not null group by Province_State having (Rate) is not null order by (Rate) asc/desc limit X,1"
    elif location == 'province':
        query = "Select Province_State, Country_Region from db1global where date = 'given date' and Country_Region != 'US' and Province_State is not null and Country_Region is not null group by Province_State, Country_Region having (Rate) is not null order by (Rate) asc/desc limit X,1"
    else:
        query = "Select Country_Region from db1global where date = 'given date' and Country_Region is not null group by Country_Region having (Rate) is not null order by (Rate) asc/desc limit X,1"
    if rate_entity == 'incidence rate':
        query = query.replace("(Rate)", "SUM(Confirmed)/SUM(Confirmed * 100000/Incidence_Rate) * 100000")
    elif rate_entity == 'case-fatality rate':
        query = query.replace("(Rate)", "SUM(Deaths)*100.0/SUM(Confirmed)")
    elif rate_entity == 'recovery rate':
        query = query.replace("(Rate)", "SUM(Recovered)*100.0/SUM(Confirmed)")
    else:
        query = query.replace("(Rate)", "Testing_Rate")
    time_entity = random.choice(single_time_entity_total)
    query, time_e = timeTotalQuerySingle(query, time_entity)
    if ascending == False:
        query = query.replace('asc/desc','desc')
        query = query.replace('X', str(order-1))
    else:
        query = query.replace('asc/desc','asc')
        query = query.replace('X', str(order-1))
    real_question = question_template.replace("(Location Entity)", location)
    real_question = real_question.replace("(Rate Entity)", rate_entity)
    real_question = real_question.replace("(Time Entity)", time_e)
    real_question = real_question.replace("(Value Entity)", val)
    question_template = question_template.replace("(Location Entity)", location)
    entities = ['Value Entity', 'Rate Entity', 'Time Entity']
    populated_entities = [val, rate_entity, time_e]
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
        
#with open('db1q4data.json', 'w') as outfile: 
#    json.dump(output,outfile)
#print("done")
    
