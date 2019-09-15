from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

import matplotlib.cm
import matplotlib as mpl
import matplotlib.colors

import map_info

class QCustomWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomWidget, self).__init__(parent)
        
        self.hboxlayout  = QHBoxLayout()
        
        self.iconlabel = QLabel()
        self.countrylabel = QLabel()
        self.colourlabel = QLabel()
        self.problabel = QLabel()
        
        
        countryfont = QFont()
        countryfont.setPointSize(14)
        #countryfont.setBold(True)
        #countryfont.setWeight(20)
        self.countrylabel.setFont(countryfont)
        
        probfont = QFont()
        probfont.setPointSize(12)
        #probfont.setBold(True)
        #countryfont.setWeight(20)
        self.problabel.setFont(probfont)
        
        self.hboxlayout.addWidget(self.iconlabel, 0)
        self.hboxlayout.addWidget(self.countrylabel, 1)
        self.hboxlayout.addWidget(self.colourlabel, 2)
        self.hboxlayout.addWidget(self.problabel, 3)
        
        self.setLayout(self.hboxlayout)

    def setIcon (self, imagePath):
        self.iconlabel.setPixmap(QPixmap(imagePath))

class CountryListWidget (QWidget):
    def __init__ (self):
        super(CountryListWidget, self).__init__()
        
        
        self.colormap = matplotlib.cm.inferno #matplotlib.cm.get_cmap('Spectral')
        self.norm = mpl.colors.LogNorm(vmin=1e-3, vmax=1.0,clip=True) # mpl.colors.Normalize(vmin=0.0, vmax=1.0)    
        
        mapinfo = map_info.MapInfo()
        self.countrycode_to_pixmap = {}
        for countrycode in mapinfo.twolettercountrycodelist:
            flagpath = mapinfo.twolettercountrycode_to_flagnormalpngfile[countrycode]
            icon = QPixmap(flagpath).scaledToWidth(60, mode=Qt.SmoothTransformation)
            self.countrycode_to_pixmap[countrycode] = icon
        
        layout = QHBoxLayout()
        self.listwidget = QListWidget(self)
        layout.addWidget(self.listwidget)
        self.setLayout(layout)
        
        
    def __gettopranking(self, probabilities,mapinfo, top=10):
        sortedstates = [(p, countryname, countrycode) for (p, countryname, countrycode)  in zip(probabilities, mapinfo.locationlist, mapinfo.twolettercountrycodelist)]
        sortedstates.sort(reverse=True)
        upper = min(len(sortedstates), top)
        sortedstates = sortedstates[0:upper]
        
        countrylist = []
        for (p, countryname, countrycode) in sortedstates:
            colorstring = matplotlib.colors.to_hex(self.colormap(self.norm(p)))
            countrylist.append((self.countrycode_to_pixmap[countrycode], countryname, colorstring, p))
        return countrylist

    def __updatelist(self, countrylist):
        self.listwidget.clear()
        for icon, country, color, prob in countrylist:            
            customwidget = QCustomWidget()
            customwidget.iconlabel.setPixmap(icon)
            customwidget.iconlabel.setFixedWidth(70)
            
            customwidget.countrylabel.setText(country)
            customwidget.countrylabel.setFixedWidth(250)
            customwidget.colourlabel.setStyleSheet("background-color:" + color +";")
            customwidget.colourlabel.setFixedWidth(10)
            
            probtext = '%0.2f' % prob 
            if prob < 0.01:
                probtext = '{:.1E}'.format(prob)
            customwidget.problabel.setText(probtext)
            
            customitem = QListWidgetItem(self.listwidget)
            customitem.setSizeHint(customwidget.sizeHint())
            
            self.listwidget.addItem(customitem)
            self.listwidget.setItemWidget(customitem, customwidget)
        
    def updatelist(self, probabilities, mapinfo, top=10):
        countrylist = self.__gettopranking(probabilities,mapinfo,top=top)
        self.__updatelist(countrylist)
        
    
    
    
    