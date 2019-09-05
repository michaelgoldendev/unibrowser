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
import random

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

    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'Unibrowser- World Map'
        self.width = 1000
        self.height = 800
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QVBoxLayout()
        self.canvas =  WorldMapCanvas(self, width=9, height=7.5) # width and height params don't have any effect when using a layout.
        layout.addWidget(self.canvas)
        
        #self.canvas.move(10,10)                
              
        """
        button = QPushButton('Set a random colour', self)
        button.setToolTip('Add a random colour to a location on the mapo')
        button.clicked.connect(lambda: self.handleButton())
        button.move(950,10)
        button.resize(140,100)
        """
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

    def __init__(self, parent=None, width=10, height=8, dpi=None):
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
        self.map = Basemap(projection='mill',lon_0=0,llcrnrlat=-75,urcrnrlat=85,llcrnrlon=-180,urcrnrlon=180)
        self.map.drawmapboundary(fill_color=self.oceancolor)
        #self.map.fillcontinents(color='#ddaa66')
        self.map.readshapefile('../shape_files/ne_10m_admin_0_countries/ne_10m_admin_0_countries', 'comarques', drawbounds = False, antialiased=True)
                 
        self.patchlistsbylocation = {}
        for info, shape in zip(self.map.comarques_info, self.map.comarques):
            patch = Polygon(np.array(shape), True, edgecolor='black', linewidth=0.5,antialiased=True) # , facecolor='red'
            locationname = info['NAME_EN']
            patchlist = self.patchlistsbylocation.get(locationname, [])
            patchlist.append(patch)
            self.patchlistsbylocation[locationname] = patchlist
            self.ax.add_patch(patch)
            
        probabilities = np.random.dirichlet(np.full((len(self.patchlistsbylocation),), 0.05))
        for (prob,loc) in zip(probabilities, self.patchlistsbylocation.keys()):
            self.setlocationcolour(loc, self.colormap(self.norm(prob)), drawimmediately=False)
            
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
        """
        self.unibrowser_img = plt.imread("../raw/unibrowser_binoculars_icon-320x501.png")
        
        self.mapwidth = self.ax.get_xlim()[1]
        self.mapheight = self.ax.get_ylim()[1]
        scalefactor = 0.045
        self.imagewidth = self.mapwidth*scalefactor
        self.imageheight = self.mapwidth*100.0/64.0*scalefactor      
        self.imagex = (self.mapwidth-self.imagewidth)/2.0
        self.imagey = (self.mapheight-self.imageheight)/2.0
        #self.unibrowser_imgax = self.ax.imshow(self.unibrowser_img, extent=[self.imagex, self.imagex+self.imagewidth, self.imagey, self.imagey+self.imageheight], zorder=1, interpolation='gaussian', animated=True)
        self.unibrowser_imgax = self.ax.imshow(self.unibrowser_img, zorder=1, interpolation='gaussian', animated=True)
        ani = animation.FuncAnimation(fig, self.updatefig, interval=10, blit=True)
        """
    
        self.draw()
    
    """
    def updatefig(self,*args):
        self.imagex += self.imagewidth*0.1
        #self.imagey += self.imageheight*0.001
        self.unibrowser_imgax.set_extent([self.imagex, self.imagex+self.imagewidth, self.imagey, self.imagey+self.imageheight])
        return self.unibrowser_imgax,
    """

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