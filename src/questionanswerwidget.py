import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from PyQt5.QtChart import *

from enum import IntEnum
import random
from functools import partial
import math
import os
import numpy as np

def samplediscrete(probabilityvec):
    r = random.random()*sum(probabilityvec)
    cumsum = 0.0
    for (i,v) in enumerate(probabilityvec):
        cumsum += v
        if r <= cumsum:
            return i
    return 0
    

RELEASE_VERSION = False

class Answer(IntEnum):
    NONE = -1
    YES = 0      
    NO = 1
    PROBABLYYES = 2
    DONTKNOW = 3
    PROBABLYNO = 4  

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
    SSVEP = 2
    
class AnswerPanelWidget(QWidget):
    
    answerclicked = pyqtSignal(int)
    
    def setInputMethod(self, inputmethod):        
        self.inputmethod = inputmethod
        if self.inputmethod == InputMethod.MOUSE:
            self.setMouseTracking(True)
        else:
            self.setMouseTracking(False)
    
    def __init__(self, inputmethod):
        super().__init__()        
        self.setInputMethod(inputmethod)
        
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
        self.panelpadding = 2
        self.blockwidth = 120
        self.blockheight = self.blockwidth
        self.blockrounding = 7
        self.buttonspacing = 500
        self.yoffset = 0
        for (index,ans) in enumerate(self.answers):
            self.blockrects.append(QRectF(self.panelpadding + index*(self.blockwidth+self.buttonspacing),  self.panelpadding + self.yoffset,  self.blockwidth,  self.blockheight))      
        
        self.facepixmaps = []
        
        self.facepixmaps.append(QPixmap(os.path.abspath(os.path.join(script_path, '../images/faces/jennifer-lawrence.jpg'))).scaledToWidth(self.blockwidth, mode=Qt.SmoothTransformation))
        self.facepixmaps.append(QPixmap(os.path.abspath(os.path.join(script_path, '../images/faces/nicolas-cage.jpg'))).scaledToWidth(self.blockwidth, mode=Qt.SmoothTransformation))
        self.panelwidth =  2*self.panelpadding + self.buttonspacing*(len(self.answers)-1) + self.blockwidth*len(self.answers) 
        self.panelheight = 2*self.panelpadding + self.blockheight + self.yoffset
        self.setFixedWidth(self.panelwidth)
        self.setFixedHeight(self.panelheight)
        self.mouseinteractionenabled = True
        
    def setFrequencies(self, frequencies):
        self.frequencies = frequencies 
        self.periodsinmilli = [1000.0/freq/self.divisions for freq in self.frequencies]
        
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
        
    def resetSelected(self):
        for (index,blockrect) in enumerate(self.blockrects):
            self.answerstates[index] = 0
        self.repaint()
        
    def setSelected(self, selectedindex):
        for (index,blockrect) in enumerate(self.blockrects):
            self.answerstates[index] = 0
        self.answerstates[selectedindex] = 2
        self.repaint()
        
            
        
    def redraw(self, event, qp):
        qp.setRenderHint(QPainter.TextAntialiasing)
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        
        path = QPainterPath()
        
        borderpen = QPen(QColor(100,100,100,255), 2)
        pressedborderpen = QPen(QColor(25,25,25,255), 3)
        
        unselectedcolor = Qt.white
        mouseovercolor = QColor(225,225,225,255)
        pressedcolor = QColor(175,175,175,255)        
        selectedcolor = QColor(255,128,128,255)
        selectedcolor = pressedcolor
        
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
            elif self.answerstates[index] == 2:
                qp.fillPath(blockpath, selectedcolor)
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

class QuestionAnswerWidget(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.inputmethod =  InputMethod.SSVEP # InputMethod.MOUSE, InputMethod.SSVEP
        
        self.setWindowTitle('Unibrowser')
        self.setMouseTracking(True)
        
        self.vboxlayout  = QVBoxLayout()        
        self.vboxlayout.setAlignment(Qt.AlignCenter)
        
        
        self.warningtimesecs = 3
        self.questiontimeoutmillis = 15000.0 if RELEASE_VERSION else 3000.0
        self.questiontimeoutmillis += self.warningtimesecs*1000.0
        self.timerintervalmillis = 1000.0
        self.questionno = 0
        self.questionframe = 0
        self.questiontimer = QTimer()        
        self.questiontimer.timeout.connect(self.updatequestion)
        
        self.bcianimationtimeoutmillis = 6000.0 if RELEASE_VERSION else 1000.0
        self.choicetimeoutmillis = 4000.0 if RELEASE_VERSION else 2000.0
        
        labelfont = QFont()
        labelfont.setPointSize(16)
        #questionfont.setBold(True)
        #questionfont.setWeight(75)
        self.label = QLabel("")
        self.label.setFont(labelfont)
        self.label.setAlignment(Qt.AlignCenter)
        self.vboxlayout.addWidget(self.label)
        
        self.answerpanel = AnswerPanelWidget(self.inputmethod)
        self.vboxlayout.addWidget(self.answerpanel)        
        
        self.shownextquestion()
        
        self.setLayout(self.vboxlayout)
        
    
    def refreshquestiontext(self):
        if self.inputmethod == InputMethod.MOUSE:
            self.label.setText(self.parent.questiontext)
        elif self.inputmethod == InputMethod.SSVEP:
            elapsedtimequestionmillis = self.questionframe*self.timerintervalmillis
            elapsedtimequestionsecs = math.ceil((self.questiontimeoutmillis-elapsedtimequestionmillis)/1000.0)
            if elapsedtimequestionsecs > self.warningtimesecs:
                self.label.setText("%s\n(%d seconds)" % (self.parent.questiontext, elapsedtimequestionsecs-self.warningtimesecs))
            else:
                self.label.setText("%s\nNow focus on your best guess and count the flashes." % self.parent.questiontext)
            return elapsedtimequestionmillis
    
    
    def shownextquestion(self):
        self.parent.nextquestion()
        self.answerpanel.resetSelected()
        self.refreshquestiontext()
        if self.inputmethod == InputMethod.SSVEP:
            self.questiontimer.start(self.timerintervalmillis)
    
    def updatequestion(self):
        self.questionframe += 1        
        elapsedtimequestionmillis = self.refreshquestiontext()
        if elapsedtimequestionmillis >= self.questiontimeoutmillis:            
            self.questiontimer.stop()
            self.questionframe = 0
            self.startBCI()
            QTimer.singleShot(self.bcianimationtimeoutmillis, self.stopBCI)
    
    def startBCI(self):
        self.answerpanel.startBCIanimation()
    
    def stopBCI(self):
        answervec = self.parent.model.answerdict[('South Africa',self.parent.qkey)]
        #simulatedanswer = samplediscrete(answervec)
        simulatedanswer = np.argmax(answervec)
        print(self.parent.model.questions[self.parent.qkey])
        print("%s, choice %d" % (answervec,simulatedanswer))
        self.answerpanel.stopBCIanimation()
        self.answerpanel.setSelected(simulatedanswer)
        QTimer.singleShot(self.choicetimeoutmillis, partial(self.answerpanel.answerclicked.emit, simulatedanswer))
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = QuestionAnswerWidget()
    sys.exit(app.exec_())