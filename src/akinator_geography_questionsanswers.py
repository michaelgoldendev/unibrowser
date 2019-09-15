import numpy as np

from mpl_toolkits.basemap import Basemap
import akinator_model

def setup_geography_akinator(akinator, mapinfo):
    defaultyes = [0.975, 0.025]
    defaultno = [0.025, 0.975]
    
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
                
    qkey = akinator.addquestion('Is the population smaller than 1,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] < 1000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
    qkey = akinator.addquestion('Is the population smaller than 10,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] < 10000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
            
    qkey = akinator.addquestion('Is the population larger than 50,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 50000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
    qkey = akinator.addquestion('Is the population larger than 100,000,000?')
    for countryname in mapinfo.locationlist:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 100000000:
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
    for countryname in mapinfo.locationlist: # add terminal questions
        qkey = akinator.addquestion('Is your location %s?' % countryname, questiontype=akinator_model.QuestionType.TERMINAL)
        for countryname_secondary in mapinfo.locationlist:
            if countryname == countryname_secondary:
                akinator.addanswer(qkey, countryname_secondary, [1.0, 0.0])
            else:
                akinator.addanswer(qkey, countryname_secondary, [0.0, 1.0])
        
            