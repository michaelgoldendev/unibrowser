import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

from enum import IntEnum
import random

class Answer(IntEnum):
    NONE = -1
    YES = 0
    PROBABLYYES = 1
    DONTKNOW = 2
    PROBABLYNO = 3    
    NO = 4
    
class AnswerPanelWidget(QWidget):
    
    answerclicked = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.mouseinteractionenabled = True
        
        
    def initUI(self):
        self.setMouseTracking(True)
        
        self.pressedanswer = Answer.NONE
        self.mouseoveranswer = Answer.NONE
        self.softoptionsenabled = True
        self.answerclicked.connect(self.answerClickedEvent)
        
        self.answers = ["Yes", "Probably\nyes", "Don't\nknow", "Probably\nno", "No"]
        self.blockrects = []
        self.blockwidth = 110
        self.blockheight = self.blockwidth
        self.blockrounding = 7
        self.buttonspacing = 30
        for (index,ans) in enumerate(self.answers):
            self.blockrects.append(QRectF( self.buttonspacing+index*(self.blockwidth+ self.buttonspacing),  self.buttonspacing,  self.blockwidth,  self.blockheight))      
        
        self.facepixmaps = [QPixmap("../images/faces/example1.jpg").scaledToWidth(self.blockwidth, mode=Qt.SmoothTransformation)]
        panelwidth =  self.buttonspacing+len(self.answers)*(self.blockwidth+ self.buttonspacing) 
        self.setGeometry(300, 300, panelwidth,  self.blockwidth+ self.buttonspacing*2)
        
    def f(self):
        #self.mouseoveranswer = (self.mouseoveranswer+1) % len(self.answers)
        self.mouseoveranswer = (self.mouseoveranswer + random.randint(2, len(self.answers)-1)) % len(self.answers)
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
            
        self.mouseinteractionenabled  = not self.mouseinteractionenabled
        if not self.mouseinteractionenabled:
            self.timer = QTimer()
            self.timer.timeout.connect(self.f)
            self.timer.start(250)
        else:
            self.timer.stop()
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
        
        fontsizes = [18,13,13,13,18]
        for (index,(answer,blockrect)) in enumerate(zip(self.answers, self.blockrects)):
            fillcolor = unselectedcolor
            qp.setFont(QFont('Roboto', fontsizes[index], weight=QFont.Normal))
            if self.mouseoveranswer == index:
                fillcolor = mouseovercolor
                qp.setFont(QFont('Roboto', fontsizes[index], weight=QFont.Bold))
            if self.pressedanswer == index:
                qp.setFont(QFont('Roboto', fontsizes[index], weight=QFont.Bold))
                fillcolor = pressedcolor
            
            
            blockpath = QPainterPath()
            blockpath.addRoundedRect(blockrect, self.blockrounding, self.blockrounding);     
            
            if self.mouseoveranswer == index:
                facerect = QRectF(0.0,0.0, self.blockwidth, self.blockheight)
                tempbrush = qp.brush()
                brush = QBrush(self.facepixmaps[0]);
                t = QTransform()
                t.translate(blockrect.x(), blockrect.y())
                brush.setTransform(t)
                qp.setBrush(brush);
                qp.drawRoundedRect(blockrect, self.blockrounding, self.blockrounding)
                qp.setBrush(tempbrush)
            else:      
                qp.fillPath(blockpath, fillcolor)
            
            #qp.drawPixmap(blockrect.toRect(), self.facepixmaps[0])
            if self.pressedanswer == index:
                qp.setPen(pressedborderpen)            
            else:
                qp.setPen(borderpen)
            qp.drawPath(blockpath)            
            
            qp.setPen(Qt.black)
            qp.drawText(blockrect, Qt.AlignCenter, answer)

class QuestionPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Unibrowser')
        self.setMouseTracking(True)
        self.show()
        
        self.vboxlayout  = QVBoxLayout()
        
        self.mousebcitoggle = QPushButton("Mouse input")
        self.mousebcitoggle.setCheckable(True)
        self.mousebcitoggle.clicked.connect(self.btnstate)
        self.mousebcitoggle.setFixedWidth(200)
        self.vboxlayout.addWidget(self.mousebcitoggle)
        
        labelfont = QFont()
        labelfont.setPointSize(15)
        #questionfont.setBold(True)
        #questionfont.setWeight(75)
        self.label = QLabel("Please calibrate by the Brain Computer Interface.")
        self.label.setFont(labelfont)
        self.label.setAlignment(Qt.AlignCenter)
        self.vboxlayout.addWidget(self.label)
        
        self.answerpanel = AnswerPanelWidget()
        self.vboxlayout.addWidget(self.answerpanel, 0)
        self.setLayout(self.vboxlayout)
        self.setGeometry(300,300,self.answerpanel.width(), 500)
    
    def btnstate(self):
      if self.mousebcitoggle.isChecked():
         self.mousebcitoggle.setText("Brain input")
      else:
         self.mousebcitoggle.setText("Mouse input")
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = QuestionPanel()
    sys.exit(app.exec_())