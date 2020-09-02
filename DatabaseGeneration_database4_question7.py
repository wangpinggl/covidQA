# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 01:15:38 2020

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
    
    
question_template = "What (Location Entity) had the (Value Entity) percentage change in (Mobility Entity) (Time Entity)?"
question_template_id = 'db4q7'
output = {}
entities = ['Location Entity', 'Value Entity', 'Mobility Entity', 'Time Entity']
single_time_entity = ['on (month), (date)', 'today', 'yesterday', 'day before yesterday', 'as of (month), (date)','as of today', 'as of yesterday', 'as of last (day)', 'last (day)']
range_time_entity = ['in the last (x) weeks', 'in the last (x) months', 'in the last (x) days', 'since last (day)','in the month of (month)', 'in (month)', 'since last week', 'since the last (x) weeks', 'since the last (x) months', 'since last month', 'since the last (x) days']
day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
loc_entity = ['county', 'county in (State)', 'county in (State Abbreviation)', 'state']
def MobilityQuerySingle(mobility, query):
    if  mobility == 'retail and recreation':
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
        month_dict= {'January' : '01', 'February' : '02', 'March' : '03', 'April' : '04', 'May' : '05', 'June' : '06', 'July' : '07' , 'August' : '08', 'September' : '09', 'October' : '10', 'November' : '11', 'December' : '12'}
        month_num = month_dict[month]
        if len(date) == 3: 
            date_num = '0' + date[0]
        else:
            date_num = date[0] + date[1]
        query = query.replace("given date", '2020-'+month_num+'-'+date_num)
        output = output.replace("(month)", month)
        output = output.replace("(date)", date)
    return query, output


count = 1

while count < 5: 
    print("Count: " + str(count))
    
    mobility = random.choice(data['Mobility Entity'])
    location = random.choice(loc_entity)
    entity = re.findall('\(([^)]+)', location)
    rand_num = random.randint(2,2)
    print("Random: " + str(rand_num))
    if rand_num == 1: 
        time_entity = random.choice(single_time_entity)
        sql_template = "Select sub_region_1/2, (Mobility) from db4mobility where date = 'given date' and country_region = 'United States' and (Mobility) is not null order by (Mobility) asc/desc limit X,1"
    else:   
        time_entity = random.choice(range_time_entity)
        sql_template = """Select t1.sub_region_1/2, t1.(Mobility)-t2.(Mobility) from(Select sub_region_1/2, (Mobility)  from db4mobility where date = 'end date' and country_region = 'United States' 
and (Mobility) is not null) as t1 Inner Join (Select sub_region_1/2, (Mobility)  from db4mobility where date = 'start date' and country_region = 'United States' and (Mobility) is not null) 
as t2 on t1.sub_region_1/2=t2.sub_region_1/2 order by t1.(Mobility)-t2.(Mobility) asc/desc limit X,1"""
    val = random.choice(data['Value Entity'])
    if val.find("(x)") >= 0:
        order = random.randint(1,5)
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
    query = sql_template
    real_question = question_template
    print("Location: " + location)
    print("Time: " + time_entity)
    print("Value: " + val)
    print("Mobility: " + mobility)
    
    if location == 'county':
      
        query = query.replace("sub_region_1/2", "sub_region_2")
        query = query.replace("'United States'", "'United States' and sub_region_2 is not null ")
        query = MobilityQuerySingle(mobility,query)
        if rand_num == 1:
            query, time_e = timeQuerySingle(time_entity,query)
        else: 
            query, time_e = timeQueryRange(query, time_entity)
        if ascending == False:
            query = query.replace("asc/desc", "desc")
            query = query.replace("X", str(order-1))
        else:
            query = query.replace("asc/desc", "asc")
            query = query.replace("X", str(order-1))
        real_question = question_template.replace("(Location Entity)", location)
        real_question = real_question.replace("(Value Entity)", val)
        real_question = real_question.replace("(Time Entity)", time_e)
        real_question = real_question.replace("(Mobility Entity)", mobility)
    elif location == 'county in (State)' or location == 'county in (State Abbreviation)': 
        if location == 'county in (State)':
            state_name = random.choice(data2['State'])
            while state_name == 'Guam' or state_name == 'Virgin Islands' or state_name == 'Diamond Princess' or state_name == 'Northern Mariana Islands':
                state_name = random.choice(data2['State'])
            query = query.replace("sub_region_1/2", "sub_region_2")
            query = query.replace("'United States'", "'United States' and sub_region_1 = \"" + state_name + "\" and sub_region_2 is not null")
            query = MobilityQuerySingle(mobility,query)
            if rand_num == 1:
                query, time_e = timeQuerySingle(time_entity,query)
            else: 
                query, time_e = timeQueryRange(query, time_entity)
            if ascending == False:
                query = query.replace("asc/desc", "desc")
                query = query.replace("X", str(order-1))
            else:
                query = query.replace("asc/desc", "asc")
                query = query.replace("X", str(order-1))
            loc = location.replace("(State)", state_name)
            real_question = question_template.replace("(Location Entity)", loc)
            real_question = real_question.replace("(Value Entity)", val)
            real_question = real_question.replace("(Time Entity)", time_e)
            real_question = real_question.replace("(Mobility Entity)", mobility)
        elif location == 'county in (State Abbreviation)': 
            state_abbreviation = random.choice(data2['State Abbreviation'])
            while state_abbreviation  == 'PR' or state_abbreviation == 'GU' or state_abbreviation == 'VI' or state_abbreviation == 'DC':
                state_abbreviation = random.choice(data2['State Abbreviation'])
            state_name = state_dict[state_abbreviation]
            query  = query.replace("sub_region_1/2", "sub_region_2")
            query = query.replace("'United States'", "'United States' and sub_region_1 = \"" + state_name + "\" and sub_region_2 is not null")
            query = MobilityQuerySingle(mobility,query)
            if rand_num == 1:
                query, time_e = timeQuerySingle(time_entity,query)
            else: 
                query, time_e = timeQueryRange(query, time_entity)
            if ascending == False:
                query = query.replace("asc/desc", "desc")
                query = query.replace("X", str(order-1))
            else:
                query = query.replace("asc/desc", "asc")
                query = query.replace("X", str(order-1))
            loc = location.replace("(State Abbreviation)", state_abbreviation)
            real_question = question_template.replace("(Location Entity)", loc)
            real_question = real_question.replace("(Value Entity)", val)
            real_question = real_question.replace("(Time Entity)", time_e)
            real_question = real_question.replace("(Mobility Entity)", mobility)
    elif location == 'state':
       
        query = query.replace('sub_region_1/2', 'sub_region_1')
        query = query.replace("'United States'", "'United States' and iso_3166_2_code like \"US-%\"")
        query = MobilityQuerySingle(mobility,query)
        if rand_num == 1:
            query, time_e = timeQuerySingle(time_entity,query)
        else: 
            query, time_e = timeQueryRange(query, time_entity)
        if ascending == False:
            query = query.replace("asc/desc", "desc")
            query = query.replace("X", str(order-1))
        else:
            query = query.replace("asc/desc", "asc")
            query = query.replace("X", str(order-1))
        real_question = question_template.replace("(Location Entity)", location)
        real_question = real_question.replace("(Value Entity)", val)
        real_question = real_question.replace("(Time Entity)", time_e)
        real_question = real_question.replace("(Mobility Entity)", mobility)
    print(real_question)
    print(query)
    count = count + 1
    
    