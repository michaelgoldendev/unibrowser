import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
import matplotlib.cm
from matplotlib import rcParams, cycler
import matplotlib as mpl

import numpy as np
import random

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'Unibrowser'
        self.width = 1200
        self.height = 800
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.canvas =  WorldMapCanvas(self, width=9, height=7.5)
        self.canvas.move(10,10)        
        
        button = QPushButton('Set a random colour', self)
        button.setToolTip('Add a random colour to a location on the mapo')
        button.clicked.connect(lambda: self.handleButton())
        button.move(950,10)
        button.resize(140,100)

        self.show()
    
    def handleButton(self):
        randomlocation = random.choice(list(self.canvas.patchlistsbylocation.keys()))
        self.canvas.setlocationcolour(randomlocation, self.canvas.colormap(random.random()))
        

class WorldMapCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=8, dpi=None):
        fig = plt.figure(figsize=(width,height))        
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
        
        # merc, mill
        # mill, robin, merc
        self.map = Basemap(projection='mill',lon_0=0,llcrnrlat=-75,urcrnrlat=87,llcrnrlon=-180,urcrnrlon=180)
        self.map.drawmapboundary(fill_color='aqua')
        #self.map.fillcontinents(color='#ddaa66')
        self.map.readshapefile('../shape_files/ne_10m_admin_0_countries/ne_10m_admin_0_countries', 'comarques', drawbounds = False, antialiased=True)
        
        self.colormap = matplotlib.cm.inferno #matplotlib.cm.get_cmap('Spectral')
        self.norm = mpl.colors.LogNorm(vmin=1e-4, vmax=1.0,clip=True) # mpl.colors.Normalize(vmin=0.0, vmax=1.0)
         
        self.patchlistsbylocation = {}
        for info, shape in zip(self.map.comarques_info, self.map.comarques):
            patch = Polygon(np.array(shape), True, edgecolor='black', linewidth=0.5,antialiased=True) # , facecolor='red'
            locationname = info['NAME_EN']
            patchlist = self.patchlistsbylocation.get(locationname, [])
            patchlist.append(patch)
            self.patchlistsbylocation[locationname] = patchlist
            self.ax.add_patch(patch)
         
        
        """
        probabilities = []
        for loc in self.patchlistsbylocation.keys():
            probabilities.append(random.random())
        probabilities = np.array(probabilities)        
        probabilities[100] = 100.0
        probabilities /= np.sum(probabilities)
        """
        probabilities = np.random.dirichlet(np.full((len(self.patchlistsbylocation),), 1.0))
        print(probabilities)
        print(np.max(probabilities))
        for (prob,loc) in zip(probabilities, self.patchlistsbylocation.keys()):
            self.setlocationcolour(loc, self.colormap(self.norm(prob)), drawimmediately=False)

        #xlimits = self.ax.get_xlim()

        #rcParams['axes.prop_cycle'] = cycler(color=self.colormap(np.linspace(0, 1, 100)))
        cax = fig.add_axes([0.2, 0.07, 0.6, 0.04])
        cb1 = mpl.colorbar.ColorbarBase(cax, cmap=self.colormap, norm=self.norm, orientation='horizontal')
        cb1.set_label('Estimated probability')
            
        self.draw()

    def setlocationcolour(self, location, color, drawimmediately=True):
        for patch in self.patchlistsbylocation[location]:
            patch.set_facecolor(color)
            if drawimmediately:
                self.ax.draw_artist(patch)        
        if drawimmediately:
            self.figure.canvas.blit(self.ax.bbox) # fast way of updating canvas
        #self.draw() # slow way of updating canvas

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())