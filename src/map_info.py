import os
from mpl_toolkits.basemap import Basemap

script_path = os.path.dirname(os.path.abspath( __file__ ))
shapefile = os.path.abspath(os.path.join(script_path, '../shape_files/ne_10m_admin_0_countries/ne_10m_admin_0_countries'))
flagdir = os.path.abspath(os.path.join(script_path, '../images/flags-normal/'))
additionalflagdir = os.path.abspath(os.path.join(script_path, '../images/flags-additional/'))

class MapInfo():

    def __init__(self):
        self.map = Basemap(projection='mill',lon_0=0,llcrnrlat=-75,urcrnrlat=85,llcrnrlon=-180,urcrnrlon=180)
        self.map.readshapefile(shapefile, 'comarques', drawbounds = False, antialiased=True)
                 
        self.locationset = set()
        self.locationlist = []
        self.twolettercountrycode_to_countryname = {}
        self.twolettercountrycodelist = []
        self.shapelistbycountryname = {}
        self.infobycountryname = {}
        
        missingcountrycodes = {}
        missingcountrycodes["Norway"] = "NO"
        
        for info, shape in zip(self.map.comarques_info, self.map.comarques):
            locationname = info['NAME_EN']
            if locationname not in self.locationset:                
                countrycode = info['ISO_A2']
                if countrycode == '-99':
                    countrycode = info['WB_A2']
                if countrycode == '-99':
                    countrycode = info['FIPS_10_']
                if countrycode == '-99' and locationname in missingcountrycodes:
                    countrycode = missingcountrycodes[locationname]
                
                if countrycode != '-99':
                    self.twolettercountrycode_to_countryname[countrycode] = locationname
                    self.twolettercountrycodelist.append(countrycode)                    
                    self.locationset.add(locationname)
                    self.locationlist.append(locationname)
                else:
                    print("No country code for: ", locationname)
            
            shapelistbylocation = self.shapelistbycountryname.get(locationname,[])
            shapelistbylocation.append(shape)
            self.shapelistbycountryname[locationname] = shapelistbylocation
            self.infobycountryname[locationname] = info
            
        self.twolettercountrycode_to_flagnormalpngfile = {}
        
        for (index, flagfile) in enumerate(os.listdir(flagdir)):
            if flagfile.endswith(".png"):
                flagpath = os.path.join(flagdir, flagfile)
                twolettercountrycode = flagfile[0:2].upper()
                if twolettercountrycode in self.twolettercountrycode_to_countryname:
                    self.twolettercountrycode_to_flagnormalpngfile[twolettercountrycode] = flagpath
                else:
                    print(twolettercountrycode)
        for (index, flagfile) in enumerate(os.listdir(additionalflagdir)):
            if flagfile.endswith(".png"):
                flagpath = os.path.join(additionalflagdir, flagfile)
                twolettercountrycode = flagfile[0:2].upper()
                if twolettercountrycode in self.twolettercountrycode_to_countryname:
                    self.twolettercountrycode_to_flagnormalpngfile[twolettercountrycode] = flagpath
                else:
                    print(twolettercountrycode)
        
        for twolettercountrycode in self.twolettercountrycode_to_countryname:
            if twolettercountrycode not in self.twolettercountrycode_to_flagnormalpngfile:
                print("Flag not available for: ", twolettercountrycode,self.twolettercountrycode_to_countryname[twolettercountrycode])