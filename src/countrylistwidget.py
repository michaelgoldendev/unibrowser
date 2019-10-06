from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtChart import *

import matplotlib.cm
import matplotlib as mpl
import matplotlib.colors

import map_info

class QCustomWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomWidget, self).__init__(parent)
        
        self.hboxlayout  = QHBoxLayout()
        
        self.rankinglabel = QLabel("1")
        self.iconlabel = QLabel()
        self.countrylabel = QLabel()
        self.colourlabel = QLabel()
        self.problabel = QLabel()
        
        
        rankingfont = QFont()
        rankingfont.setPointSize(9)
        #rankingfont.setBold(True)
        self.rankinglabel.setFont(rankingfont)
        self.rankinglabel.setStyleSheet("color: #666666;")
        self.rankinglabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        countryfont = QFont()
        countryfont.setPointSize(12)
        #countryfont.setBold(True)
        #countryfont.setWeight(20)
        self.countrylabel.setFont(countryfont)
        
        
        probfont = QFont()
        probfont.setPointSize(10)
        #probfont.setBold(True)
        #countryfont.setWeight(20)
        self.problabel.setFont(probfont)
        
        #self.hboxlayout.addWidget(self.rankinglabel, 0)
        self.hboxlayout.addWidget(self.iconlabel, 0)
        self.hboxlayout.addWidget(self.countrylabel, 1)
        self.hboxlayout.addWidget(self.colourlabel, 0)
        self.hboxlayout.addWidget(self.problabel, 1)
        
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
        #self.listwidget.setStyleSheet('background: #f9f9f9;')
        self.listwidget.setStyleSheet("""        
                                    QListWidget::item:disabled
                                    {                               
                                        background: #f7f7f7;
                                    }
                                     """)
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
        for (rank, (icon, country, color, prob)) in enumerate(countrylist):            
            customwidget = QCustomWidget()
            #customwidget.rankinglabel.setText("%d" % (rank+1))
            #customwidget.rankinglabel.setFixedWidth(25)
            
            customwidget.iconlabel.setPixmap(icon)
            customwidget.iconlabel.setFixedWidth(70)
            customwidget.iconlabel.setStyleSheet('background: transparent;')
            
            customwidget.countrylabel.setText(country)
            customwidget.countrylabel.setFixedWidth(250)
            customwidget.countrylabel.setStyleSheet('background: transparent;')
            
            customwidget.colourlabel.setStyleSheet("background-color:" + color +";")
            customwidget.colourlabel.setFixedWidth(10)
            
            probtext = '%0.2f' % prob 
            if prob < 0.01:
                probtext = '{:.1E}'.format(prob)
            customwidget.problabel.setText(probtext)
            customwidget.problabel.setStyleSheet('background: transparent;')
            
            customitem = QListWidgetItem(self.listwidget)
            customitem.setSizeHint(customwidget.sizeHint())
            customitem.setFlags(Qt.NoItemFlags)
            
            
            
            self.listwidget.addItem(customitem)
            self.listwidget.setItemWidget(customitem, customwidget)
        
    def updatelist(self, probabilities, mapinfo, top=10):
        countrylist = self.__gettopranking(probabilities,mapinfo,top=top)
        self.__updatelist(countrylist)
        
    
    
    
    