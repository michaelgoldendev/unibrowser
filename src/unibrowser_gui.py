from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

import numpy as np
import sys
import akinator_model
import akinator_geography_questionsanswers
import worldmapwindow
import map_info

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.mapinfo = map_info.MapInfo()
        
        self.model = akinator_model.Akinator()
        akinator_geography_questionsanswers.setup_geography_akinator(self.model, self.mapinfo)
        
        self.label = QLabel("")
        
        #self.actionExit.triggered.connect(self.close)
        self.worldmapwindow = worldmapwindow.WorldMapWindow(self.mapinfo)
        self.initUI()        
        self.updateWorldMap(self.model)
        
        self.nextquestion()
    
    def close(self):
        exit()
        
        
    def initUI(self):     
        self.setWindowTitle("Unibrowser")
        
        layout = QVBoxLayout()
        
        questionfont = QFont()
        questionfont.setPointSize(15)
        questionfont.setBold(True)
        questionfont.setWeight(75)
        
        self.label.setFont(questionfont)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        answerbuttonfont = QFont()
        answerbuttonfont.setPointSize(13)
        answerbuttonfont.setBold(True)
        #answerbuttonfont.setWeight(75)
        
        self.yesbutton = QPushButton('Yes', self)
        self.yesbutton.setFont(answerbuttonfont)
        self.yesbutton.clicked.connect(lambda: self.handleButton(0))
        self.yesbutton.setToolTip('Yes')
        layout.addWidget(self.yesbutton)
        
        self.probablyyesbutton = QPushButton('Probably yes', self)
        self.probablyyesbutton.setFont(answerbuttonfont)
        self.probablyyesbutton.clicked.connect(lambda: self.handleButton(1))
        self.probablyyesbutton.setToolTip('Probably yes')
        layout.addWidget(self.probablyyesbutton)
       
        self.maybebutton = QPushButton('Don\'t know', self)
        self.maybebutton.setFont(answerbuttonfont)
        self.maybebutton.clicked.connect(lambda: self.handleButton(2))
        self.maybebutton.setToolTip('Don\'t know')
        layout.addWidget(self.maybebutton)
        
        self.probablynobutton = QPushButton('Probably no', self)
        self.probablynobutton.setFont(answerbuttonfont)
        self.probablynobutton.clicked.connect(lambda: self.handleButton(3))
        self.probablynobutton.setToolTip('Probably no')
        layout.addWidget(self.probablynobutton)       
        
        self.nobutton = QPushButton('No', self)
        self.nobutton.setFont(answerbuttonfont)
        self.nobutton.clicked.connect(lambda: self.handleButton(4))
        self.nobutton.setToolTip('No')
        layout.addWidget(self.nobutton)
        
        
        self.setLayout(layout)
        self.show()
        
    def handleButton(self, answer):
        #self.model.bayesianupdate_discreteanswer(self.qkey, answer)
        if answer == 0: # Yes
            self.model.bayesianupdate_probanswer(self.qkey, [0.98, 0.02])
        elif  answer == 1:
            self.model.bayesianupdate_probanswer(self.qkey, [0.80, 0.20])
        elif  answer == 2:
            self.model.bayesianupdate_probanswer(self.qkey, [0.50, 0.50])
        elif answer == 3:
            self.model.bayesianupdate_probanswer(self.qkey, [0.20, 0.80])
        elif answer == 4:
            self.model.bayesianupdate_probanswer(self.qkey, [0.02, 0.98])
            
        
        self.nextquestion()
       
            
    def updateWorldMap(self, akinator):
        for (state,prob) in zip(akinator.statelist, akinator.stateprobs):
            self.worldmapwindow.canvas.setlocationcolourbyvalue(state,prob,drawimmediately=False)
        self.worldmapwindow.canvas.draw()
        self.worldmapwindow.listwidget.updatelist(akinator.stateprobs, self.mapinfo)
    
    def nextquestion(self):
        self.qkey = self.model.getnextquestion()
        if self.qkey >= 0:
            questiontype = self.model.questiontypes[self.qkey]
            if questiontype == akinator_model.QuestionType.TERMINAL:
                self.probablyyesbutton.setEnabled(False)
                self.maybebutton.setEnabled(False)
                self.probablynobutton.setEnabled(False)
            else:
                self.probablyyesbutton.setEnabled(True)
                self.maybebutton.setEnabled(True)
                self.probablynobutton.setEnabled(True)
            
            self.model.usedquestions.append(self.qkey)
            self.label.setText("%d. %s" % (len(self.model.usedquestions), self.model.questions[self.qkey]))
            self.updateWorldMap(self.model)
        else:
            self.model.usedquestions = []
            
        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = MainWindow()    
    sys.exit(app.exec_())