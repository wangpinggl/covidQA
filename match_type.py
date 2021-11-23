
import numpy as np
import json
import datetime
import utility
import re
import random

utility = utility.Utility()

month_dict = utility.month_dict

month_dict6 = utility.month_dict6

day_dict = utility.day_dict

today = str(datetime.date.today()).replace("-","")

state_dict = utility.state_dict

state_key = list(state_dict.keys())

state_val = list(state_dict.values())

def dateconvert1(day, month):
    monthstr = str(month_dict[month])
    daystr = str(day_dict[day])
    datenum = monthstr + '_' + daystr + '_' + '2021'
    return datenum

def dateconvert2(day, month):
    monthstr = str(month_dict[month])
    daystr = str(day_dict[day])
    datenum = '2021' + monthstr + daystr
    return datenum

def dateconvert6(day, month):
    monthstr = str(month_dict[month])
    daystr = str(day_dict[day])
    datenum = '2021' + '-' + monthstr + '-' + daystr
    return datenum

def monthconvert1(month):
    monthstr = str(month_dict[month])
    if monthstr == '01':
        startdate = '01_01_2021'
        enddate = '01_31_2021'
    elif monthstr == '02':
        startdate = '02_01_2021'
        enddate = '02_28_2021'
    elif monthstr == '03':
        startdate = '03_01_2021'
        enddate = '03_31_2021'
    elif monthstr == '04':
        startdate = '04_01_2021'
        enddate = '04_30_2021'
    elif monthstr == '05':
        startdate = '05_01_2021'
        enddate = '05_31_2021'
    elif monthstr == '06':
        startdate = '06_01_2021'
        enddate = '06_30_2021'
    elif monthstr == '07':
        startdate = '07_01_2021'
        enddate = '07_31_2021'
    elif monthstr == '08':
        startdate = '08_01_2021'
        enddate = '08_31_2021'
    elif monthstr == '09':
        startdate = '09_01_2021'
        enddate = '09_30_2021'
    elif monthstr == '10':
        startdate = '10_01_2021'
        enddate = '10_31_2021'
    elif monthstr == '11':
        startdate = '11_01_2021'
        enddate = '11_30_2021'
    else:
        startdate = '12_01_2021'
        enddate = '12_31_2021'
    return startdate, enddate

def monthconvert2(month):
    monthstr = str(month_dict[month])
    if monthstr == '01':
        startdate = '20210101'
        enddate = '20210131'
    elif monthstr == '02':
        startdate = '20210201'
        enddate = '20210228'
    elif monthstr == '03':
        startdate = '20210301'
        enddate = '20210331'
    elif monthstr == '04':
        startdate = '20210401'
        enddate = '20210430'
    elif monthstr == '05':
        startdate = '20210501'
        enddate = '20210531'
    elif monthstr == '06':
        startdate = '20210601'
        enddate = '20210630'
    elif monthstr == '07':
        startdate = '20210701'
        enddate = '20210731'
    elif monthstr == '08':
        startdate = '20210801'
        enddate = '20210831'
    elif monthstr == '09':
        startdate = '20210901'
        enddate = '20210930'
    elif monthstr == '10':
        startdate = '20211001'
        enddate = '20211031'
    elif monthstr == '11':
        startdate = '20211101'
        enddate = '20211130'
    else:
        startdate = '20211201'
        enddate = '20211231'
    return startdate, enddate

def monthconvert4(month):
    monthstr = str(month_dict[month])
    if monthstr == '01':
        startdate = '2021-01-01'
        enddate = '2021-01-31'
    elif monthstr == '02':
        startdate = '2021-02-01'
        enddate = '2021-02-28'
    elif monthstr == '03':
        startdate = '2021-03-01'
        enddate = '2021-03-31'
    elif monthstr == '04':
        startdate = '2021-04-01'
        enddate = '2021-04-30'
    elif monthstr == '05':
        startdate = '2021-05-01'
        enddate = '2021-05-31'
    elif monthstr == '06':
        startdate = '2021-06-01'
        enddate = '2021-06-30'
    elif monthstr == '07':
        startdate = '2021-07-01'
        enddate = '2021-07-31'
    elif monthstr == '08':
        startdate = '2021-08-01'
        enddate = '2021-08-31'
    elif monthstr == '09':
        startdate = '2021-09-01'
        enddate = '2021-09-30'
    elif monthstr == '10':
        startdate = '2021-10-01'
        enddate = '2021-10-31'
    elif monthstr == '11':
        startdate = '2021-11-01'
        enddate = '2021-11-30'
    else:
        startdate = '2021-12-01'
        enddate = '2021-12-31'
    return startdate, enddate

case_entity = utility.case_entity

demographic_entity = utility.demographic_entity

entities = utility.entities

amount_entity = utility.amount_entity

with open('templist.json') as json_file:
    data1 = json.load(json_file)

with open('entitylist.json') as json_file:
    data3 = json.load(json_file)

with open('natural_question.json') as json_file:
    data5 = json.load(json_file)

genderlist = data3['Gender']
testlist = data3['Testing Entity']
bedlist = data3['Bed Entity']
ratelist = data3['Rate Entity']
ratelist2 = data3['Rate Entity2']
moblist = data3['Mobility Entity']
hoslist = data3['Hospitalization Entity']
statelist = data3['State Entity']
caselist = data3['Cases']
caselist2 = data3['Cases2']
countrylist = data3['Country Entity']
monthlist = data3['Month']
daylist = data3['Day']
numberlist = data3['Number']
valuelist = data3['Value Entity']
amountlist = data3['Amount Entity']
racelist = data3['Race']
demlist = data3['Demographic Entity']
countylist = data3['County Entity']
provincelist = data3['Province Entity']

for item in data5.values():
    question = item[0]["real_question"]
    question_temp = item[0]["question"]
    query = item[0]["sql"]
    bucket = {}
    for item in genderlist:
        if question.find(item) != -1:
            bucket.update({'Gender': item})
    for item in testlist:
        if question.find(item) != -1:
            bucket.update({'Testing Entity': item})
    for item in bedlist:
        if question.find(item) != -1:
            bucket.update({'Bed Entity': item})
    for item in ratelist:
        if question.find(item) != -1:
            bucket.update({'Rate Entity': item})
    for item in ratelist2:
        if question.find(item) != -1:
            bucket.update({'Rate Entity2': item})
    for item in moblist:
        if question.find(item) != -1:
            bucket.update({'Mobility Entity': item})
    for item in hoslist:
        if question.find(item) != -1:
            bucket.update({'Hospitalization Entity': item})
    for item in statelist:
        if question.find(item) != -1:
            bucket.update({'State Entity': item})
    for item in caselist:
        if question.find(item) != -1:
            bucket.update({'Cases': item})
    for item in caselist2:
        if question.find(item) != -1:
            bucket.update({'Cases2': item})
    for item in countrylist:
        if question.find(item) != -1:
            bucket.update({'Country Entity': item})
    for item in monthlist:
        if question.find(item) != -1:
            bucket.update({'Month': item})
    for item in daylist:
        if question.find(item) != -1:
            bucket.update({'Day': item})
    for item in numberlist:
        if question.find(item) != -1:
            bucket.update({'Number': item})
    for item in valuelist:
        if question.find(item) != -1:
            bucket.update({'Value Entity': item})
    for item in amountlist:
        if question.find(item) != -1:
            bucket.update({'Amount Entity': item})
    for item in racelist:
        if question.find(item) != -1:
            bucket.update({'Race': item})
    for item in demlist:
        if question.find(item) != -1:
            bucket.update({'Demographic Entity': item})
    for item in countylist:
        if question.find(item) != -1:
            bucket.update({'County Entity': item})
    for item in provincelist:
        if question.find(item) != -1:
            bucket.update({'Province Entity': item})

    for keys in data1.keys():
        entity_list = list(data1[keys])
        matchflag = 1
        for item in entity_list:
            if (matchflag == 1) and (item not in list(bucket.keys())):
                matchflag = 0

        if matchflag == 1:
            if entity_list == ['Value Entity', 'Rate Entity2', 'Day', 'Month']:
                if 'state' in question:
                    bucket.update({'matched temp': 'Which state has the (Value Entity) (Rate Entity) in (Day), (Month)?'})
                elif 'county' in question:
                    bucket.update({'matched temp': 'Give me the county that has the (Value Entity) (Rate Entity) in (Day), (Month).'})
                elif 'country' in question:
                    bucket.update({'matched temp': 'List the country that has the (Value Entity) (Rate Entity) in (Day), (Month).'})
                else:
                    bucket.update({'matched temp': 'Provide me with the province that has the (Value Entity) (Rate Entity) in (Day), (Month).'})
            if entity_list == ['County Entity', 'State Entity', 'Race']:
                if 'percentage' in question:
                    bucket.update({'matched temp': 'List the percentage of Covid-19 deaths in (County Entity), (State Entity) that are from (Race Entity).'})
                else:
                    bucket.update({'matched temp': 'How many (Race Entity) deaths occured in (County Entity), (State Entity)?'})
            if entity_list == ['Value Entity', 'Testing Entity', 'Day', 'Month']:
                if 'state' in question:
                    bucket.update({'matched temp': 'Give me the state with the (Value Entity) (Testing Entity) in (Day), (Month).'})
                else:
                    bucket.update({'matched temp': 'Give me the country that has the (Value Entity) (Testing Entity) in (Day), (Month).'})
            if entity_list == ['Value Entity', 'Testing Entity', 'Month']:
                if 'state' in question:
                    bucket.update({'matched temp': 'Provide me with the state with the (Value Entity) (Testing Entity) in (Month).'})
                else:
                    bucket.update({'matched temp': 'List the country that has the (Value Entity) (Testing Entity) in (Month).'})
            else:
                bucket.update({'matched temp': keys})
            break
        else:
            bucket.update({'matched temp': 'None'})




    real_question = bucket['matched temp']

    try:
        gender = bucket['Gender']
    except KeyError:
        pass
    try:
        tes = bucket['Testing Entity']
    except KeyError:
        tes = ''
    try:
        bed = bucket['Bed Entity']
    except KeyError:
        pass
    try:
        rat = bucket['Rate Entity']
    except KeyError:
        rat = ''
    try:
        rat = bucket['Rate Entity2']
    except KeyError:
        rat = ''
    try:
        mob = bucket['Mobility Entity']
    except KeyError:
        pass
    try:
        hos = bucket['Hospitalization Entity']
    except KeyError:
        pass
    try:
        state = bucket['State Entity']
        state_name = bucket['State Entity']
    except KeyError:
        pass
    try:
        cas = bucket['Cases']
    except KeyError:
        pass
    try:
        cas = bucket['Cases2']
    except KeyError:
        pass
    try:
        country_name = bucket['Country Entity']
        country = bucket['Country Entity']
    except KeyError:
        pass
    try:
        mon = bucket['Month']
    except KeyError:
        pass
    try:
        num = bucket['Number']
    except KeyError:
        pass
    try:
        day = bucket['Day']
    except KeyError:
        pass
    try:
        val = bucket['Value Entity']
    except KeyError:
        pass
    try:
        amo = bucket['Amount Entity']
    except KeyError:
        pass
    try:
        rac = bucket['Race']
    except KeyError:
        pass
    try:
        dem = bucket['Demographic Entity']
    except KeyError:
        pass
    try:
        county_name = bucket['County Entity']
    except KeyError:
        pass
    try:
        province_name = bucket['Province Entity']
    except KeyError:
        pass

    if real_question == "How many (Cases) occurred in (State Entity) in (Day), (Month)?":

        sql = "Select SUM(Cases) from db1_state_date where (Location)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("date", given_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        sql = sql.replace("(Location)", "Province_State = \"" + state + "\"")
        bucket.update({'sql': sql})

    if real_question == "Give me the number of (Cases) occurred in (County Entity), (State Entity) in (Day), (Month).":

        sql = "Select SUM(Cases) from db1_date where (Location)"
        given_date = dateconvert1(day, mon)
        sql = sql.replace("date", given_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        sql = sql.replace("(Location)", "Province_State = \"" + state_name + "\" and Admin2 = \"" + county_name + "\" ")
        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of (Cases) occurred in (Province Entity), (Country Entity) in (Month).":

        sql = "Select (Select SUM(Cases) from db1_end_date where (Location)) - (Select SUM(Cases) from db1_start_date where (Location))"

        start_date, end_date = monthconvert1(mon)
        sql = sql.replace("end_date", end_date)
        sql = sql.replace("start_date", start_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        sql = sql.replace("(Location)",
                          "Province_State = \"" + province_name + "\" and Country_Region = \"" + country_name + "\" ")
        bucket.update({'sql': sql})

    if real_question == "List the number of (Cases) occurred in (Country Entity) in (Month).":

        sql = "Select (Select SUM(Cases) from db1_end_date where (Location)) - (Select SUM(Cases) from db1_start_date where (Location))"

        start_date, end_date = monthconvert1(mon)
        sql = sql.replace("end_date", end_date)
        sql = sql.replace("start_date", start_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        if country == 'United States':
            sql = sql.replace("(Location)", "Country_Region = 'US' ")
        else:
            sql = sql.replace("(Location)", "Country_Region = \"" + country + "\" ")
        bucket.update({'sql': sql})

    if real_question == "What is the (Rate Entity) in (State Entity) in (Day), (Month)?":

        sql = "Select (Rate) from db1_state_given_date where (Location)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        sql = sql.replace("(Location)", "Province_State = \"" + state + "\"")
        bucket.update({'sql': sql})

    if real_question == "Give me the number of (Rate Entity) in (County Entity), (State Entity) in (Day), (Month).":

        sql = "Select (Rate) from db1_given_date where (Location)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        sql = sql.replace("(Location)", "Province_State = \"" + state_name + "\" and Admin2 = \"" + county_name + "\" ")
        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of (Rate Entity) in (Province Entity), (Country Entity) in (Day), (Month).":

        sql = "Select (Rate) from db1_given_date where (Location)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        sql = sql.replace("(Location)",
                          "Province_State = \"" + province_name + "\" and Country_Region = \"" + country_name + "\" ")
        bucket.update({'sql': sql})

    if real_question == "List the number of (Rate Entity) in (Country Entity) in (Day), (Month).":

        sql = "Select (Rate) from db1_given_date where (Location)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        if country == 'United States':
            sql = sql.replace("(Location)", "Country_Region = 'US' ")
        else:
            sql = sql.replace("(Location)", "Country_Region = \"" + country + "\" ")
        bucket.update({'sql': sql})

    if real_question == "What State has the (Value Entity) number of (Case Entity) in (Day), (Month)?":

        sql = "Select Province_State from db1_state_given_date where Province_State is not null Group by Province_State order by SUM(Cases) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "Give me the State that has the (Value Entity) number of (Case Entity) in (Day), (Month).":

        sql = "Select Province_State from db1_state_given_date where Province_State is not null Group by Province_State order by SUM(Cases) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "Provide me with the State that has the (Value Entity) number of (Case Entity) in (Day), (Month).":

        sql = "Select Province_State from db1_state_given_date where Province_State is not null Group by Province_State order by SUM(Cases) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "List the State that has the (Value Entity) number of (Case Entity) in (Day), (Month).":

        sql = "Select Province_State from db1_state_given_date where Province_State is not null Group by Province_State order by SUM(Cases) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if cas == 'confirmed cases' or cas == 'cases' or cas == 'cases increased' or cas == 'confirmed cases increased':
            sql = sql.replace("Cases", "Confirmed")
        elif cas == 'daily cases' or cas == 'new cases':
            sql = sql.replace("Cases", 'Confirmed')
        elif cas == 'deaths' or cas == 'deaths increased':
            sql = sql.replace("Cases", "Deaths")
        elif cas == 'active cases' or cas == 'active cases increased':
            sql = sql.replace("Cases", "Active")
        elif cas == 'recovered cases' or cas == 'recovered cases increased':
            sql = sql.replace("Cases", "Recovered")
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "Which state has the (Value Entity) (Rate Entity) in (Day), (Month)?":

        sql = "Select Province_State from db1_state_given_date where Province_State is not null group by Province_State having (Rate) is not null order by (Rate) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "Give me the county that has the (Value Entity) (Rate Entity) in (Day), (Month).":

        sql = "Select Admin2, Province_State from db1_given_date where Admin2 is not null and Province_State is not null group by Admin2, Province_State having (Rate) is not null order by (Rate) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "Provide me with the province that has the (Value Entity) (Rate Entity) in (Day), (Month).":

        sql = "Select Province_State, Country_Region from db1_given_date where Country_Region != 'US' and Province_State is not null and Country_Region is not null group by Province_State, Country_Region having (Rate) is not null order by (Rate) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "List the country that has the (Value Entity) (Rate Entity) in (Day), (Month).":

        sql = "Select Country_Region from db1_given_date where Country_Region is not null group by Country_Region having (Rate) is not null order by (Rate) (Value Entity)"

        given_date = dateconvert1(day, mon)
        sql = sql.replace("given_date", given_date)
        if rat == 'incidence rate':
            sql = sql.replace("(Rate)", 'SUM(Confirmed)/SUM(Confirmed*100000/Incidence_Rate) * 100000')
        elif rat == 'case-fatality rate':
            sql = sql.replace("(Rate)", 'SUM(Deaths)*100.0/SUM(Confirmed)')
        elif rat == 'recovery rate':
            sql = sql.replace("(Rate)", 'SUM(Recovered)*100.0./SUM(Confirmed)')
        else:
            sql = sql.replace("(Rate)", 'Testing_Rate')
        if val == 'highest' or val == 'most':
            sql = sql.replace('(Value Entity)', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('(Value Entity)', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})

    if real_question == "What is the (Rate Entity) in (State Entity)?":
        sql = "Select Rate Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0 /totalTestResultsIncrease")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease * 100.0/totalTestResultsIncrease")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive * 100.0/totalTestResults")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
        sql = sql.replace('current date', today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)
        bucket.update({'sql': sql})

    if real_question == "Give me the (Rate Entity) in (State Entity).":
        sql = "Select Rate Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0 /totalTestResultsIncrease")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease * 100.0/totalTestResultsIncrease")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive * 100.0/totalTestResults")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
        sql = sql.replace('current date', today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)
        bucket.update({'sql': sql})

    if real_question == "Provide me with the (Rate Entity) in (State Entity).":
        sql = "Select Rate Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0 /totalTestResultsIncrease")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease * 100.0/totalTestResultsIncrease")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive * 100.0/totalTestResults")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
        sql = sql.replace('current date', today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "List the (Rate Entity) in (State Entity).":
        sql = "Select Rate Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0 /totalTestResultsIncrease")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease * 100.0/totalTestResultsIncrease")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive * 100.0/totalTestResults")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
        sql = sql.replace('current date', today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Which state has the (Value Entity) number of people (Hospitalization Entity)?":
        sql = "Select state from db2state where date = 'given date' and (Null) order by Hospitalization Entity Column Value Entity"

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("given date", today)

        bucket.update({'sql': sql})

    if real_question == "Give me the state with the (Value Entity) number of people (Hospitalization Entity).":
        sql = "Select state from db2state where date = 'given date' and (Null) order by Hospitalization Entity Column Value Entity"

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("given date", today)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the state with the (Value Entity) number of people (Hospitalization Entity).":
        sql = "Select state from db2state where date = 'given date' and (Null) order by Hospitalization Entity Column Value Entity"

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("given date", today)

        bucket.update({'sql': sql})

    if real_question == "List the state with the (Value Entity) number of people (Hospitalization Entity).":
        sql = "Select state from db2state where date = 'given date' and (Null) order by Hospitalization Entity Column Value Entity"

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("given date", today)

        bucket.update({'sql': sql})

    if real_question == "How many people are (Hospitalization Entity) in (State Entity)?":

        sql = "Select Hospitalization Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("current date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Give me the number of people who are (Hospitalization Entity) in (State Entity).":

        sql = "Select Hospitalization Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("current date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of people who are (Hospitalization Entity) in (State Entity).":

        sql = "Select Hospitalization Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("current date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "List the number of people who are (Hospitalization Entity) in (State Entity).":

        sql = "Select Hospitalization Entity Column from db2State where date = 'current date' and state = \"State Entity\" "

        if hos == 'Currently in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCurrently")
            sql = sql.replace("(Null)", "inICUCurrently is not null")
        elif hos == 'Cumulatively in ICU':
            sql = sql.replace("Hospitalization Entity Column", "inICUCumulative")
            sql = sql.replace("(Null)", "inICUCumulative is not null")
        elif hos == 'Currently on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCurrently")
            sql = sql.replace("(Null)", "onVentilatorCurrently is not null")
        elif hos == 'Cumulatively on ventilators':
            sql = sql.replace("Hospitalization Entity Column", "onVentilatorCumulative")
            sql = sql.replace("(Null)", "onVentilatorCumulative is not null")
        elif hos == 'Cumulatively hospitalized':
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCumulative")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null")
        else:
            sql = sql.replace("Hospitalization Entity Column", "hospitalizedCurrently")
            sql = sql.replace("(Null)", "hospitalizedCurrently is not null")
        sql = sql.replace("current date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "What is the number of (Testing Entity) done in (State Entity) in (Day), (Month)?":

        sql = "Select Testing Entity Column from db2State where date = 'Time Entity' and state = \"State Entity\" "

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
        else:
            sql = sql.replace("Testing Entity Column", 'totalTestResultsIncrease')
        given_date = dateconvert2(day, mon)
        sql = sql.replace("Time Entity", given_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Give me the number of (Testing Entity) done in (State Entity) in (Day), (Month).":

        sql = "Select Testing Entity Column from db2State where date = 'Time Entity' and state = \"State Entity\" "

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
        else:
            sql = sql.replace("Testing Entity Column", 'totalTestResultsIncrease')
        given_date = dateconvert2(day, mon)
        sql = sql.replace("Time Entity", given_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of (Testing Entity) done in (State Entity) in (Month).":

        sql = "Select (Select Testing Entity Column from db2State where date = 'Time End' and state = \"State Entity\") - (Select Testing Entity Column from db2State where date = 'Time Start' and state = \"State Entity\")"

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
        else:
            break
        start_date, end_date = monthconvert2(mon)
        sql = sql.replace("Time End", end_date)
        sql = sql.replace("Time Start", start_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "List the number of (Testing Entity) done in (State Entity) in (Month).":

        sql = "Select (Select Testing Entity Column from db2State where date = 'Time End' and state = \"State Entity\") - (Select Testing Entity Column from db2State where date = 'Time Start' and state = \"State Entity\")"

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
        else:
            break
        start_date, end_date = monthconvert2(mon)
        sql = sql.replace("Time End", end_date)
        sql = sql.replace("Time Start", start_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Which state has the (Value Entity) (Testing Entity) in (Day), (Month)?":

        sql = "Select state from db2State where date = 'Time Entity' and (Null) order by Testing Entity Column Value Entity"

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
            sql = sql.replace("(Null)", "totalTestResults is not null")
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
            sql = sql.replace("(Null)", "positive is not null")
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
            sql = sql.replace("(Null)", "negative is not null")
        else:
            sql = sql.replace("Testing Entity Column", 'totalTestResultsIncrease')
            sql = sql.replace("(Null)", "totalTestResultsIncrease is not null")
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        given_date = dateconvert2(day, mon)
        sql = sql.replace("Time Entity", given_date)

        bucket.update({'sql': sql})

    if real_question == "Give me the state with the (Value Entity) (Testing Entity) in (Day), (Month).":

        sql = "Select state from db2State where date = 'Time Entity' and (Null) order by Testing Entity Column Value Entity"

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
            sql = sql.replace("(Null)", "totalTestResults is not null")
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
            sql = sql.replace("(Null)", "positive is not null")
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
            sql = sql.replace("(Null)", "negative is not null")
        else:
            sql = sql.replace("Testing Entity Column", 'totalTestResultsIncrease')
            sql = sql.replace("(Null)", "totalTestResultsIncrease is not null")
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        given_date = dateconvert2(day, mon)
        sql = sql.replace("Time Entity", given_date)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the state with the (Value Entity) (Testing Entity) in (Month).":

        sql = "Select t1.state from (Select state, Testing Entity Column from db2State where date =  'Time End' and (Null)) as t1 Inner Join (Select state, Testing Entity Column from db2State where date = 'Time Start' and (Null)) as t2 on t1.state = t2.state order by t1.Testing Entity Column-t2.Testing Entity Column Value Entity"

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
            sql = sql.replace("(Null)", "totalTestResults is not null")
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
            sql = sql.replace("(Null)", "positive is not null")
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
            sql = sql.replace("(Null)", "negative is not null")
        else:
            sql = sql.replace("Testing Entity Column", 'totalTestResultsIncrease')
            sql = sql.replace("(Null)", "totalTestResultsIncrease is not null")
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        start_date, end_date = monthconvert2(mon)
        sql = sql.replace("Time End", end_date)
        sql = sql.replace("Time Start", start_date)

        bucket.update({'sql': sql})

    if real_question == "List the state with the (Value Entity) (Testing Entity) in (Month).":

        sql = "Select t1.state from (Select state, Testing Entity Column from db2State where date =  'Time End' and (Null)) as t1 Inner Join (Select state, Testing Entity Column from db2State where date = 'Time Start' and (Null)) as t2 on t1.state = t2.state order by t1.Testing Entity Column-t2.Testing Entity Column Value Entity"

        if tes == 'total tests' or tes == 'total tests increased':
            sql = sql.replace("Testing Entity Column", 'totalTestResults')
            sql = sql.replace("(Null)", "totalTestResults is not null")
        elif tes == 'positive tests' or tes == 'positive tests increased':
            sql = sql.replace("Testing Entity Column", 'positive')
            sql = sql.replace("(Null)", "positive is not null")
        elif tes == 'negative tests' or tes == 'negative tests increased':
            sql = sql.replace("Testing Entity Column", 'negative')
            sql = sql.replace("(Null)", "negative is not null")
        else:
            sql = sql.replace("Testing Entity Column", 'totalTestResultsIncrease')
            sql = sql.replace("(Null)", "totalTestResultsIncrease is not null")
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        start_date, end_date = monthconvert2(mon)
        sql = sql.replace("Time End", end_date)
        sql = sql.replace("Time Start", start_date)

        bucket.update({'sql': sql})

    if real_question == "What percentage of (Cases) in (State Entity) are (Race)?":

        sql = "Select Case Entity Column_Race Entity Column from db2race where date = 'given date' and state = \"State Entity\" "

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'

        sql = sql.replace("Race Entity Column", race_input)
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Give me the percentage of (Cases) in (State Entity) that are (Race).":

        sql = "Select Case Entity Column_Race Entity Column from db2race where date = 'given date' and state = \"State Entity\" "

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'

        sql = sql.replace("Race Entity Column", race_input)
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the percentage of (Cases) in (State Entity) that are (Race).":

        sql = "Select Case Entity Column_Race Entity Column from db2race where date = 'given date' and state = \"State Entity\" "

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'

        sql = sql.replace("Race Entity Column", race_input)
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "List the percentage of (Cases) in (State Entity) that are (Race).":

        sql = "Select Case Entity Column_Race Entity Column from db2race where date = 'given date' and state = \"State Entity\" "

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'

        sql = sql.replace("Race Entity Column", race_input)
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Which state has the (Value Entity) percentage of (Race) (Cases)?":

        sql = "Select state from db2race where date = 'given date' and Case Entity Column_Race Entity Column is not null order by Case Entity Column_Race Entity Column Value Entity"

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        sql = sql.replace("given date", today)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Give me the state with the (Value Entity) percentage of (Race) (Cases).":

        sql = "Select state from db2race where date = 'given date' and Case Entity Column_Race Entity Column is not null order by Case Entity Column_Race Entity Column Value Entity"

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        sql = sql.replace("given date", today)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the state with the (Value Entity) percentage of (Race) (Cases).":

        sql = "Select state from db2race where date = 'given date' and Case Entity Column_Race Entity Column is not null order by Case Entity Column_Race Entity Column Value Entity"

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        sql = sql.replace("given date", today)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "List the state with the (Value Entity) percentage of (Race) (Cases).":

        sql = "Select state from db2race where date = 'given date' and Case Entity Column_Race Entity Column is not null order by Case Entity Column_Race Entity Column Value Entity"

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'

        sql = sql.replace("given date", today)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
            race_input = race_input + '*100.0/Cases_Total'
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
            race_input = race_input + '*100.0/Deaths_Total'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "How many (Race) (Cases) occurred in (State Entity) in (Day), (Month)?":

        sql = "Select Case Entity Column_Race Entity Column from db2race where date = 'Time Entity' and state = \"State Entity\" "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        given_date = dateconvert2(day, mon)
        sql = sql.replace("Time Entity", given_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Give me the number of (Race) (Cases) occurred in (State Entity) in (Day), (Month).":

        sql = "Select Case Entity Column_Race Entity Column from db2race where date = 'Time Entity' and state = \"State Entity\" "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        given_date = dateconvert2(day, mon)
        sql = sql.replace("Time Entity", given_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of (Race) (Cases) occurred in (State Entity) in (Month).":

        sql = "Select(Select Case Entity Column_Race Entity Column from db2race where date = 'Time End' and state = \"State Entity\") - (Select Case Entity Column_Race Entity Column from db2race where date = 'Time Start' and state = \"State Entity\") "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        start_date, end_date = monthconvert2(mon)
        sql = sql.replace("Time End", end_date)
        sql = sql.replace("Time Start", start_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "List the number of (Race) (Cases) occurred in (State Entity) in (Month).":

        sql = "Select(Select Case Entity Column_Race Entity Column from db2race where date = 'Time End' and state = \"State Entity\") - (Select Case Entity Column_Race Entity Column from db2race where date = 'Time Start' and state = \"State Entity\") "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        start_date, end_date = monthconvert2(mon)
        sql = sql.replace("Time End", end_date)
        sql = sql.replace("Time Start", start_date)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        if rac == 'African-American' or rac == 'Black':
            race_input = 'Black'
        elif rac == 'Asian':
            race_input = 'Asian'
        elif rac == 'White' or rac == 'Caucasian':
            race_input = 'White'
        elif rac == 'American Indian' or rac == 'Alaska Native' or rac == 'American Indian or Alaska Native':
            race_input = 'AIAN'
        elif rac == 'Pacific Islander' or rac == 'Native Hawaiian' or rac == 'Pacific Islander and Native Hawaiian':
            race_input = 'NHPI'
        elif rac == 'multiracial' or rac == 'mixed':
            race_input = 'Multiracial'
        else:
            race_input = 'Latinx'
        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Which state has the (Value Entity) (Rate Entity)?":

        sql = "Select state from db2state where date = 'current date' and (Null) order by Rate Entity Column Value Entity"

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "positiveIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease *100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "negativeIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive *100.0/totalTestResults")
            sql = sql.replace("(Null)", "positive is not null and totalTestResults is not null")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
            sql = sql.replace("(Null)", "negative is not null and totalTestResults is not null")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null and positive is not null")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        sql = sql.replace("current date", today)

        bucket.update({'sql': sql})

    if real_question == "Give me the state with the (Value Entity) (Rate Entity).":

        sql = "Select state from db2state where date = 'current date' and (Null) order by Rate Entity Column Value Entity"

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "positiveIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease *100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "negativeIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive *100.0/totalTestResults")
            sql = sql.replace("(Null)", "positive is not null and totalTestResults is not null")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
            sql = sql.replace("(Null)", "negative is not null and totalTestResults is not null")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null and positive is not null")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        sql = sql.replace("current date", today)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the state with the (Value Entity) (Rate Entity).":

        sql = "Select state from db2state where date = 'current date' and (Null) order by Rate Entity Column Value Entity"

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "positiveIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease *100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "negativeIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive *100.0/totalTestResults")
            sql = sql.replace("(Null)", "positive is not null and totalTestResults is not null")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
            sql = sql.replace("(Null)", "negative is not null and totalTestResults is not null")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null and positive is not null")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        sql = sql.replace("current date", today)

        bucket.update({'sql': sql})

    if real_question == "List the state with the (Value Entity) (Rate Entity).":

        sql = "Select state from db2state where date = 'current date' and (Null) order by Rate Entity Column Value Entity"

        if rat == 'daily percent positive rate':
            sql = sql.replace("Rate Entity Column", "positiveIncrease * 100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "positiveIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'daily percent negative rate':
            sql = sql.replace("Rate Entity Column", "negativeIncrease *100.0/totalTestResultsIncrease")
            sql = sql.replace("(Null)", "negativeIncrease is not null and totalTestResultsIncrease is not null")
        elif rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "positive *100.0/totalTestResults")
            sql = sql.replace("(Null)", "positive is not null and totalTestResults is not null")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "negative * 100.0/totalTestResults")
            sql = sql.replace("(Null)", "negative is not null and totalTestResults is not null")
        else:
            sql = sql.replace("Rate Entity Column", "hospitalizedCumulative * 100.0/positive")
            sql = sql.replace("(Null)", "hospitalizedCumulative is not null and positive is not null")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        sql = sql.replace("current date", today)

        bucket.update({'sql': sql})

    if real_question == "What is the racial breakdown of (Cases) in (State Entity)?":

        sql = "Select Case Entity Column_Total,Case Entity Column_White, Case Entity Column_Black,Case Entity Column_LatinX, Case Entity Column_Asian,Case Entity Column_NHPI, Case Entity Column_Multiracial, Case Entity Column_Other, Case Entity Column_Unknown from db2race where date = 'given date' and state = \"State Entity\" "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Give me the racial breakdown of (Cases) in (State Entity).":

        sql = "Select Case Entity Column_Total,Case Entity Column_White, Case Entity Column_Black,Case Entity Column_LatinX, Case Entity Column_Asian,Case Entity Column_NHPI, Case Entity Column_Multiracial, Case Entity Column_Other, Case Entity Column_Unknown from db2race where date = 'given date' and state = \"State Entity\" "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the racial breakdown of (Cases) in (State Entity).":

        sql = "Select Case Entity Column_Total,Case Entity Column_White, Case Entity Column_Black,Case Entity Column_LatinX, Case Entity Column_Asian,Case Entity Column_NHPI, Case Entity Column_Multiracial, Case Entity Column_Other, Case Entity Column_Unknown from db2race where date = 'given date' and state = \"State Entity\" "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "List the racial breakdown of (Cases) in (State Entity).":

        sql = "Select Case Entity Column_Total,Case Entity Column_White, Case Entity Column_Black,Case Entity Column_LatinX, Case Entity Column_Asian,Case Entity Column_NHPI, Case Entity Column_Multiracial, Case Entity Column_Other, Case Entity Column_Unknown from db2race where date = 'given date' and state = \"State Entity\" "

        if cas.find('cases') >= 0:
            sql = sql.replace("Case Entity Column", "Cases")
        else:
            sql = sql.replace("Case Entity Column", "Deaths")
        sql = sql.replace("given date", today)
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        bucket.update({'sql': sql})

    if real_question == "What is the number of (Bed Entity) in (State Entity)?":

        sql = "Select Sum(Bed Entity Column) From db3 Where STATE_Name = \"State Entity\""

        if bed == 'staffed beds':
            sql = sql.replace("Bed Entity Column", "NUM_STAFFED_BEDS")
        elif bed == 'licensed beds':
            sql = sql.replace("Bed Entity Column", "NUM_LICENSED_BEDS")
        elif bed == 'ICU beds':
            sql = sql.replace("Bed Entity Column", "NUM_ICU_BEDS")
        sql = sql.replace("State Entity", state)

        bucket.update({'sql': sql})

    if real_question == "Give me the number of (Bed Entity) in (State Entity).":

        sql = "Select Sum(Bed Entity Column) From db3 Where STATE_Name = \"State Entity\""

        if bed == 'staffed beds':
            sql = sql.replace("Bed Entity Column", "NUM_STAFFED_BEDS")
        elif bed == 'licensed beds':
            sql = sql.replace("Bed Entity Column", "NUM_LICENSED_BEDS")
        elif bed == 'ICU beds':
            sql = sql.replace("Bed Entity Column", "NUM_ICU_BEDS")
        sql = sql.replace("State Entity", state)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of (Bed Entity) in (County Entity), (State Entity).":

        sql = "Select SUM(Bed Entity Column) from db3 where STATE_Name = \"State Entity\" and COUNTY_Name = \"County Entity\""

        if bed == 'staffed beds':
            sql = sql.replace("Bed Entity Column", "NUM_STAFFED_BEDS")
        elif bed == 'licensed beds':
            sql = sql.replace("Bed Entity Column", "NUM_LICENSED_BEDS")
        elif bed == 'ICU beds':
            sql = sql.replace("Bed Entity Column", "NUM_ICU_BEDS")
        sql = sql.replace("County Entity", county_name)
        sql = sql.replace("State Entity", state_name)

        bucket.update({'sql': sql})

    if real_question == "List the number of (Bed Entity) in (County Entity), (State Entity).":

        sql = "Select SUM(Bed Entity Column) from db3 where STATE_Name = \"State Entity\" and COUNTY_Name = \"County Entity\""

        if bed == 'staffed beds':
            sql = sql.replace("Bed Entity Column", "NUM_STAFFED_BEDS")
        elif bed == 'licensed beds':
            sql = sql.replace("Bed Entity Column", "NUM_LICENSED_BEDS")
        elif bed == 'ICU beds':
            sql = sql.replace("Bed Entity Column", "NUM_ICU_BEDS")
        sql = sql.replace("County Entity", county_name)
        sql = sql.replace("State Entity", state_name)

        bucket.update({'sql': sql})

    if real_question == "What is the breakdown of (Cases) by (Demographic Entity) in the United States?":

        sql = "Select * from table_name"

        if cas == 'cases' or cas == 'confirmed cases':
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4casesex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4caserace'
            else:
                table_name = 'db4caseage'
        else:
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4deathsex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4deathrace'
            else:
                table_name = 'db4deathage'
        sql = sql.replace("table_name", table_name)

        bucket.update({'sql': sql})

    if real_question == "Give me the breakdown of (Cases) by (Demographic Entity) in the United States.":

        sql = "Select * from table_name"

        if cas == 'cases' or cas == 'confirmed cases':
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4casesex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4caserace'
            else:
                table_name = 'db4caseage'
        else:
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4deathsex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4deathrace'
            else:
                table_name = 'db4deathage'
        sql = sql.replace("table_name", table_name)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the breakdown of (Cases) by (Demographic Entity) in the United States.":

        sql = "Select * from table_name"

        if cas == 'cases' or cas == 'confirmed cases':
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4casesex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4caserace'
            else:
                table_name = 'db4caseage'
        else:
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4deathsex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4deathrace'
            else:
                table_name = 'db4deathage'
        sql = sql.replace("table_name", table_name)

        bucket.update({'sql': sql})

    if real_question == "List the breakdown of (Cases) by (Demographic Entity) in the United States.":

        sql = "Select * from table_name"

        if cas == 'cases' or cas == 'confirmed cases':
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4casesex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4caserace'
            else:
                table_name = 'db4caseage'
        else:
            if dem == 'sex' or dem == 'gender':
                table_name = 'db4deathsex'
            elif dem == 'race' or dem == 'race and ethnicity' or dem == 'ethnicity':
                table_name = 'db4deathrace'
            else:
                table_name = 'db4deathage'
        sql = sql.replace("table_name", table_name)

        bucket.update({'sql': sql})

    if real_question == "Which (Demographic Entity) has the (Value Entity) (Amount Entity) (Cases) in the United States?":

        sql = "Select Demographic Entity, Amount Entity from table name Order by Amount Entity Value Entity"

        if cas == 'confirmed cases' or cas == 'cases':
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4casesex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4caseage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4caserace")
        else:
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4deathsex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4deathage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4deathrace")
        if amo == 'percentage of':
            sql = sql.replace("Amount Entity", "Count")
        else:
            sql = sql.replace("Amount Entity", "Count")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        bucket.update({'sql': sql})

    if real_question == "Give me the (Demographic Entity) that has the (Value Entity) (Amount Entity) (Cases) in the United States.":

        sql = "Select Demographic Entity, Amount Entity from table name Order by Amount Entity Value Entity"

        if cas == 'confirmed cases' or cas == 'cases':
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4casesex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4caseage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4caserace")
        else:
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4deathsex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4deathage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4deathrace")
        if amo == 'percentage of':
            sql = sql.replace("Amount Entity", "Count")
        else:
            sql = sql.replace("Amount Entity", "Count")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        bucket.update({'sql': sql})

    if real_question == "Provide me with the (Demographic Entity) that has the (Value Entity) (Amount Entity) (Cases) in the United States.":

        sql = "Select Demographic Entity, Amount Entity from table name Order by Amount Entity Value Entity"

        if cas == 'confirmed cases' or cas == 'cases':
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4casesex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4caseage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4caserace")
        else:
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4deathsex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4deathage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4deathrace")
        if amo == 'percentage of':
            sql = sql.replace("Amount Entity", "Count")
        else:
            sql = sql.replace("Amount Entity", "Count")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        bucket.update({'sql': sql})

    if real_question == "List the (Demographic Entity) that has the (Value Entity) (Amount Entity) (Cases) in the United States.":

        sql = "Select Demographic Entity, Amount Entity from table name Order by Amount Entity Value Entity"

        if cas == 'confirmed cases' or cas == 'cases':
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4casesex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4caseage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4caserace")
        else:
            if dem == 'sex' or dem == 'gender':
                sql = sql.replace("Demographic Entity", "Sex")
                sql = sql.replace("table name", "db4deathsex")
            elif dem == 'age' or dem == 'age group':
                sql = sql.replace("Demographic Entity", "Age_Group")
                sql = sql.replace("table name", "db4deathage")
            else:
                sql = sql.replace("Demographic Entity", "Race_Ethnicity")
                sql = sql.replace("table name", "db4deathrace")
        if amo == 'percentage of':
            sql = sql.replace("Amount Entity", "Count")
        else:
            sql = sql.replace("Amount Entity", "Count")

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        bucket.update({'sql': sql})

    if real_question == "What is the total forecasted number of deaths in (State Entity) in the next (x) days?":

        sql = "Select Max(point) from db4forecaststate where target_week_end_date = 'Time Entity' and location_name = \"State Entity\""

        sql = sql.replace("State Entity", state)
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "Provide me with the total forecasted number of deaths in (State Entity) in the next (x) days.":

        sql = "Select Max(point) from db4forecaststate where target_week_end_date = 'Time Entity' and location_name = \"State Entity\""

        sql = sql.replace("State Entity", state)
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "Give me the total forecasted number of deaths in (State Entity) in the next (x) days.":

        sql = "Select Max(point) from db4forecaststate where target_week_end_date = 'Time Entity' and location_name = \"State Entity\""

        sql = sql.replace("State Entity", state)
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "List the total forecasted number of deaths in (State Entity) in the next (x) days.":

        sql = "Select Max(point) from db4forecaststate where target_week_end_date = 'Time Entity' and location_name = \"State Entity\""

        sql = sql.replace("State Entity", state)
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "Which state will have the (Value Entity) total forecasted number of deaths in the next (x) days?":

        sql = "Select location_name, Max(point) from db4forecaststate WHERE target_week_end_date = 'Time Entity' and location_name != 'National' group by location_name order by Max(point) asc/desc limit 0,1"

        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "Provide me with the state that have the (Value Entity) total forecasted number of deaths in the next (x) days.":

        sql = "Select location_name, Max(point) from db4forecaststate WHERE target_week_end_date = 'Time Entity' and location_name != 'National' group by location_name order by Max(point) asc/desc limit 0,1"

        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "Give me the  state that have the (Value Entity) total forecasted number of deaths in the next (x) days.":

        sql = "Select location_name, Max(point) from db4forecaststate WHERE target_week_end_date = 'Time Entity' and location_name != 'National' group by location_name order by Max(point) asc/desc limit 0,1"

        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "List the  state that have the (Value Entity) total forecasted number of deaths in the next (x) days.":

        sql = "Select location_name, Max(point) from db4forecaststate WHERE target_week_end_date = 'Time Entity' and location_name != 'National' group by location_name order by Max(point) asc/desc limit 0,1"

        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        today = datetime.date.today()
        num_day = int(num)
        future_date = today + datetime.timedelta(days=num_day)
        if future_date.weekday() == 5:
            sql = sql.replace("Time Entity", str(future_date))
        elif future_date.weekday() == 6:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=6)))
        else:
            sql = sql.replace("Time Entity", str(future_date + datetime.timedelta(days=5 - future_date.weekday())))

        bucket.update({'sql': sql})

    if real_question == "What is the percentage change in (Mobility Entity) in (State Entity) in (Day), (Month)?":

        sql = "Select (Mobility) FROM db4mobility WHERE date = \"given date\" AND country_region = \"United States\" AND sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\""

        given_date = dateconvert6(day, mon)
        sql = sql.replace("given date", given_date)
        sql = sql.replace("State name", state)
        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")

        bucket.update({'sql': sql})

    if real_question == "Give me the percentage change in (Mobility Entity) in (State Entity) in (Day), (Month).":

        sql = "Select (Mobility) FROM db4mobility WHERE date = \"given date\" AND country_region = \"United States\" AND sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\""

        given_date = dateconvert6(day, mon)
        sql = sql.replace("given date", given_date)
        sql = sql.replace("State name", state)
        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")

        bucket.update({'sql': sql})

    if real_question == "Provide me with the percentage change in (Mobility Entity) in (County Entity) (State Entity) in (Month).":

        sql = "Select (Select (Mobility) from db4mobility where date = 'end date' and country_region = 'United States' and sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\") - (Select (Mobility) from db4mobility where date = 'start date' and country_region = 'United States' and sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\")"

        sql = sql.replace("State name", state_name + "\" AND sub_region_2 = \"" + county_name + " County")
        start_date, end_date = monthconvert4(mon)
        sql = sql.replace("end date", end_date)
        sql = sql.replace("start date", start_date)
        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")

        bucket.update({'sql': sql})

    if real_question == "List the percentage change in (Mobility Entity) in (County Entity) (State Entity) in (Month).":

        sql = "Select (Select (Mobility) from db4mobility where date = 'end date' and country_region = 'United States' and sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\") - (Select (Mobility) from db4mobility where date = 'start date' and country_region = 'United States' and sub_region_1 = \"State name\" and iso_3166_2_code LIKE \"US-%\")"

        sql = sql.replace("State name", state_name + "\" AND sub_region_2 = \"" + county_name + " County")
        start_date, end_date = monthconvert4(mon)
        sql = sql.replace("end date", end_date)
        sql = sql.replace("start date", start_date)
        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")

        bucket.update({'sql': sql})

    if real_question == "Which state had the (Value Entity) percentage change in (Mobility Entity) today?":

        sql = "Select sub_region_1, (Mobility) from db4mobility where date = 'Time Entity' and country_region = 'United States' and iso_3166_2_code like \"US-%\" and (Mobility) is not null order by (Mobility) asc/desc limit 0,1"

        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")
        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        today = datetime.date.today()
        sql = sql.replace("Time Entity", str(today))

        bucket.update({'sql': sql})

    if real_question == "Give me the state that had the (Value Entity) percentage change in (Mobility Entity) today.":

        sql = "Select sub_region_1, (Mobility) from db4mobility where date = 'Time Entity' and country_region = 'United States' and iso_3166_2_code like \"US-%\" and (Mobility) is not null order by (Mobility) asc/desc limit 0,1"

        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")
        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        today = datetime.date.today()
        sql = sql.replace("Time Entity", str(today))

        bucket.update({'sql': sql})

    if real_question == "Give me the county that had the (Value Entity) percentage change in (Mobility Entity) in (Month).":

        sql = """Select t1.sub_region_2, t1.(Mobility)-t2.(Mobility) from(Select sub_region_2, (Mobility)  from db4mobility where date = 'end date' and country_region = 'United States' and sub_region_2 is not null and (Mobility) is not null) as t1 Inner Join (Select sub_region_2, (Mobility)  from db4mobility where date = 'start date' and country_region = 'United States' and (Mobility) is not null) as t2 on t1 sub_region_2=t2.sub_region_2 order by t1.(Mobility)-t2.(Mobility) asc/desc limit 0,1"""

        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")
        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        start_date, end_date = monthconvert4(mon)
        sql = sql.replace("end date", end_date)
        sql = sql.replace("start date", start_date)


        bucket.update({'sql': sql})

    if real_question == "List the county that had the (Value Entity) percentage change in (Mobility Entity) in (Month).":
        sql = """Select t1.sub_region_2, t1.(Mobility)-t2.(Mobility) from(Select sub_region_2, (Mobility)  from db4mobility where date = 'end date' and country_region = 'United States' and sub_region_2 is not null and (Mobility) is not null) as t1 Inner Join (Select sub_region_2, (Mobility)  from db4mobility where date = 'start date' and country_region = 'United States' and (Mobility) is not null) as t2 on t1 sub_region_2=t2.sub_region_2 order by t1.(Mobility)-t2.(Mobility) asc/desc limit 0,1"""

        if mob == 'retail and recreation':
            sql = sql.replace("(Mobility)", "retail_and_recreation_percent_change_from_baseline")
        elif mob == 'grocery and pharmacy':
            sql = sql.replace("(Mobility)", "grocery_and_pharmacy_percent_change_from_baseline")
        elif mob == 'parks':
            sql = sql.replace("(Mobility)", "parks_percent_change_from_baseline")
        elif mob == 'transit stations':
            sql = sql.replace("(Mobility)", "transit_stations_percent_change_from_baseline")
        elif mob == 'workplaces':
            sql = sql.replace("(Mobility)", "workplaces_percent_change_from_baseline")
        else:
            sql = sql.replace("(Mobility)", "residential_percent_change_from_baseline")
        if val == 'highest' or val == 'most':
            sql = sql.replace("asc/desc", "desc")
        else:
            sql = sql.replace("asc/desc", "asc")
        start_date, end_date = monthconvert4(mon)
        sql = sql.replace("end date", end_date)
        sql = sql.replace("start date", start_date)

        bucket.update({'sql': sql})

        if real_question == "Which county in (State Entity) has the (Value Entity) percentage of (Race Entity) deaths?":
            sql = "Select County_Name from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = 'State Entity' order by Race Entity Column Value Entity"

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
        while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                "Pacific Islander and Native Hawaiian") >= 0 or (
                (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                "Non-Hispanic") >= 0):
            specific_race = random.choice(data3['Race'])
        if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
            race_input = "Non_Hispanic_Black"
        elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
            race_input = "Hispanic"
        elif specific_race.find("Asian") >= 0:
            race_input = "Non_Hispanic_Asian"
        elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
            race_input = "Non_Hispanic_AIAN"
        else:
            race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:
            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')
        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Give me the county in (State Entity) has the (Value Entity) percentage of (Race Entity) deaths.":

        sql = "Select County_Name from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = 'State Entity' order by Race Entity Column Value Entity"
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the county in (State Entity) that has the (Value Entity) percentage of (Race Entity) deaths.":

        sql = "Select County_Name from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = 'State Entity' order by Race Entity Column Value Entity"

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "List the county in (State Entity) that has the (Value Entity) percentage of (Race Entity) deaths.":

        sql = "Select County_Name from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = 'State Entity' order by Race Entity Column Value Entity"

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        state_abbreviation = state_key[state_val.index(state)]
        sql = sql.replace("State Entity", state_abbreviation)

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "What percentage of Covid-19 deaths in (County Entity), (State Entity) are from (Race Entity)?":

        sql = "Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and County_Name = \"County Entity\" and State = \"State Entity\""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Give me the percentage of Covid-19 deaths in (County Entity), (State Entity) that are from (Race Entity).":

        sql = "Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and County_Name = \"County Entity\" and State = \"State Entity\""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the percentage of Covid-19 deaths in (County Entity), (State Entity) that are from (Race Entity).":

        sql = "Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and County_Name = \"County Entity\" and State = \"State Entity\""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "List the percentage of Covid-19 deaths in (County Entity), (State Entity) that are from (Race Entity).":

        sql = "Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and County_Name = \"County Entity\" and State = \"State Entity\""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "How many (Race Entity) deaths occured in (County Entity), (State Entity)?":

        sql = "Select Round((Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\") * (Select Deaths from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\"))"

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Give me the number of (Race Entity) deaths occured in (County Entity), (State Entity).":

        sql = "Select Round((Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\") * (Select Deaths from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\"))"

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of (Race Entity) deaths occured in (County Entity), (State Entity).":

        sql = "Select Round((Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\") * (Select Deaths from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\"))"

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "List the number of (Race Entity) deaths occured in (County Entity), (State Entity).":

        sql = "Select Round((Select Race Entity Column from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\") * (Select Deaths from db5 where Indicator = 'Distribution of COVID-19 deaths (%)' and State = \"State Entity\" and County_Name = \"County Entity\"))"

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        specific_race = rac
        if rac == "people of color":
            race_input = "Non_Hispanic_Black"
        else:
            specific_race = rac
            while specific_race.find("multiracial") >= 0 or specific_race.find("mixed") >= 0 or specific_race.find(
                    "Pacific Islander") >= 0 or specific_race.find("Native Hawaiian") >= 0 or specific_race.find(
                    "Pacific Islander and Native Hawaiian") >= 0 or (
                    (specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0) and rac.find(
                    "Non-Hispanic") >= 0):
                specific_race = random.choice(data3['Race'])
            if specific_race.find("African-American") >= 0 or specific_race.find("Black") >= 0:
                race_input = "Non_Hispanic_Black"
            elif specific_race.find("Hispanic") >= 0 or specific_race.find("Latino") >= 0:
                race_input = "Hispanic"
            elif specific_race.find("Asian") >= 0:
                race_input = "Non_Hispanic_Asian"
            elif specific_race.find("Alaska Native") >= 0 or specific_race.find(
                    "American Indian or Alaska Native") >= 0 or specific_race.find("American Indian") >= 0:
                race_input = "Non_Hispanic_AIAN"
            else:
                race_input = "Non_Hispanic_White"

        if rac.find("people of color") >= 0:

            real_sub = rac
        elif rac.find("people") < 0:
            if specific_race == 'American Indian or Alaska Native':
                real_sub = rac.replace("(race)", 'American Indians or Alaska Natives')
            else:
                real_sub = rac.replace("(race)", specific_race + 's')

        else:
            real_sub = rac.replace("(race)", specific_race)

        sql = sql.replace("Race Entity Column", race_input)

        bucket.update({'sql': sql})

    if real_question == "What is the racial breakdown of Covid-19 deaths in (County Entity), (State Entity)?":
        sql = """Select Deaths, Non_Hispanic_White, Non_Hispanic_Black, Non_Hispanic_AIAN, Non_Hispanic_Asian, Other, Hispanic from db5 where Indicator = \"Distribution of COVID-19 deaths (%)\" and State = \"State Entity\" and County_Name = \"County Entity\""""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        bucket.update({'sql': sql})

    if real_question == "Give me the racial breakdown of Covid-19 deaths in (County Entity), (State Entity).":
        sql = """Select Deaths, Non_Hispanic_White, Non_Hispanic_Black, Non_Hispanic_AIAN, Non_Hispanic_Asian, Other, Hispanic from db5 where Indicator = \"Distribution of COVID-19 deaths (%)\" and State = \"State Entity\" and County_Name = \"County Entity\""""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

        bucket.update({'sql': sql})

    if real_question == "Provide me with the racial breakdown of Covid-19 deaths in (County Entity), (State Entity).":
        sql = """Select Deaths, Non_Hispanic_White, Non_Hispanic_Black, Non_Hispanic_AIAN, Non_Hispanic_Asian, Other, Hispanic from db5 where Indicator = \"Distribution of COVID-19 deaths (%)\" and State = \"State Entity\" and County_Name = \"County Entity\""""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

    bucket.update({'sql': sql})

    if real_question == "List the racial breakdown of Covid-19 deaths in (County Entity), (State Entity).":
        sql = """Select Deaths, Non_Hispanic_White, Non_Hispanic_Black, Non_Hispanic_AIAN, Non_Hispanic_Asian, Other, Hispanic from db5 where Indicator = \"Distribution of COVID-19 deaths (%)\" and State = \"State Entity\" and County_Name = \"County Entity\""""

        state_abbreviation = state_key[state_val.index(state_name)]
        sql = sql.replace("State Entity", state_abbreviation)
        sql = sql.replace("County Entity", county_name + " County")

    bucket.update({'sql': sql})

    if real_question == "What are the number of (Testing Entity) done by (Country) in (Day), (Month)?":

        sql = "Select Testing Entity Column from db6 where Entity = \"Country Name\" and Date = 'Time Entity'"

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)

        sql = sql.replace("Country Name", cou)
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

        bucket.update({'sql': sql})

    if real_question == "Give me the number of (Testing Entity) done by (Country) in (Day), (Month).":

        sql = "Select Testing Entity Column from db6 where Entity = \"Country Name\" and Date = 'Time Entity'"

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)

        sql = sql.replace("Country Name", cou)
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

        bucket.update({'sql': sql})

    if real_question == "Provide me with the number of (Testing Entity) done by (Country) in (Month).":

        sql = "Select (Select Testing Entity Column from db6 where date = 'Time End' and Entity = \" Country Entity\") - (Select Testing Entity Column from db6 where date = 'Time Start' and Entity = \"Country Entity\")"

        time_start, time_end = monthconvert4(mon)
        sql = sql.replace("Time End", time_end)
        sql = sql.replace("Time Start", time_start)

        sql = sql.replace("Country Entity", cou)
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

        bucket.update({'sql': sql})

    if real_question == "List the number of (Testing Entity) done by (Country) in (Month).":

        sql = "Select (Select Testing Entity Column from db6 where date = 'Time End' and Entity = \" Country Entity\") - (Select Testing Entity Column from db6 where date = 'Time Start' and Entity = \"Country Entity\")"

        time_start, time_end = monthconvert4(mon)
        sql = sql.replace("Time End", time_end)
        sql = sql.replace("Time Start", time_start)

        sql = sql.replace("Country Entity", cou)
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

        bucket.update({'sql': sql})

    if real_question == "What is the (Rate Entity) in (Country) in (Day), (Month)?":

        sql = "Select Rate Entity Column from db6file2 where date = 'Time Entity' and Entity = \"Country Entity\""

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        sql = sql.replace("Country Entity", cou)
        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")

        bucket.update({'sql': sql})

    if real_question == "Give me the (Rate Entity) in (Country) in (Day), (Month).":

        sql = "Select Rate Entity Column from db6file2 where date = 'Time Entity' and Entity = \"Country Entity\""

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        sql = sql.replace("Country Entity", cou)
        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")

        bucket.update({'sql': sql})

    if real_question == "Provide me with the (Rate Entity) in (Country) in (Day), (Month).":

        sql = "Select Rate Entity Column from db6file2 where date = 'Time Entity' and Entity = \"Country Entity\""

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        sql = sql.replace("Country Entity", cou)
        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")

        bucket.update({'sql': sql})

    if real_question == "List the (Rate Entity) in (Country) in (Day), (Month).":

        sql = "Select Rate Entity Column from db6file2 where date = 'Time Entity' and Entity = \"Country Entity\""

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        sql = sql.replace("Country Entity", cou)
        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")

        bucket.update({'sql': sql})

    if real_question == "Which country has the (Value Entity) (Testing Entity) in (Day), (Month)?":

        sql = "Select Entity from db6 where date = 'Time Entity' order by Testing Entity Column Value Entity"

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

    bucket.update({'sql': sql})

    if real_question == "Give me the country that has the (Value Entity) (Testing Entity) in (Day), (Month).":

        sql = "Select Entity from db6 where date = 'Time Entity' order by Testing Entity Column Value Entity"

        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

        bucket.update({'sql': sql})

    if real_question == "Provide me with the country that has the (Value Entity) (Testing Entity) in (Month).":

        sql = "Select e1 from (Select Entity as E1, Testing Entity Column as tot1 from db6 where date = 'Time End') as t1 Inner Join (Select Entity as e2, Testing Entity Column as tot2 from db6 where date = 'Time Start') as t2 on t1.e1=t2.e2 order by t1.tot1-t2.tot2 Value Entity"

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

        time_start, time_end = monthconvert4(mon)
        sql = sql.replace("Time End", time_end)
        sql = sql.replace("Time Start", time_start)

        bucket.update({'sql': sql})

    if real_question == "List the country that has the (Value Entity) (Testing Entity) in (Month).":

        sql = "Select e1 from (Select Entity as E1, Testing Entity Column as tot1 from db6 where date = 'Time End') as t1 Inner Join (Select Entity as e2, Testing Entity Column as tot2 from db6 where date = 'Time Start') as t2 on t1.e1=t2.e2 order by t1.tot1-t2.tot2 Value Entity"

        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        if tes == 'daily tests':
            sql = sql.replace("Testing Entity Column", "New_Test")
            sql = sql.replace("db6", "db6file4")
        else:
            sql = sql.replace("Testing Entity Column", "Total")

        time_start, time_end = monthconvert4(mon)
        sql = sql.replace("Time End", time_end)
        sql = sql.replace("Time Start", time_start)

        bucket.update({'sql': sql})

    if real_question == "Which country has the (Value Entity) (Rate Entity) in (Day), (Month)?":

        sql = "Select Entity from db6file2 where date = 'Time Entity' order by Rate Entity Column Value Entity"

        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")
        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        bucket.update({'sql': sql})

    if real_question == "Give me the country that has the (Value Entity) (Rate Entity) in (Day), (Month).":

        sql = "Select Entity from db6file2 where date = 'Time Entity' order by Rate Entity Column Value Entity"

        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")
        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        bucket.update({'sql': sql})

    if real_question == "Provide me with the country that has the (Value Entity) (Rate Entity) in (Day), (Month).":

        sql = "Select Entity from db6file2 where date = 'Time Entity' order by Rate Entity Column Value Entity"

        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")
        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')

        bucket.update({'sql': sql})

    if real_question == "List the country that has the (Value Entity) (Rate Entity) in (Day), (Month).":

        sql = "Select Entity from db6file2 where date = 'Time Entity' order by Rate Entity Column Value Entity"

        if rat == 'percent positive rate':
            sql = sql.replace("Rate Entity Column", "pos_rate")
        elif rat == 'percent negative rate':
            sql = sql.replace("Rate Entity Column", "100-pos_rate")
        else:
            sql = sql.replace("Rate Entity Column", "daily_rate")
            sql = sql.replace("db6file2", "db6file3")
        given_date = dateconvert6(day, mon)
        sql = sql.replace("Time Entity", given_date)
        if val == 'highest' or val == 'most':
            sql = sql.replace('Value Entity', 'desc limit 0' + ', 1')
        else:
            sql = sql.replace('Value Entity', 'asc limit 0' + ', 1')
        bucket.update({'sql': sql})







