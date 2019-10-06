from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import sys
import akinator_model
import akinator_geography_questionsanswers
import map_info
from akinator_model import QuestionType

from worldmapwidget import WorldMapCanvas
from questionanswerwidget import QuestionAnswerWidget
from questionanswerwidget import Answer
import countrylistwidget

import os
script_path = os.path.dirname(os.path.abspath( __file__ ))

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        #self.setFixedWidth(800)
        
        self.qkey = -1
        self.questiontext = ""
        
        self.mapinfo = map_info.MapInfo()
        
        self.model = akinator_model.Akinator()
        akinator_geography_questionsanswers.setup_geography_akinator(self.model, self.mapinfo)
        
        #self.actionExit.triggered.connect(self.close)
        
        
        self.setWindowTitle("Unibrowser")        
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.canvas =  WorldMapCanvas(self.mapinfo, parent=self, width=10.5, height=9.5)
        self.listwidget = countrylistwidget.CountryListWidget()
        self.listwidget.setFixedWidth(450)
        
        self.questionanswerpanel = QuestionAnswerWidget(self)
        #self.questionanswerpanel.setFixedHeight(200)
        self.questionanswerpanel.answerpanel.answerclicked.connect(self.answerClickedEvent)
        
        
        
        mainlayout = QHBoxLayout()
        
        leftframe =  QFrame()
        leftframelayout = QVBoxLayout()
        leftframelayout.setAlignment(Qt.AlignCenter)
        leftframelayout.addWidget(self.questionanswerpanel)        
        leftframelayout.addWidget(self.canvas)        
        leftframe.setLayout(leftframelayout)
        
        rightframe = QFrame()
        rightframelayout = QVBoxLayout()
        rightframelayout.setAlignment(Qt.AlignCenter)
        labelfont = QFont()
        labelfont.setPointSize(18)
        #labelfont.setBold(True)
        #labelfont.setWeight(70)
        rankinglabel = QLabel("Country ranking")
        rankinglabel.setFont(labelfont)
        rankinglabel.setAlignment(Qt.AlignCenter)
        rightframelayout.addWidget(rankinglabel)
        rightframelayout.addWidget(self.listwidget)
        rightframe.setLayout(rightframelayout)
        
        mainlayout.addWidget(leftframe, 1)
        mainlayout.addWidget(rightframe)     
        
      
        
        
        self.updateWorldMap(self.model)
        self.setLayout(mainlayout)
        
        
        self.show()
        
        
    
    def close(self):
        exit()
   
        
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
    
    def answerClickedEvent(self, answer):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if answer == Answer.YES: # Yes
            self.model.bayesianupdate_probanswer(self.qkey, [0.98, 0.02])
        elif  answer == Answer.PROBABLYYES:
            self.model.bayesianupdate_probanswer(self.qkey, [0.80, 0.20])
        elif  answer == Answer.DONTKNOW:
            self.model.bayesianupdate_probanswer(self.qkey, [0.50, 0.50])
        elif answer == Answer.PROBABLYNO:
            self.model.bayesianupdate_probanswer(self.qkey, [0.20, 0.80])
        elif answer == Answer.NO:
            self.model.bayesianupdate_probanswer(self.qkey, [0.02, 0.98])
        #self.nextquestion()
        questiontype = self.model.questiontypes[self.qkey]
        if questiontype == QuestionType.TERMINAL:
            if answer == Answer.YES:
                self.canvas.showUnicorn()
                self.questionanswerpanel.label.setText("The Unibrow sees all.")
        else:
            self.questionanswerpanel.shownextquestion()
        QApplication.restoreOverrideCursor()
       
            
    def updateWorldMap(self, akinator):
        for (state,prob) in zip(akinator.statelist, akinator.stateprobs):
            self.canvas.setlocationcolourbyvalue(state,prob,drawimmediately=False)
        self.canvas.draw()
        self.listwidget.updatelist(akinator.stateprobs, self.mapinfo, top=1000)
    
    def nextquestion(self):
        self.qkey = self.model.getnextquestion()
        if self.qkey >= 0:
            questiontype = self.model.questiontypes[self.qkey]
            """
            if questiontype == akinator_model.QuestionType.TERMINAL:
                self.questionanswerpanel.softoptionsenabled = False
                self.questionanswerpanel.repaint()
            else:
                self.questionanswerpanel.softoptionsenabled = True
                self.questionanswerpanel.repaint()
            """
            
            """
            if questiontype == akinator_model.QuestionType.TERMINAL:
                self.probablyyesbutton.setEnabled(False)
                self.maybebutton.setEnabled(False)
                self.probablynobutton.setEnabled(False)
            else:
                self.probablyyesbutton.setEnabled(True)
                self.maybebutton.setEnabled(True)
                self.probablynobutton.setEnabled(True)
            """
            
            self.model.usedquestions.append(self.qkey)          
        else:
            self.model.usedquestions = []
        
        self.questiontext = "%d. %s" % (len(self.model.usedquestions), self.model.questions[self.qkey])
        #self.questionanswerpanel.questiontext = "%d. %s" % (len(self.model.usedquestions), self.model.questions[self.qkey])
        #self.questionanswerpanel.shownextquestion()
        self.updateWorldMap(self.model)
        
        return self.qkey
        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = MainWindow() 
    ex.showMaximized()
    sys.exit(app.exec_())