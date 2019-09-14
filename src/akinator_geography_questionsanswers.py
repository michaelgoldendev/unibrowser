import numpy as np
import map_info
import akinator_model

from mpl_toolkits.basemap import Basemap

def setup_geography_akinator(akinator):
    defaultyes = [0.90, 0.05, 0.05]
    defaultmaybe = [0.2, 0.60, 0.2]
    defaultno = [0.05, 0.05, 0.90]
    
    mapinfo = map_info.MapInfo()
    
    map = mapinfo.map
    
    qkey = akinator.addquestion('Is this location considered a high income country?')
    for countryname in mapinfo.infobycountryname:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("1.") or info['INCOME_GRP'].startswith("2."):
            akinator.addanswer(qkey, countryname, defaultyes)
        else:
            akinator.addanswer(qkey, countryname, defaultno)
    
    qkey = akinator.addquestion('Is this location considered a low income country?')
    for countryname in mapinfo.infobycountryname:
        info = mapinfo.infobycountryname[countryname]
        if info['INCOME_GRP'].startswith("4.") or info['INCOME_GRP'].startswith("5."):
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
    
        
    continents = ['Asia', 'South America', 'Africa', 'Europe', 'North America', 'Oceania', 'Antarctica']
    continents.sort()
    
    # is you country in X continent?
    for continent in continents:
        qkey = akinator.addquestion('Is your location in %s?' % continent)
        for countryname in mapinfo.infobycountryname:
            info = mapinfo.infobycountryname[countryname]
            if info['CONTINENT'] == continent:
                akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
            else:
                akinator.addanswer(qkey, info['NAME_EN'], defaultno)
                
    qkey = akinator.addquestion('Is the population smaller than 1,000,000?')
    for countryname in mapinfo.infobycountryname:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] < 1000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
    
    qkey = akinator.addquestion('Is the population smaller than 10,000,000?')
    for countryname in mapinfo.infobycountryname:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] < 10000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
            
    qkey = akinator.addquestion('Is the population larger than 50,000,000?')
    for countryname in mapinfo.infobycountryname:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 50000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
    
    qkey = akinator.addquestion('Is the population larger than 100,000,000?')
    for countryname in mapinfo.infobycountryname:
        info = mapinfo.infobycountryname[countryname]
        if info['POP_EST'] >= 100000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)