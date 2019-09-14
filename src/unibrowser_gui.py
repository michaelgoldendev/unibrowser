from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

import numpy as np
import sys
import akinator_model
import akinator_geography_questionsanswers
import worldmap
import map_info

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.mapinfo = map_info.MapInfo()
        
        self.model = akinator_model.Akinator()
        akinator_geography_questionsanswers.setup_geography_akinator(self.model, self.mapinfo)
        self.qkey = self.model.getnextquestion()
        self.model.usedquestions.append(self.qkey)
        self.label = QLabel(self.model.questions[self.qkey])
        
        self.worldmapwindow = worldmap.WorldMapWindow(self.mapinfo)
        self.updateWorldMap(self.model)
        self.initUI()
        
        
        
    def initUI(self):     
        self.setWindowTitle("Unibrowser")
        
        layout = QVBoxLayout()
        
        questionfont = QFont()
        questionfont.setPointSize(18)
        questionfont.setBold(True)
        questionfont.setWeight(75)
        
        self.label.setFont(questionfont)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        answerbuttonfont = QFont()
        answerbuttonfont.setPointSize(14)
        answerbuttonfont.setBold(True)
        #answerbuttonfont.setWeight(75)
        
        yesbutton = QPushButton('Yes', self)
        yesbutton.setFont(answerbuttonfont)
        yesbutton.clicked.connect(lambda: self.handleButton(akinator_model.DefaultResponse.YES))
        yesbutton.setToolTip('Yes')
        layout.addWidget(yesbutton)
        
        maybebutton = QPushButton('Don\'t know', self)
        maybebutton.setFont(answerbuttonfont)
        maybebutton.clicked.connect(lambda: self.handleButton(akinator_model.DefaultResponse.DONTKNOW))
        maybebutton.setToolTip('Don\'t know')
        layout.addWidget(maybebutton)
        
        nobutton = QPushButton('No', self)
        nobutton.setFont(answerbuttonfont)
        nobutton.clicked.connect(lambda: self.handleButton(akinator_model.DefaultResponse.NO))
        nobutton.setToolTip('No')
        layout.addWidget(nobutton)
        
        self.setLayout(layout)
        self.show()
        
    def handleButton(self, answer):
        self.model.bayesianupdate_discreteanswer(self.qkey, answer)
        self.qkey = self.model.getnextquestion()
        if self.qkey >= 0:
            self.model.usedquestions.append(self.qkey)
            self.label.setText(self.model.questions[self.qkey])       
            self.updateWorldMap(self.model)
        else:
            exit()
            
    def updateWorldMap(self, akinator):
        for (state,prob) in zip(akinator.statelist, akinator.stateprobs):
            self.worldmapwindow.canvas.setlocationcolourbyvalue(state,prob,drawimmediately=False)
        self.worldmapwindow.canvas.draw()
            
        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = MainWindow()    
    sys.exit(app.exec_())