import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

from enum import IntEnum
import random
from functools import partial
import math
import os

script_path = os.path.dirname(os.path.abspath( __file__ ))

class PausableQTimer(QTimer):
    
    def __init__(self):
        self.remainingtime = 0
    
    def pause(self):
        self.remainingtime = self.remainingTime()
        self.stop()
        self.setInterval(self.remainingtime)
    
    def resume(self):
        self.start()
        
    

class InputMethod(IntEnum):
    MOUSE = 0
    P300SPELLING = 1
    POWERSPECTRUM = 2

"""
class Answer(IntEnum):
    NONE = -1
    YES = 0
    PROBABLYYES = 1
    DONTKNOW = 2
    PROBABLYNO = 3    
    NO = 4
"""
class Answer(IntEnum):
    NONE = -1
    YES = 0   
    NO = 1
    
class AnswerPanelWidget(QWidget):
    
    answerclicked = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()        
        self.initUI()
        self.mouseinteractionenabled = True
        
        
    def initUI(self):
        self.setMouseTracking(False)
        
        self.pressedanswer = Answer.NONE
        self.mouseoveranswer = Answer.NONE
        self.softoptionsenabled = True
        self.answerclicked.connect(self.answerClickedEvent) 
        
        self.answers = ["Yes", "No"]
        self.answerstates = [0 for i in range(len(self.answers))]
        self.frequencies = [3.0,4.5]   
        self.divisions = 4
        self.fractionofdivision = 1 # show face for 1/4 of time
        self.periodsinmilli = [1000.0/freq/self.divisions for freq in self.frequencies]
        self.counts = [0 for i in range(len(self.answers))]
        
        self.timers = [QTimer() for i in range(len(self.answers))]
        for (index, timer) in enumerate(self.timers):
            timer.timeout.connect(partial(self.flash,index))
        
        self.blockrects = []
        self.blockwidth = 200
        self.blockheight = self.blockwidth
        self.blockrounding = 7
        self.buttonspacing = 250
        self.yoffset = 0
        for (index,ans) in enumerate(self.answers):
            self.blockrects.append(QRectF(index*(self.blockwidth+self.buttonspacing),  self.yoffset,  self.blockwidth,  self.blockheight))      
        
        self.facepixmaps = []
        
        self.facepixmaps.append(QPixmap(os.path.abspath(os.path.join(script_path, '../images/faces/jennifer-lawrence.jpg'))).scaledToWidth(self.blockwidth, mode=Qt.SmoothTransformation))
        self.facepixmaps.append(QPixmap(os.path.abspath(os.path.join(script_path, '../images/faces/nicolas-cage.jpg'))).scaledToWidth(self.blockwidth, mode=Qt.SmoothTransformation))
        self.panelwidth =  self.buttonspacing*(len(self.answers)-1) + self.blockwidth*len(self.answers)
        self.panelheight = self.blockheight + self.yoffset
        self.setFixedWidth(self.panelwidth)
        self.setFixedHeight(self.panelheight)
                
        
    def flash(self, index):
        if self.counts[index] % self.divisions < self.fractionofdivision:
            self.answerstates[index] = 1 # show face
        else:
            self.answerstates[index] = 0 # don't show face
        self.counts[index] += 1
        self.repaint()
        
    def startBCIanimation(self):
        for (index,period) in enumerate(self.periodsinmilli):
            self.counts[index] = 0
            self.timers[index].start(period)
    
    def stopBCIanimation(self):
        for (index,period) in enumerate(self.periodsinmilli):
                self.timers[index].stop()
                self.answerstates[index] = 0
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.redraw(event, qp)
        qp.end()
    
    def mouseMoveEvent(self, event): 
        if self.mouseinteractionenabled:
            previous = self.mouseoveranswer
            self.pressedanswer = Answer.NONE
            self.mouseoveranswer = Answer.NONE
            for (index,blockrect) in enumerate(self.blockrects):
                if blockrect.contains(event.x(), event.y()):
                    self.mouseoveranswer = index
            if previous != self.mouseoveranswer:        
                self.repaint()
    
    def mousePressEvent(self, event):
        if self.mouseinteractionenabled:
            self.pressedanswer = self.mouseoveranswer
            self.repaint()
    
    def mouseReleaseEvent(self, event):
        if self.mouseinteractionenabled:
            if self.mouseoveranswer != Answer.NONE:
                self.pressedanswer = Answer.NONE
                self.answerclicked.emit(self.mouseoveranswer)
                self.pressedanswer = Answer.NONE
            self.repaint()
        else:            
            #self.mouseinteractionenabled  = not self.mouseinteractionenabled
            if not self.mouseinteractionenabled:
                self.startanimation()
                self.mouseoveranswer = Answer.NONE            
            else:
                for (index,timer) in enumerate(self.timers):
                    timer.stop()                
                    self.answerstates[index] = 0
                    self.mouseoveranswer = Answer.NONE
                self.repaint()
    
    def answerClickedEvent(self, event):
        print(event)
        
    def redraw(self, event, qp):
        qp.setRenderHint(QPainter.TextAntialiasing)
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        
        path = QPainterPath()
        
        borderpen = QPen(QColor(100,100,100,255), 2)
        pressedborderpen = QPen(QColor(25,25,25,255), 3)
        
        unselectedcolor = Qt.white
        mouseovercolor = QColor(225,225,225,255)
        pressedcolor = QColor(175,175,175,255)
        
        fontpenblack = QPen(QColor(0,0,0,225))
        fontpentransparent = QPen(QColor(0,0,0,30))
        
        #fontsizes = [18,13,13,13,18]
        fontsizes = [36,36]
        for (index,(answer,blockrect)) in enumerate(zip(self.answers, self.blockrects)):
                
            fillcolor = unselectedcolor
            qp.setFont(QFont('Roboto', fontsizes[index], weight=QFont.Normal))
            if self.answerstates[index] == 1 or self.mouseoveranswer == index:
                fillcolor = mouseovercolor
                qp.setFont(QFont('Roboto', fontsizes[index], weight=QFont.Bold))
            if self.pressedanswer == index:
                qp.setFont(QFont('Roboto', fontsizes[index], weight=QFont.Bold))
                fillcolor = pressedcolor
            
            
            blockpath = QPainterPath()
            blockpath.addRoundedRect(blockrect, self.blockrounding, self.blockrounding);                 
            
            if self.answerstates[index] == 1 or self.mouseoveranswer == index:
                facerect = QRectF(0.0,0.0, self.blockwidth, self.blockheight)
                tempbrush = qp.brush()
                brush = QBrush(self.facepixmaps[index]);
                t = QTransform()
                t.translate(blockrect.x(), blockrect.y())
                brush.setTransform(t)
                qp.setBrush(brush);
                qp.drawRoundedRect(blockrect, self.blockrounding, self.blockrounding)
                qp.setBrush(tempbrush)
            else:      
                qp.fillPath(blockpath, fillcolor)
            
            if self.pressedanswer == index:
                qp.setPen(pressedborderpen)            
            else:
                qp.setPen(borderpen)
            qp.drawPath(blockpath)            
            
            
            qp.setPen(fontpenblack)
            if self.answerstates[index] == 1:
                qp.setPen(fontpentransparent)
            qp.drawText(blockrect, Qt.AlignCenter, answer)

class QuestionPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.inputmethod = InputMethod.MOUSE
        
        self.setWindowTitle('Unibrowser')
        self.setMouseTracking(True)
        
        self.vboxlayout  = QVBoxLayout()        
        self.vboxlayout.setAlignment(Qt.AlignCenter)
        
        
        self.warningtimesecs = 3
        self.questiontimeoutmillis = 15000.0
        self.questiontimeoutmillis += self.warningtimesecs*1000.0
        self.timerintervalmillis = 1000.0
        self.questiontext = "Is your country in the Northern Hemisphere?"
        self.questionno = 0
        self.questionframe = 0
        self.questiontimer = QTimer()        
        self.questiontimer.timeout.connect(self.updatequestion)
        
        self.bcianimationtimeoutmillis = 6000.0
        
        """
        self.mousebcitoggle = QPushButton("Mouse input")
        self.mousebcitoggle.setCheckable(True)
        self.mousebcitoggle.clicked.connect(self.btnstate)
        self.mousebcitoggle.setFixedWidth(200)
        self.vboxlayout.addWidget(self.mousebcitoggle)
        """
        
        labelfont = QFont()
        labelfont.setPointSize(16)
        #questionfont.setBold(True)
        #questionfont.setWeight(75)
        self.label = QLabel("")
        self.label.setFont(labelfont)
        self.setFixedWidth(1000)
        self.label.setAlignment(Qt.AlignCenter)
        self.vboxlayout.addWidget(self.label)
        
        self.answerpanel = AnswerPanelWidget()
        self.vboxlayout.addWidget(self.answerpanel)
        self.setLayout(self.vboxlayout)
        
        self.shownextquestion()
        
        self.show()
        
    
    def refreshquestiontext(self):
        elapsedtimequestionmillis = self.questionframe*self.timerintervalmillis
        elapsedtimequestionsecs = math.ceil((self.questiontimeoutmillis-elapsedtimequestionmillis)/1000.0)
        if elapsedtimequestionsecs > self.warningtimesecs:
            self.label.setText("%s\n(%d seconds)" % (self.questiontext, elapsedtimequestionsecs-self.warningtimesecs))
        else:
            self.label.setText("%s\nNow focus on your answer and try count the flashes." % self.questiontext)
        return elapsedtimequestionmillis
    
    
    def shownextquestion(self):
        self.refreshquestiontext()
        self.questiontimer.start(self.timerintervalmillis)        
    
    def updatequestion(self):
        self.questionframe += 1        
        elapsedtimequestionmillis = self.refreshquestiontext()
        if elapsedtimequestionmillis >= self.questiontimeoutmillis:            
            self.questiontimer.stop()
            self.questionframe = 0
            #self.shownextquestion()
            self.startBCI()
            QTimer.singleShot(self.bcianimationtimeoutmillis, self.stopBCI)
    
    def startBCI(self):
        self.answerpanel.startBCIanimation()
    
    def stopBCI(self):
        self.answerpanel.stopBCIanimation()
        self.shownextquestion()
    
    def btnstate(self):
      if self.mousebcitoggle.isChecked():
         self.mousebcitoggle.setText("Brain input")
      else:
         self.mousebcitoggle.setText("Mouse input")
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = QuestionPanel()
    sys.exit(app.exec_())