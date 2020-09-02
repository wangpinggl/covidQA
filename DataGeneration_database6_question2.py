# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 04:35:34 2020

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
question_template = 'What is the (Rate Entity) in (Location Entity) (Time Entity)?'
question_template_id = 'db6q2' 
time_entity_list = ['on (month), (date)', 'today', 'yesterday', 'day before yesterday', 'as of (month), (date)','as of today', 'as of yesterday', 'as of last (day)', 'last (day)', 'as of day before yesterday']
output = {}
entities = ['Rate Entity', 'Location Entity', 'Time Entity']
month_day_dict = {'January' : 30, 'February' : 29, 'March' : 31, 'April' : 30, 'May' : 31, 'June' : 30, 'July' :31, 'August' : 31, 'September' : 30, 'October' : 31, 'November' : 30, 'December' : 31}
month_dict= {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7 , 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
day_map = {'Monday' : 0, 'Tuesday' : 1, 'Wednesday' : 2, 'Thursday' : 3, 'Friday' : 4, 'Saturday' : 5, 'Sunday' : 6}
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
rate_entity_list = ['percent positive rate', 'percent negative rate', 'daily testing rate']
count = 1

def timeSingleQuery(query, time_entity):
    output = time_entity

    if time_entity.find('today')>=0: 
        in_date = datetime.date.today()
    elif time_entity.find('yesterday') >=0: 
        in_date = datetime.date.today() - datetime.timedelta(days =1)
    elif time_entity.find('day before yesterday') >= 0: 
        in_date = datetime.date.today() - datetime.timedellta(days=2)
    elif time_entity.find('last (day)') >=0: 
        chosen_date = random.choice(day)
        today = datetime.date.today()
        offset = (today.weekday() - day_map[chosen_date]) %7
        if offset == 0: 
            in_date = today-datetime.timedelta(days=7)
        else: 
            in_date = today-datetime.timedelta(days=offset)
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
        in_date = datetime.date(2020, month_dict[month], int(date_num))
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
    query = query.replace('given date', in_date.strftime("%b %d, %Y"))
    return query, output
        
    
    
while count <300 :
    location = random.choice(data2['Country'])
    rate_entity = random.choice(rate_entity_list)
    time_entity = random.choice(time_entity_list)
    output[count] = []
    if random.random()<0.2:
        isNull = True
    else:
        isNull = False
    if rate_entity == 'percent positive rate':
        sql_template = "Select pos_rate from db6file2 where date = 'given date' and Entity = \"Country Name\" "
        query = sql_template.replace("Country Name", location)
        if isNull:
            query, time_e = timeSingleQuery(query, 'today')
            time_e = 'Null'
        else:
            query, time_e = timeSingleQuery(query, time_entity)
    elif rate_entity == 'percent negative rate':
        sql_template = "Select 100-pos_rate from db6file2 where date = 'given date' and Entity = \"Country Name\" "
        query = sql_template.replace("Country Name", location)
        if isNull:
            query, time_e = timeSingleQuery(query, 'today')
            time_e = 'Null'
        else:
            query, time_e = timeSingleQuery(query, time_entity)
    else:
        sql_template = "Select daily_rate from db6file3 where date = 'given date' and Entity = \"Country Name\" "
        query = sql_template.replace("Country Name", location)
        query, time_e = timeSingleQuery(query, time_entity)
    real_question = question_template.replace("(Location Entity)", location)
    if isNull:
        real_question = real_question.replace(" (Time Entity)", "")
    else:
        real_question = real_question.replace("(Time Entity)", time_e)
    real_question = real_question.replace("(Rate Entity)", rate_entity)
    populated_entities = []
    populated_entities.append(rate_entity)
    populated_entities.append(location)
    populated_entities.append(time_e)
    c.execute(query)
    result = c.fetchall()
    #if len(result) == 0 or result[0][0] == None:
      #  continue
    #elif real_question in question_key.keys():
     #   continue
    #else:
    print("Count: " + str(count))
    print(real_question)
    print(query)
    print(result)
    output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
    'entities' : entities, 'question' : real_question, 
    'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 6'})
    count = count + 1
print(output)