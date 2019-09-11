from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

import numpy as np
import sys
import akinator_model
import akinator_geography_questionsanswers
import worldmap

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.model = akinator_model.Akinator()
        akinator_geography_questionsanswers.setup_geography_akinator(self.model)
        self.qkey = self.model.getnextquestion()
        self.model.usedquestions.append(self.qkey)
        self.label = QLabel(self.model.questions[self.qkey])
        
        self.worldmapwindow = worldmap.WorldMapWindow()
        self.updateWorldMap(self.model)
        self.initUI()
        
        
        
    def initUI(self):     
        self.setWindowTitle("Unibrowser")
        
        layout = QVBoxLayout()
        
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        yesbutton = QPushButton('Yes', self)
        yesbutton.clicked.connect(lambda: self.handleButton(akinator_model.DefaultResponse.YES))
        yesbutton.setToolTip('Yes')
        layout.addWidget(yesbutton)
        
        maybebutton = QPushButton('Don\'t know', self)
        maybebutton.clicked.connect(lambda: self.handleButton(akinator_model.DefaultResponse.DONTKNOW))
        maybebutton.setToolTip('Don\'t know')
        layout.addWidget(maybebutton)
        
        nobutton = QPushButton('No', self)
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