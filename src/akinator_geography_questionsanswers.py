import numpy as np

from mpl_toolkits.basemap import Basemap
import akinator_model

import json
import re
import os

script_path = os.path.dirname(os.path.abspath( __file__ ))
questionsfile = os.path.abspath(os.path.join(script_path, '../questions.json'))

def add_demographic_info_from_shape_data(akinator, mapinfo):    
    incomeyes = [0.90, 0.1]
    incomeno = [0.1, 0.90]
    
    defaultyes = [0.75, 0.25]
    defaultno = [0.25, 0.75]
    
    qkey = akinator.addquestion('Is this country considered a high income country?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("1.") or info['INCOME_GRP'].startswith("2."):
            akinator.addanswer(qkey, countryname, incomeyes)
        else:
            akinator.addanswer(qkey, countryname, incomeno)
    
    qkey = akinator.addquestion('Is this country considered a low income country?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("4.") or info['INCOME_GRP'].startswith("5."):
            akinator.addanswer(qkey, countryname, incomeyes)
        else:
            akinator.addanswer(qkey, countryname, incomeno)
    
    """
    continents = ['Asia', 'South America', 'Africa', 'Europe', 'North America', 'Oceania', 'Antarctica']
    continents.sort()
    
    # is you country in X continent?
    for continent in continents:
        qkey = akinator.addquestion('Is your location in %s?' % continent)
        for countryname in mapinfo.locationlist:
            info = mapinfo.infobycountryname[countryname]
            if info['CONTINENT'] == continent:
                akinator.addanswer(qkey, countryname, defaultyes)
            else:
                akinator.addanswer(qkey, countryname, defaultno)
    """
    
    qkey = akinator.addquestion('Is the population less than 1,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] < 1000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
    qkey = akinator.addquestion('Is the population less than 10,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] < 10000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
            
    qkey = akinator.addquestion('Is the population greater than 50,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 50000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
    qkey = akinator.addquestion('Is the population greater than 100,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 100000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
            
    qkey = akinator.addquestion('Is the population greater than 300,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 300000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
            
def add_additional_questions(akinator, mapinfo):     
    
    """
    Left hand drive countries
    """
    leftdrivingcountries = ["Anguilla", "Antigua and Barbuda", "Australia", "Bangladesh", "Barbados", "Bhutan", "Botswana", "Brunei", "Cyprus", "Dominica", "eSwatini", "Fiji", "Grenada", "Guernsey", "Guyana", "Hong Kong", "India", "Indonesia", "Ireland",  "Jamaica", "Japan", "Jersey", "Kenya", "Kiribati", "Lesotho", "Malawi", "Malaysia", "Maldives", "Malta", "Mauritius", "Mozambique", "Namibia", "Nauru", "Nepal", "New Zealand", "Pakistan", "Papua New Guinea", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "Seychelles", "Singapore", "Solomon Islands", "South Africa", "Sri Lanka", "Saint Lucia", "Saint Vincent and the Grenadines", "Suriname", "Tanzania", "Thailand", "Tonga", "Trinidad and Tobago", "Tuvalu", "Uganda", "United Kingdom", "Zambia", "Zimbabwe"]
    notneeded = ["Isle Of Man","Northern Ireland", "Scotland", "Wales", "Swaziland", "Antigua", "Bahamas", "Tasmania"]
    sortedcountries = list(mapinfo.infobycountryname.keys())
    sortedcountries.sort()
    print(sortedcountries)
    for country in leftdrivingcountries:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
    
    qkey = akinator.addquestion('Does your country drive on the left side of the road?')
    for countryname in mapinfo.infobycountryname:
        if countryname in leftdrivingcountries:
            akinator.addanswer(qkey, countryname, [0.75, 0.25])
        else:
            akinator.addanswer(qkey, countryname, [0.25, 0.75])
    
    """
    Countries with nuclear weapons
    """
    hasnuclearweapons = ["United States of America", "Russia", "United Kingdom", "France", "China", "India", "Pakistan", "North Korea", "Israel"]
    if country in hasnuclearweapons:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
    qkey = akinator.addquestion('Does your country currently possess nuclear weapons?')
    for countryname in mapinfo.infobycountryname:
        if countryname in hasnuclearweapons:
            akinator.addanswer(qkey, countryname, [0.9, 0.1])
        else:
            akinator.addanswer(qkey, countryname, [0.1, 0.9])
            
    """
    Countries that have participated in Eurovision
    """
    participatedineurovsion = ["Albania","Armenia","Australia","Austria","Azerbaijan","Belarus","Belgium","Bosnia and Herzegovina","Bulgaria","Croatia","Cyprus","Czech Republic","Denmark","Estonia","Finland","France","Georgia","Germany","Greece","Hungary","Iceland","Ireland","Israel","Italy","Latvia","Lithuania","Malta","Moldova","Montenegro","Netherlands","North Macedonia","Norway","Poland","Portugal","Romania","Russia","San Marino","Serbia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Turkey","Ukraine","United Kingdom","Andorra","Macedonia","Monaco","Serbia and Montenegro","Luxembourg","Yugoslavia","Morocco"]
    if country in participatedineurovsion:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
            
    qkey = akinator.addquestion('Has your country ever participated in Eurovision?')
    for countryname in mapinfo.infobycountryname:
        if countryname in participatedineurovsion:
            akinator.addanswer(qkey, countryname, [0.8, 0.2])
        else:
            akinator.addanswer(qkey, countryname, [0.2, 0.8])
            
    

def setup_geography_akinator(akinator, mapinfo):
    
    # it's important to add the these terminal questions first to maintain a canonical country ordering (i.e. so the code doesn't break)
    for countryname in mapinfo.locationlist: # add terminal questions
        qkey = akinator.addquestion('Is your country %s?' % countryname, questiontype=akinator_model.QuestionType.TERMINAL)
        for countryname_secondary in mapinfo.locationlist:
            if countryname == countryname_secondary:
                akinator.addanswer(qkey, countryname_secondary, [1.0, 0.0])
            else:
                akinator.addanswer(qkey, countryname_secondary, [0.0, 1.0])
    
    internetcode_to_ciacountryname = {}
    
    ciacountrycode_tocountrycode = {}
    ciacountrycode_tocountrycode["UK"] = "GB"
    ciacountrycode_tocountrycode["SU"] = "RU"
    
    # Adds a large number of questions from the CIA fact book
    jsondict = json.load(open(questionsfile,"r"))
    nocode = {}
    for (questionttext, countryname, countrycodestring, answervec) in jsondict:
        m = re.match(r'^.*?\.(..).*$', countrycodestring)
        countrycode = countrycodestring[0:2]
        if m != None:
            countrycode = m[1]
        
        countrycode = ciacountrycode_tocountrycode.get(countrycode, countrycode)
            
        internetcode_to_ciacountryname[countrycode] = countryname
        if countrycode in mapinfo.twolettercountrycode_to_countryname:
            countryname = mapinfo.twolettercountrycode_to_countryname[countrycode]
            akinator.addquestionanswer(questionttext, countryname, answervec, questiontype=akinator_model.QuestionType.NONTERMINAL)
        else:
            nocode[countrycode] = countryname
    #print(internetcode_to_ciacountryname)
    print(nocode)
    
    add_demographic_info_from_shape_data(akinator, mapinfo)
    add_additional_questions(akinator, mapinfo)
    
        
            