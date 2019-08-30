import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch

import numpy as np
import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'Unibrowser'
        self.width = 1024
        self.height = 768
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.canvas =  WorldMapCanvas(self, width=10, height=8)
        self.move(0,0)
        
        button = QPushButton('Add a random colour', self)
        button.setToolTip('Add a random colour to a country on the mapo')
        button.clicked.connect(lambda: self.handleButton())
        button.move(800,0)
        button.resize(140,100)

        self.show()
    
    def handleButton(self):
        randomcountry = random.choice(list(self.canvas.patchlistsbycountry.keys()))
        randomcolor = (random.random(), random.random(), random.random())
        print(randomcolor)
        self.canvas.updatecolor(randomcountry, randomcolor)
        

class WorldMapCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=8, dpi=None):
        fig = plt.figure(figsize=(10,8))
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
        
        self.map = Basemap(projection='mill',lon_0=0)
        self.map.drawmapboundary(fill_color='aqua')
        self.map.fillcontinents(color='#ddaa66',lake_color='aqua')
        self.map.readshapefile('../shape_files/ne_10m_admin_0_countries/ne_10m_admin_0_countries', 'comarques', drawbounds = False)
        
         
        self.patchlistsbycountry = {}
        for info, shape in zip(self.map.comarques_info, self.map.comarques):
            patch = Polygon(np.array(shape), True, edgecolor='black', linewidth=0.5) # , facecolor='red'
            
            countryname = info['NAME_EN']
            patchlist = self.patchlistsbycountry.get(countryname, [])
            patchlist.append(patch)
            self.patchlistsbycountry[countryname] = patchlist
            
            #if "United States" in info['NAME_EN']:        
            self.ax.add_patch(patch)
        
        for patch in self.patchlistsbycountry['South Africa']:
            patch.set_facecolor('red')        
            
        print(list(self.patchlistsbycountry.keys()))
        
        self.draw()

    def updatecolor(self, country, color):
        for patch in self.patchlistsbycountry[country]:
            patch.set_facecolor(color)
            #patch.draw()
            self.ax.draw_artist(patch)
        self.figure.canvas.blit(self.ax.bbox) # fast way of updating canvas
        #self.draw() # slow way of updating canvas

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())