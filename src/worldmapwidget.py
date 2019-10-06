import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtChart import *


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import Patch
import matplotlib.cm
from matplotlib import rcParams, cycler
import matplotlib as mpl
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import numpy as np

import map_info
from questionanswerwidget import QuestionAnswerWidget

import os
script_path = os.path.dirname(os.path.abspath( __file__ ))

class WorldMapCanvas(FigureCanvas):
    def __init__(self, mapinfo, parent=None, width=12, height=10, dpi=None):        
        self.showLegend = False
        self.image = plt.imread(os.path.abspath(os.path.join(script_path, '../images/unibrowser_binoculars_icon-1178x1844.png')))
        self.oi = OffsetImage(self.image, zoom = 0.28)
        
        self.mapinfo = mapinfo
        fig = plt.figure(figsize=(width,height))       
        #plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        plt.subplots_adjust(left=0.01, right=0.99, top=1.0, bottom=0.005)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = plt.gca()
                #self.ax = self.figure.add_subplot(111)
        
        # graphical parameters
        self.colormap = matplotlib.cm.inferno #matplotlib.cm.get_cmap('Spectral')
        self.norm = mpl.colors.LogNorm(vmin=1e-3, vmax=1.0,clip=True) # mpl.colors.Normalize(vmin=0.0, vmax=1.0)       
        self.oceancolor = '#bff2ff'
        fig.patch.set_facecolor('white')
        
        # possible projections: mill, robin, merc
        self.map = self.mapinfo.map
        self.map.drawmapboundary(fill_color=self.oceancolor)
        #self.map.fillcontinents(color='#ddaa66')
        #self.map.readshapefile('../shape_files/ne_10m_admin_0_countries/ne_10m_admin_0_countries', 'comarques', drawbounds = False, antialiased=True)
                 
        self.patchlistsbylocation = {}
        for locationname in self.mapinfo.shapelistbycountryname:
            for shape in self.mapinfo.shapelistbycountryname[locationname]:
                patch = Polygon(np.array(shape), True, edgecolor='black', linewidth=0.5,antialiased=True)
                patchlist = self.patchlistsbylocation.get(locationname, [])
                patchlist.append(patch)
                self.patchlistsbylocation[locationname] = patchlist
                self.ax.add_patch(patch)
            
        #probabilities = np.random.dirichlet(np.full((len(self.patchlistsbylocation),), 0.05))
        probabilities = np.ones(len(self.patchlistsbylocation))*1e-100
        for (prob,loc) in zip(probabilities, self.patchlistsbylocation.keys()):
            self.setlocationcolourbyvalue(loc, prob, drawimmediately=False)
            
            
        if self.showLegend:
            #cax = fig.add_axes([0.2, 0.07, 0.6, 0.04])
            cax = fig.add_axes([0.2, 0.065, 0.6, 0.04])
            cb1 = mpl.colorbar.ColorbarBase(cax, cmap=self.colormap, norm=self.norm, orientation='horizontal')
            tickcoords = cb1.ax.get_xticks()
            ticklabels = cb1.ax.get_xticklabels()
            for (coord,ticklabel) in zip(tickcoords, ticklabels):
                val = self.norm.inverse(coord)
                if np.abs(val-1.0) < val*1.0e-10:                
                    ticklabel.set_text("1.0")
                elif np.abs(val-0.5) < val*1.0e-10:                
                    ticklabel.set_text("0.5")
                elif np.abs(val-0.1) < val*1.0e-10:
                    ticklabel.set_text("0.1")
                elif np.abs(val-0.01) < val*1.0e-10:
                    ticklabel.set_text("0.01")
                elif np.abs(val-0.001) < val*1.0e-10:
                    ticklabel.set_text("0.001")
                elif np.abs(val-0.0001) < val*1.0e-10:
                    ticklabel.set_text("0.0001")
            ticklabels[0].set_text("<" + ticklabels[0].get_text())
                
                
            cb1.ax.set_xticklabels(ticklabels)
            cb1.set_label('Estimated probability')
        
       
        self.box = AnnotationBbox(self.oi, (self.ax.get_xlim()[1]/2.0, self.ax.get_ylim()[1]/2.0), frameon=False)

        #ani = animation.FuncAnimation(fig, self.animate, interval = 50, blit = False)
    
        self.draw()
        
    def setlocationcolourbyvalue(self, location, value, drawimmediately=True):
        self.setlocationcolour(location, self.colormap(self.norm(value)), drawimmediately=drawimmediately)

    def setlocationcolour(self, location, color, drawimmediately=True):
        for patch in self.patchlistsbylocation[location]:
            patch.set_facecolor(color)
            if drawimmediately:
                self.ax.draw_artist(patch)
        if drawimmediately:
            self.figure.canvas.blit(self.ax.bbox) # fast way of updating canvas
        #self.draw() # slow way of updating canvas
    
    def showUnicorn(self):        
        self.ax.add_artist(self.box)
        self.draw()
        
        
    """
    def animate(self, i) : 
        self.box.set_position((i*10000, i*10000))
    """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WorldMapWidget(map_info.MapInfo())
    sys.exit(app.exec_())