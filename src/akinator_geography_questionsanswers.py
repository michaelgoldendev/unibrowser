import numpy as np

from mpl_toolkits.basemap import Basemap
import akinator_model

import json
import re

def setup_geography_akinator(akinator, mapinfo):
    print(mapinfo.locationlist)
    exit()
    
    # it's important to add the these terminal questions first to maintain a canonical country ordering (i.e. so the code doesn't break)
    for countryname in mapinfo.locationlist: # add terminal questions
        qkey = akinator.addquestion('Is your location %s?' % countryname, questiontype=akinator_model.QuestionType.TERMINAL)
        for countryname_secondary in mapinfo.locationlist:
            if countryname == countryname_secondary:
                akinator.addanswer(qkey, countryname_secondary, [1.0, 0.0])
            else:
                akinator.addanswer(qkey, countryname_secondary, [0.0, 1.0])
    
    internetcode_to_ciacountryname = {}
    
    ciacountrycode_tocountrycode = {}
    ciacountrycode_tocountrycode["UK"] = "GB"
    ciacountrycode_tocountrycode["SU"] = "RU"
    
    jsondict = json.load(open("../questions.json","r"))
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
    
    
    
    
    defaultyes = [0.90, 0.1]
    defaultno = [0.1, 0.9]
    
    qkey = akinator.addquestion('Is this location considered a high income country?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("1.") or info['INCOME_GRP'].startswith("2."):
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
    qkey = akinator.addquestion('Is this location considered a low income country?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("4.") or info['INCOME_GRP'].startswith("5."):
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
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
    
    
        
            