import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

import matplotlib.cm
import matplotlib as mpl
import matplotlib.colors

class QCustomWidget (QWidget):
    def __init__ (self, parent = None):
        super(QCustomWidget, self).__init__(parent)
        
        self.hboxlayout  = QHBoxLayout()
        
        self.iconlabel = QLabel()
        self.countrylabel = QLabel()
        self.colourlabel = QLabel()
        
        
        countryfont = QFont()
        countryfont.setPointSize(16)
        countryfont.setBold(True)
        #countryfont.setWeight(20)
        self.countrylabel.setFont(countryfont)
        
        self.hboxlayout.addWidget(self.iconlabel, 0)
        self.hboxlayout.addWidget(self.countrylabel, 1)
        self.hboxlayout.addWidget(self.colourlabel, 2)
        
        self.setLayout(self.hboxlayout)

    def setIcon (self, imagePath):
        self.iconlabel.setPixmap(QPixmap(imagePath))

class exampleQMainWindow (QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        
        colormap = matplotlib.cm.inferno #matplotlib.cm.get_cmap('Spectral')
        norm = mpl.colors.LogNorm(vmin=1e-3, vmax=1.0,clip=True) # mpl.colors.Normalize(vmin=0.0, vmax=1.0)       
        
        flagdir = '../images/flags-normal/'
        flagfiles = os.listdir(flagdir)
        
        countrylist = []
        for (index, flagfile) in enumerate(flagfiles):
            flagpath = os.path.join(flagdir, flagfile)
            v = index/len(flagfiles)
            colorstring = matplotlib.colors.to_hex(colormap(norm(v)))
            countrylist.append((QPixmap(flagpath), 'South Africa', colorstring))
        
        
        # Create QListWidget
        self.listwidget = QListWidget(self)
        for icon, country, color in countrylist:
            icon = icon.scaledToWidth(80, mode=Qt.SmoothTransformation)
            
            customwidget = QCustomWidget()
            customwidget.iconlabel.setPixmap(icon)
            customwidget.iconlabel.setFixedWidth(85)
            
            customwidget.countrylabel.setText(country)
            #customwidget.countrylabel.resize(QSize(200, customwidget.countrylabel.height()))
            customwidget.countrylabel.setFixedWidth(250)
            customwidget.colourlabel.setStyleSheet("background-color:" + color +";")
            customwidget.colourlabel.setFixedWidth(10)
            
            #customitem.setIcon(icon)
            # Create QListWidgetItem
            customitem = QListWidgetItem(self.listwidget)
            customitem.setSizeHint(customwidget.sizeHint())
            
            self.listwidget.addItem(customitem)
            self.listwidget.setItemWidget(customitem, customwidget)
        self.setCentralWidget(self.listwidget)

app = QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())