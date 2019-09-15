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
import matplotlib.animation as animation

import numpy as np
import countrylistwidget

class UnicornIcon(QLabel):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        pix = QPixmap("../raw/unibrowser_binoculars_icon-320x501.png")
        pix = pix.scaledToWidth(64, mode=Qt.SmoothTransformation)
        self.setPixmap(pix)       
        self.h = pix.height()
        self.w = pix.width()
        print(self.h)
        
        self.setGeometry(QRect(0, 0, self.w, self.h))
        self.setStyleSheet("background-color: rgba(0, 0, 0,0);")
        
    def _set_pos(self, pos):
        
        self.move(pos.x() - self.w/2, pos.y() - self.h/2)

    pos = pyqtProperty(QPointF, fset=_set_pos)   

class WorldMapWindow(QWidget):

    def __init__(self, mapinfo):
        super().__init__()
        self.mapinfo = mapinfo
        self.left = 0
        self.top = 0
        self.title = 'Unibrowser- World Map'
        self.width = 1300
        self.height = 800
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QHBoxLayout()
        self.canvas =  WorldMapCanvas(self.mapinfo, parent=self, width=8.5, height=7.5)
        layout.addWidget(self.canvas)
        
        self.listwidget = countrylistwidget.CountryListWidget()
        layout.addWidget(self.listwidget)
        
        self.setLayout(layout)
        
        """
        self.unicornicon = UnicornIcon(self)
        self.path = QPainterPath()
        self.path.moveTo(30, 30)
        self.path.cubicTo(30, 30, 200, 30, 500, 30)
        self.initAnimation()
        """
        
        self.show()
    
    """
    def handleButton(self):
        randomlocation = random.choice(list(self.canvas.patchlistsbylocation.keys()))
        self.canvas.setlocationcolour(randomlocation, self.canvas.colormap(random.random()))
    """
    
    """
    def paintEvent(self, e):    
        
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.end()             

        
    def initAnimation(self):
        
        self.anim = QPropertyAnimation(self.unicornicon, b'pos')
        self.anim.setDuration(1000)
        
        self.anim.setStartValue(QPointF(30, 30))
        
        vals = [p/100 for p in range(0, 101)]

        for i in vals:
            self.anim.setKeyValueAt(i, self.path.pointAtPercent(i))  
                
        self.anim.setEndValue(QPointF(500, 30))        
        self.anim.start()
    """
        

class WorldMapCanvas(FigureCanvas):

    def __init__(self, mapinfo, parent=None, width=10, height=8, dpi=None):
        self.mapinfo = mapinfo
        fig = plt.figure(figsize=(width,height))        
        #plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        plt.subplots_adjust(left=0.01, right=0.99, top=1.0, bottom=0.0)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WorldMapWindow()
    sys.exit(app.exec_())