import numpy as np

from mpl_toolkits.basemap import Basemap
import akinator_model

import json
import re
import os

script_path = os.path.dirname(os.path.abspath( __file__ ))
questionsfile = os.path.abspath(os.path.join(script_path, '../questions.json'))

def add_demographic_info_from_shape_data(akinator, mapinfo):
    defaultyes = [0.85, 0.15]
    defaultno = [0.15, 0.85]
    
    qkey = akinator.addquestion('Is this country considered a high income country?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("1.") or info['INCOME_GRP'].startswith("2."):
            akinator.addanswer(qkey, countryname, [0.85, 0.15])
        else:
            akinator.addanswer(qkey, countryname, [0.15, 0.85])
    
 
    qkey = akinator.addquestion('Is this country considered a low income country?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("4.") or info['INCOME_GRP'].startswith("5."):
            akinator.addanswer(qkey, countryname, [0.75, 0.25])
        else:
            akinator.addanswer(qkey, countryname, [0.25, 0.75])
    
    
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
    
    """
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
    """
    qkey = akinator.addquestion('Is the population greater than 30,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 30000000:
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
            akinator.addanswer(qkey, countryname, [0.85, 0.15])
        else:
            akinator.addanswer(qkey, countryname, [0.15, 0.85])
    
    """
    Countries with nuclear weapons
    """
    hasnuclearweapons = ["United States of America", "Russia", "United Kingdom", "France", "People's Republic of China", "India", "Pakistan", "North Korea", "Israel"]
    for country in hasnuclearweapons:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
    qkey = akinator.addquestion('Does your country currently have nuclear weapons?')
    for countryname in mapinfo.infobycountryname:
        if countryname in hasnuclearweapons:
            akinator.addanswer(qkey, countryname, [0.9, 0.1])
        else:
            akinator.addanswer(qkey, countryname, [0.1, 0.9])
            
    """
    Countries that have participated in Eurovision
    """
    participatedineurovsion = ["Albania","Armenia","Australia","Austria","Azerbaijan","Belarus","Belgium","Bosnia and Herzegovina","Bulgaria","Croatia","Cyprus","Czech Republic","Denmark","Estonia","Finland","France","Georgia","Germany","Greece","Hungary","Iceland","Ireland","Israel","Italy","Latvia","Lithuania","Malta","Moldova","Montenegro","Netherlands","Republic of Macedonia","Norway","Poland","Portugal","Romania","Russia","San Marino","Serbia","Slovakia","Slovenia","Spain","Sweden","Switzerland","Turkey","Ukraine","United Kingdom","Andorra","Monaco","Montenegro","Luxembourg","Morocco"]
    #,"Yugoslavia"
    for country in participatedineurovsion:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
            
    qkey = akinator.addquestion('Has your country ever participated in Eurovision?')
    for countryname in mapinfo.infobycountryname:
        if countryname in participatedineurovsion:
            akinator.addanswer(qkey, countryname, [0.80, 0.2])
        else:
            akinator.addanswer(qkey, countryname, [0.2, 0.80])
    
    """
    Countries that have participated in football world cup
    """
    wonthefootballworldcup = ["Brazil", "Italy", "Germany", "Uruguay", "Argentina", "France", "United Kingdom", "Spain"]
    for country in wonthefootballworldcup:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
    
    qkey = akinator.addquestion('Has your country ever won a football world cup?')
    for countryname in mapinfo.infobycountryname:
        if countryname in wonthefootballworldcup:
            akinator.addanswer(qkey, countryname, [0.85, 0.15])
        else:
            akinator.addanswer(qkey, countryname, [0.15, 0.85])
            
    """
    Countries that don't use the metric system
    """
    print("Metric system")
    dontusethemetricystem = ["United States of America", "Liberia", "Burma"]
    for country in dontusethemetricystem:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
            
    qkey = akinator.addquestion('Is your country one of the three that do not use the metric system?')
    for countryname in mapinfo.infobycountryname:
        if countryname in dontusethemetricystem:
            akinator.addanswer(qkey, countryname, [0.90, 0.10])
        else:
            akinator.addanswer(qkey, countryname, [0.10, 0.90])
    
    
    
    
    """
    Hosted the olympic games
   
    print("Olympic games")
    hostedolympicgames = ["United States", "France", "Germany", "Greece", "Japan", "Italy", "United Kingdom", "Canada", "Australia", "Russia", "South Korea", "Switzerland", "Norway", "Austria", "China", "Brazil", "Sweden", "Belgium", "Netherlands", "Finland", "Mexico", "Spain", "Yugoslavia"]
    wellknownolympichosts = ["United States", "France", "Germany", "Greece", "Japan", "United Kingdom", "Australia", "Russia", "South Korea", "China", "Brazil"]
    for country in hostedolympicgames:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
            
    qkey = akinator.addquestion('Has your country hosted the summer or winter Olympic games?')
    for countryname in mapinfo.infobycountryname:
        if countryname in hostedolympicgames:
            if countryname in wellknownolympichosts:
                akinator.addanswer(qkey, countryname, [0.95, 0.05])
            else:
                akinator.addanswer(qkey, countryname, [0.70, 0.30])
        else:
            akinator.addanswer(qkey, countryname, [0.1, 0.90])
            if countryname in wellknownolympichosts:
                akinator.addanswer(qkey, countryname, [0.05, 0.95])
            else:
                akinator.addanswer(qkey, countryname, [0.30, 0.70])
    """
    
    """
    Does your country use the Euro as its currency?
    """    
    eurocountries = [ "Austria", "Belgium", "Cyprus", "Estonia", "Finland", "France", "Germany", "Greece", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal", "Slovakia", "Slovenia", "Spain"]
    for country in eurocountries:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
            
    qkey = akinator.addquestion('Does your country use the Euro as its currency?')
    for countryname in mapinfo.infobycountryname:
        if countryname in eurocountries:
            akinator.addanswer(qkey, countryname, [0.85, 0.15])
        else:
            akinator.addanswer(qkey, countryname, [0.15, 0.85])
        
    """
    Does your country have the death penalty?
    """    
    deathpenalty = ["Afghanistan", "India", "Nigeria", "United States of America", "Iran", "Japan", "Taiwan", "Kuwait", "Zimbabwe", "Libya", "Thailand", "Guyana", "Uganda", "Bangladesh", "Iraq", "Indonesia", "Botswana", "United Arab Emirates", "The Bahamas", "Cuba", "Belarus", "Yemen", "Saudi Arabia", "Vietnam", "Syria", "Egypt", "South Sudan", "Democratic Republic of the Congo", "Ethiopia", "People's Republic of China", "Sudan", "Comoros", "Somalia", "Barbados", "Malaysia", "Chad", "Pakistan", "Oman", "Singapore", "Saint Kitts and Nevis", "Saint Lucia", "Bahrain", "North Korea", "Equatorial Guinea", "Saint Vincent and the Grenadines", "Palestine", "Trinidad and Tobago", "Lesotho", "Antigua and Barbuda", "Belize", "Dominica", "Jamaica", "Jordan"]
    for country in deathpenalty:
        if country not in mapinfo.infobycountryname:
            print("Country cannot be found: ", country)
            
    qkey = akinator.addquestion('Does your country have the death penalty?')
    for countryname in mapinfo.infobycountryname:
        if countryname in deathpenalty:
            akinator.addanswer(qkey, countryname, [0.85, 0.15])
        else:
            akinator.addanswer(qkey, countryname, [0.15, 0.85])
    
    for country in mapinfo.infobycountryname.keys():
        if "bahama" in country.lower():
            print(country)
    

def setup_geography_akinator(akinator, mapinfo):
    quicksetup = False # use True for testing purposes only, speeds-up application loading times.
    
    if not quicksetup:
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
        exclusions = ["Oceania"]
        for (questionttext, countryname, countrycodestring, answervec) in jsondict:
            excluded = False
            for exclusion in exclusions:
                if exclusion in questionttext:
                    excluded = True
            #if not questionttext.startswith("Does your country border"):
            if not excluded:
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
    
        
            