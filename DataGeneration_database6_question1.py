# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 00:58:31 2020

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

question_template = "What are the number of (Testing Entity) done by (Country Entity) (Time Entity)?"
question_template_id = 'db6q1'
output = {}
question_key = {}
entities = ['Testing Entity', 'Location Entity', 'Time Entity']
testing_entity_list = ['daily tests', 'total tests', 'total tests increased'] 
single_time_entity_total = ['as of yesterday', 'as of day before yesterday', 'as of today', 'as of (month), (date)', 'as of last (day)', 'up till yesterday', 'up till today', 'up till today', 'up till day before yesterday', 'up till last (day)', 'up till (month), (date)']
single_time_entity_daily = ['today', 'yesterday', 'last (day)', 'on (month), (date)', 'day before yesterday']
range_time_entity_total = ['today', 'yesterday', 'day before yesterday', 'last (day)', 'on (month), (date)', 'in the last (x) weeks', 'in the last (x) days', 'since last (day)', 'in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month', 'since the last (x) days']
range_time_entity = ['in the last (x) weeks', 'in the last (x) months', 'in the last (x) days', 'since last (day)','in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month', 'since the last (x) days']
count = 1
month_dict= {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7 , 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
month_day_dict = {'January' : 30, 'February' : 29, 'March' : 31, 'April' : 30, 'May' : 31, 'June' : 30, 'July' :31, 'August' : 31, 'September' : 30, 'October' : 31, 'November' : 30, 'December' : 31}
day_map = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6}
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
def timeDailyQuerySingle(query, time_entity):
    output = time_entity
    if time_entity == 'today': 
        query = query.replace('Time Entity', datetime.date.today().strftime("%b %d, %Y"))
    elif time_entity == 'yesterday':
        date = datetime.date.today() - datetime.timedelta(days=1)
        query = query.replace('Time Entity', date.strftime("%b %d, %Y"))
    elif time_entity == 'day before yesterday': 
        date = datetime.date.today() - datetime.timedelta(days=2)
        query = query.replace('Time Entity', date.strftime("%b %d, %Y"))
    elif time_entity == 'last (day)':
        chosen_date = random.choice(day)
        today = datetime.date.today()
        offset = (today.weekday() - day_map[chosen_date]) %7
        if offset == 0: 
            query = query.replace("Time Entity", (today-datetime.timedelta(days=7)).strftime("%b %d, %Y"))
        else: 
            query = query.replace("Time Entity", (today-datetime.timedelta(days=offset)).strftime("%b %d, %Y"))
        output = output.replace("(day)", chosen_date)
    else:
        month = random.choice(data2['Month'])
        date = random.choice(data2['Day'])
        while date == '31st' or date == '30th' or date == '29th': 
            date = random.choice(data2['Day'])
        while date in day: 
            date = random.choice(data2['Day'])
        if len(date) == 3: 
            date_num = date[0]
                            
        else:
            date_num = date[0:2]
        mon = month[0:3]
        query = query.replace("Time Entity", mon + " " + date_num + ", 2020")
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
    return query, output

def timeTotalQuerySingle(query, time_entity):
    output = time_entity
    if time_entity.find('today')>=0: 
        query = query.replace('Time Entity', datetime.date.today().strftime("%b %d, %Y"))
    elif time_entity.find('yesterday')>=0:
        date = datetime.date.today() - datetime.timedelta(days=1)
        query = query.replace('Time Entity', date.strftime("%b %d, %Y"))
    elif time_entity.find('day before yesterday') >=0: 
        date = datetime.date.today() - datetime.timedelta(days=2)
        query = query.replace('Time Entity', date.strftime("%b %d, %Y"))
    elif time_entity.find('last (day)') >=0:
        chosen_date = random.choice(day)
        today = datetime.date.today()
        offset = (today.weekday() - day_map[chosen_date]) %7
        if offset == 0: 
            query = query.replace("Time Entity", (today-datetime.timedelta(days=7)).strftime("%b %d, %Y"))
        else: 
            query = query.replace("Time Entity", (today-datetime.timedelta(days=offset)).strftime("%b %d, %Y"))
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
        mon = month[0:3]
        query = query.replace("Time Entity", mon + " " + date_num + ", 2020")
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
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
    query = query.replace("Time Entity", end_date.strftime("%b %d, %Y"),1)
    query = query.replace("Time Entity", start_date.strftime("%b %d, %Y"),1)
    return query, output
            
while count < 300: 
    output[count] = []
    location = random.choice(data2['Country'])
    testing_entity = random.choice(testing_entity_list)
    isNull = False
    if testing_entity == 'daily tests': 
        time_entity = random.choice(single_time_entity_daily)
        sql_template = "Select Testing Entity Column from db6file4 where Entity = \"Country Entity\" and Date = 'Time Entity'"
        query = sql_template.replace("Testing Entity Column", "New_Test")
        query = query.replace("Country Entity", location)
        query, time_e = timeDailyQuerySingle(query, time_entity)
        
    elif testing_entity == 'total tests': 
        time_entity = random.choice(single_time_entity_total)
        sql_template = "Select Testing Entity Column from db6 where Entity = \"Country Name\" and Date = 'Time Entity'"
        query = sql_template.replace("Testing Entity Column", "Total")
        query = query.replace("Country Entity", location)
        if random.random() <0.2: 
            isNull = True
        if isNull:
            query, time_e = timeTotalQuerySingle(query, 'today')
            time_e = "Null"
        else:
            query, time_e = timeTotalQuerySingle(query,time_entity)
        
    else:
        time_entity = random.choice(range_time_entity_total)
        sql_template = "Select (Select Testing Entity Column from db6 where date = 'Time Entity' and Entity = \" Country Entity\") - (Select Testing Entity Column from db6 where date = 'Time Entity' and Entity = \"Country Entity\")"
        
        query = sql_template.replace("Country Entity", location)
        query = query.replace("Testing Entity Column", "Total")
        query, time_e = timeTotalQueryRange(query, time_entity)
    
    real_question = question_template
    real_question = real_question.replace("(Testing Entity)", testing_entity)
    real_question = real_question.replace("(Country Entity)", location)
    if isNull:
        real_question = real_question.replace(" (Time Entity)", "")
    else:
        real_question = real_question.replace("(Time Entity)", time_e)
    populated_entities = []
    populated_entities.append(testing_entity)
    populated_entities.append(location)
    populated_entities.append(time_e)
    c.execute(query)
    result = c.fetchall()
    #if len(result) == 0:
      #  continue
    if real_question in question_key.keys():
        continue
    else:
        question_key[real_question] = True
        output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
              'entities' : entities, 'question' : real_question, 
              'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 6'})
        print(count)
        print(time_e)
        print(question_template)
        print(sql_template)
        print(real_question)
        print(query)
        print(result)
        count = count + 1
with open('db6q1data.json', 'w') as outfile: 
    json.dump(output,outfile)
print("done")