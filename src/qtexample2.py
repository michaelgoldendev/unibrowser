from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.label = QLabel('Is your character real?')        
        
        self.questions = []
        self.questions.append("Is your character real")
        self.questions.append("Is your character male?")
        self.questions.append("Is your character tall?")
        self.questions.append("Do they have special powers?")        
        self.qindex = 0
                        
        self.initUI()
        
        
    def initUI(self):     
        self.setWindowTitle("Unibrowser")
        """
        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.show()
        """
        layout = QVBoxLayout()
        
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        yesbutton = QPushButton('Yes', self)
        yesbutton.clicked.connect(lambda: self.handleButton('yes'))
        yesbutton.setToolTip('Yes')
        layout.addWidget(yesbutton)
        
        maybebutton = QPushButton('Maybe', self)
        maybebutton.clicked.connect(lambda: self.handleButton('maybe'))
        maybebutton.setToolTip('Maybe')
        layout.addWidget(maybebutton)
        
        nobutton = QPushButton('No', self)
        nobutton.clicked.connect(lambda: self.handleButton('no'))
        nobutton.setToolTip('No')
        layout.addWidget(nobutton)
        
        self.setLayout(layout)
        self.show()
        
    def handleButton(self, s):
        #self.label.setText('Button Clicked!')     
        self.qindex = (self.qindex+1) % len(self.questions)
        self.label.setText(self.questions[self.qindex])
        print('Button clicked %s' % s)
        
    def changeTitle(self, state):
      
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')
            
        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())