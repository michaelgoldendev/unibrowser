import numpy as np
import akinator_model

from mpl_toolkits.basemap import Basemap

def setup_geography_akinator(akinator):
    defaultyes = [0.90, 0.05, 0.05]
    defaultmaybe = [0.2, 0.60, 0.2]
    defaultno = [0.05, 0.05, 0.90]
    
    map = Basemap(projection='mill',lon_0=0,llcrnrlat=-75,urcrnrlat=85,llcrnrlon=-180,urcrnrlon=180)
    map.readshapefile('../shape_files/ne_10m_admin_0_countries/ne_10m_admin_0_countries', 'comarques', drawbounds = False, antialiased=True)
    
    """
    for info, shape in zip(map.comarques_info, map.comarques):
        print(info,shape)
    """
    """
    incomelabels = []
    for info, shape in zip(map.comarques_info, map.comarques):
        if info['INCOME_GRP'] not in incomelabels:
            incomelabels.append(info['INCOME_GRP'])
    print(incomelabels)
    """
    
    qkey = akinator.addquestion('Is this location considered a high income country?')
    for info, shape in zip(map.comarques_info, map.comarques):
        if info['INCOME_GRP'].startswith("1.") or info['INCOME_GRP'].startswith("2."):
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
    
    qkey = akinator.addquestion('Is this location considered a low income country?')
    for info, shape in zip(map.comarques_info, map.comarques):
        if info['INCOME_GRP'].startswith("4.") or info['INCOME_GRP'].startswith("5."):
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
    
        
    continents = ['Asia', 'South America', 'Africa', 'Europe', 'North America', 'Oceania', 'Antarctica']
    continents.sort()
    
    # is you country in X continent?
    for continent in continents:
        qkey = akinator.addquestion('Is your location in %s?' % continent)
        for info, shape in zip(map.comarques_info, map.comarques):
            if info['CONTINENT'] == continent:
                akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
            else:
                akinator.addanswer(qkey, info['NAME_EN'], defaultno)
                
    qkey = akinator.addquestion('Is the population smaller than 1,000,000?')
    for info, shape in zip(map.comarques_info, map.comarques):
        if info['POP_EST'] < 1000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
    
    qkey = akinator.addquestion('Is the population smaller than 10,000,000?')
    for info, shape in zip(map.comarques_info, map.comarques):
        if info['POP_EST'] < 10000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
            
    qkey = akinator.addquestion('Is the population larger than 50,000,000?')
    for info, shape in zip(map.comarques_info, map.comarques):
        if info['POP_EST'] >= 50000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
    
    qkey = akinator.addquestion('Is the population larger than 100,000,000?')
    for info, shape in zip(map.comarques_info, map.comarques):
        if info['POP_EST'] >= 100000000:
            akinator.addanswer(qkey, info['NAME_EN'], defaultyes)
        else:
            akinator.addanswer(qkey, info['NAME_EN'], defaultno)
        
    akinator.reset()
    
        
model = akinator_model.Akinator()        
setup_geography_akinator(model)
#print(model.answerdict)