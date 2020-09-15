# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 04:06:51 2020

@author: Srikar Balusu
"""

import json
import pandas as pd
import numpy as np
import re
import random
import sqlite3


with open('lookup1.json') as json_file: 
    data = json.load(json_file)

with open('uniquelookup.json') as json_file:
    data2 = json.load(json_file)

conn = sqlite3.connect('testQ.db')
c = conn.cursor()

question_template = 'What (Demographic Entity) has the (Value Entity) (Amount Entity) (Case Entity) in the United States?'
question_template_id = 'db4q2' 
output = {}

case_entity = ['cases', 'confirmed cases', 'deaths']
demographic_entity = ['sex', 'race', 'age', 'age group', 'race and ethnicity', 'ethnicity', 'gender']
entities = ['Demographic Entity', 'Value Entity', 'Amount Entity', 'Case Entity']
amount_entity = ['number of','percentage of']
count = 1

def changeQuery(demographic, ascending, amount, case):
    query = ""
    if case == 'confirmed cases' or case == 'cases':
        if demographic == 'sex' or demographic == 'gender':
            query = sql_template.replace("Demographic Entity", "Sex")
            query = query.replace("table name", "db4casegender")
        elif demographic == 'age' or demographic == 'age group':
            query = sql_template.replace("Demographic Entity", "Age_Group")
            query = query.replace("table name", "db4caseage")
        else:
            query = sql_template.replace("Demographic Entity", "Race_Ethnicity")
            query = query.replace("table name", "db4caserace")
    else:
        if demographic == 'sex' or demographic == 'gender':
            query = sql_template.replace("Demographic Entity", "Sex")
            query = query.replace("table name", "db4deathgender")
        elif demographic == 'age' or demographic == 'age group':
            query = sql_template.replace("Demographic Entity", "Age_Group")
            query = query.replace("table name", "db4deathage")
        else:
            query = sql_template.replace("Demographic Entity", "Race_Ethnicity")
            query = query.replace("table name", "db4deathrace")
    if amount =='percentage of': 
        query = query.replace("Amount Entity", "Percentage")
    else:
        query = query.replace("Amount Entity", "Count")
    
    if ascending == False:
        query = query.replace('Value Entity','desc limit ' + str(order-1) + ', 1')
    else:
        query = query.replace('Value Entity','asc limit ' + str(order-1) + ', 1')
    
    return query

for case in case_entity:
    for demographic in demographic_entity:
        for amount in amount_entity:
            output[count] = []
            populated_entities = []
            sql_template = "Select Demographic Entity, Amount Entity from table name Order by Amount Entity Value Entity"
            val = random.choice(data['Value Entity'])
            query = ""
            if val.find("(x)") >= 0:
                order = random.randint(1,4)
                val = val.replace("(x)", str(order))
                if order == 2: 
                    val = val.replace("th", "nd")
                if order == 3: 
                    val = val.replace("th", "rd")
            else:
                order = 1
            if val.find("most") >= 0 or val.find("highest") >=0 or val.find("Highest") >=0:
                ascending = False
            else:
                ascending = True
            real_question = question_template.replace("(Demographic Entity)", demographic)
            real_question = real_question.replace("(Value Entity)", val)
            real_question = real_question.replace("(Case Entity)", case)
            real_question = real_question.replace("(Amount Entity)", amount)
            query = changeQuery(demographic, ascending, amount, case)
            c.execute(query)
            result = c.fetchall()
            populated_entities.append(demographic)
            populated_entities.append(val)
            populated_entities.append(amount)
            populated_entities.append(case)
            output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
                 'entities' : entities, 'question' : real_question, 
                 'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 4'})
            print(count)
            print(question_template)
            print(sql_template)
            print(real_question)
            print(query)
            print(result)
            count = count + 1

with open('db4q2data.json', 'w') as outfile: 
    json.dump(output,outfile)

print("done")