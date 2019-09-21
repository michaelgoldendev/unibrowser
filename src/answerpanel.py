import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from enum import IntEnum

class Answer(IntEnum):
    NONE = 0
    YES = 1
    PROBABLYYES = 2
    DONTKNOW = 3
    PROBABLYNO = 4    
    NO = 5

class AnswerPanel(QWidget):
    
    answerclicked = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        self.width = 800
        self.height = 300
        self.setGeometry(300, 300, self.width, self.height)
        
        self.midpoint = 40
        self.arrowheight = self.midpoint*2.0
        self.arrowheadlength = 60
        self.arrowmidlength = self.width-self.arrowheadlength*2.0
        self.arrowinnerheight = 0 
        
        
        self.setWindowTitle('Answer Picker')
        self.setMouseTracking(True)
        self.show()
        
        self.highlightedanswer = Answer.NONE
        self.selectedanswer = Answer.NONE
        self.answerclicked.connect(self.answerClickedEvent)

    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.redraw(event, qp)
        qp.end()
    
    def mouseMoveEvent(self, event): 
        previous = self.selectedanswer
        if event.y() <= 80:
            if event.x() < self.rect().width()/5.0:
                self.selectedanswer= Answer.NO
            elif event.x() < self.rect().width()*2.0/5.0:
                self.selectedanswer= Answer.PROBABLYNO
            elif event.x() < self.rect().width()*3.0/5.0:
                self.selectedanswer= Answer.DONTKNOW
            elif event.x() < self.rect().width()*4.0/5.0:
                self.selectedanswer = Answer.PROBABLYYES
            elif event.x() < self.rect().width():
                self.selectedanswer = Answer.YES
        else:
            self.selectedanswer = Answer.NONE
        if previous != self.selectedanswer:        
            self.repaint()
    
    def mousePressEvent(self, event):
        self.highlightedanswer = self.selectedanswer
        self.repaint()
    
    def mouseReleaseEvent(self, event):
        if self.selectedanswer != Answer.NONE:
            self.highlightedanswer = Answer.NONE
            self.answerclicked.emit(self.selectedanswer)
            self.highlightedanswer = Answer.NONE
            self.selectedanswer = Answer.NONE
        self.repaint()
    
    def answerClickedEvent(self, event):
        print(event)        
        
    def redraw(self, event, qp):
        qp.setRenderHint(QPainter.TextAntialiasing)
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        
        
        points = [
            QPoint(0,self.midpoint), 
            QPoint(self.arrowheadlength,0), 
            QPoint(self.arrowheadlength,self.arrowinnerheight),
            QPoint(self.arrowheadlength+self.arrowmidlength,self.arrowinnerheight),
            QPoint(self.arrowheadlength+self.arrowmidlength,0),
            QPoint(self.arrowheadlength+self.arrowmidlength+self.arrowheadlength,self.midpoint),
            QPoint(self.arrowheadlength+self.arrowmidlength,2.0*self.midpoint),
            QPoint(self.arrowheadlength+self.arrowmidlength,2.0*self.midpoint-self.arrowinnerheight),
            QPoint(self.arrowheadlength,2.0*self.midpoint-self.arrowinnerheight),
            QPoint(self.arrowheadlength,2.0*self.midpoint)
            ]
        qp.setPen(Qt.NoPen);
        grad = QLinearGradient(0,self.midpoint, self.arrowheadlength+self.arrowmidlength+self.arrowheadlength,self.midpoint)
        grad.setColorAt(0.0, QColor(250,61,63))
        grad.setColorAt(0.5, QColor(79,88,167))
        grad.setColorAt(1.0, QColor(22,254,104))
        qp.setBrush(QBrush(grad))
        poly = QPolygon(points) 
        qp.drawPolygon(poly)
      
       
        
        texty = self.midpoint*0.0
        
        normalcolor = QColor(0, 0, 0)
        pressedcolor = QColor(0,0,0,150)
        if self.highlightedanswer != Answer.NONE:
            pressedcolor = QColor(0,0,0)
            
        textpos = QRect(0.0, texty,self.arrowheadlength*2.0-5.0,self.arrowheight)        
        if self.selectedanswer == Answer.NO:
             qp.setPen(pressedcolor)
             qp.setFont(QFont('Roboto', 20, weight=QFont.Bold))
        else:
             qp.setPen(normalcolor)
             qp.setFont(QFont('Roboto', 18, weight=QFont.Normal))             
        qp.drawText(textpos, Qt.AlignCenter, "No")
       
        if self.selectedanswer == Answer.YES:
             qp.setPen(pressedcolor)
             qp.setFont(QFont('Roboto', 20, weight=QFont.Bold))
        else:
             qp.setPen(normalcolor)
             qp.setFont(QFont('Roboto', 18, weight=QFont.Normal))
        textpos = QRect(self.arrowmidlength+5.0,texty,self.arrowheadlength*2.0,self.arrowheight)
        qp.drawText(textpos, Qt.AlignCenter, "Yes")
        
        if self.selectedanswer == Answer.DONTKNOW:
             qp.setPen(pressedcolor)
             qp.setFont(QFont('Roboto', 16, weight=QFont.Bold))
        else:
             qp.setPen(normalcolor)
             qp.setFont(QFont('Roboto', 14, weight=QFont.Normal))
        textpos = QRect(self.arrowheadlength,texty,self.arrowmidlength,self.arrowheight)
        qp.drawText(textpos, Qt.AlignCenter, "Don't\nknow")
        
        if self.selectedanswer == Answer.PROBABLYNO:
             qp.setPen(pressedcolor)
             qp.setFont(QFont('Roboto', 16, weight=QFont.Bold))
        else:
             qp.setPen(normalcolor)
             qp.setFont(QFont('Roboto', 14, weight=QFont.Normal))
        textpos = QRect(0,texty,(self.arrowheadlength+self.arrowmidlength+self.arrowheadlength)/2.0,self.arrowheight)
        qp.drawText(textpos, Qt.AlignCenter, "Probably\nno")
        
        if self.selectedanswer == Answer.PROBABLYYES:
             qp.setPen(pressedcolor)
             qp.setFont(QFont('Roboto', 16, weight=QFont.Bold))
        else:
             qp.setPen(normalcolor)
             qp.setFont(QFont('Roboto', 14, weight=QFont.Normal))
        textpos = QRect((self.arrowheadlength+self.arrowmidlength+self.arrowheadlength)/2.0,texty,(self.arrowheadlength+self.arrowmidlength+self.arrowheadlength)/2.0,self.arrowheight)
        qp.drawText(textpos, Qt.AlignCenter, "Probably\nyes")
                
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = AnswerPanel()
    sys.exit(app.exec_())