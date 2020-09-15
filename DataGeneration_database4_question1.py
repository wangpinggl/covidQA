# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 03:39:20 2020

@author: Srikar Balusu
"""

import json
import pandas as pd
import numpy as np
import re
import random
import sqlite3

question_template = "What is the breakdown of (Case Entity) by (Demographic Entity) in the United States?"
question_template_id = 'db4q1'
output = {}
question_key = {}
conn = sqlite3.connect('testQ.db')
c = conn.cursor()
case_entity = ['cases', 'confirmed cases', 'deaths']
demographic_entity = ['sex', 'race', 'age', 'age group', 'race and ethnicity', 'ethnicity', 'gender']
entities = ['Case Entity', 'Demographic Entity']
count = 1
for i in case_entity:
    for j in demographic_entity: 
        output[count] = []
        populated_entities = []
        real_question = question_template.replace("(Demographic Entity)", j)
        real_question = real_question.replace("(Case Entity)", i)
        sql_template = "Select * from table_name"
        if i == 'cases' or i == 'confirmed cases': 
            if j == 'sex' or j == 'gender':
                table_name = 'db4casegender'
            elif j == 'race' or j == 'race and ethnicity' or j=='ethnicity': 
                table_name = 'db4caserace'
            else:
                table_name = 'db4caseage'
        else:
            if j == 'sex' or j == 'gender':
                table_name = 'db4deathgender'
            elif j == 'race' or j == 'race and ethnicity' or j=='ethnicity': 
                table_name = 'db4deathrace'
            else:
                table_name = 'db4deathage'
        query = sql_template.replace("table_name", table_name)
        populated_entities.append(i)
        populated_entities.append(j)
        c.execute(query)
        result = c.fetchall()
        output[count].append({'question_template_id' : question_template_id, 'question_template' : question_template, 
        'entities' : entities, 'question' : real_question, 
        'populated_entities': populated_entities, 'query_template' : sql_template, 'query' :  query, 'database': 'database 4'})
        print(count)
        print(real_question)
        print(query)
        print(result)
        count = count + 1
    
with open('db4q1data.json', 'w') as outfile: 
    json.dump(output,outfile)

        
print('done')