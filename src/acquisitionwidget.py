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

from questionanswerwidget import AnswerPanelWidget
from questionanswerwidget import InputMethod

import acquisitionmodule

RELEASE_VERSION = True
       
class AcquisitionThread(QRunnable):
    def run(self):
        acquisitionmodule.acquiredata()

class AcquisitionWidget(QWidget):
    
    def __init__(self):
        super().__init__()

        self.inputmethod =  InputMethod.SSVEP # InputMethod.MOUSE, InputMethod.SSVEP
        self.answerpanel = AnswerPanelWidget(self.inputmethod)
        
        self.setWindowTitle('Unibrowser')
        self.setMouseTracking(False)
        
        self.vboxlayout  = QVBoxLayout()        
        self.vboxlayout.setAlignment(Qt.AlignCenter)
        
        
        self.warningtimesecs = 3
        self.questiontimeoutmillis = 15000.0 if RELEASE_VERSION else 3000.0
        self.questiontimeoutmillis += self.warningtimesecs*1000.0
        self.timerintervalmillis = 1000.0
        self.questionno = 0
        self.questionframe = 0
        self.questiontimer = QTimer()        
        
        self.bcianimationtimeoutmillis = 6000.0 if RELEASE_VERSION else 1000.0
        self.choicetimeoutmillis = 4000.0 if RELEASE_VERSION else 2000.0
        
        self.yesspinnerframe = QFrame()
        self.yespinnerlayout  = QHBoxLayout() 
        self.yesspinnerframe.setLayout(self.yespinnerlayout)
        self.labelyes = QLabel("Yes frequency (Hz)")
        self.labelyes.setFixedWidth(150)
        self.yespinnerlayout.addWidget(self.labelyes)        
        self.spinboxyes = QDoubleSpinBox()
        self.spinboxyes.setMinimum(0.1)
        self.spinboxyes.setMaximum(100.0)
        self.spinboxyes.setSingleStep(0.1)
        self.spinboxyes.setValue(5.0)
        self.spinboxyes.setDecimals(1)
        self.yespinnerlayout.addWidget(self.spinboxyes) 
        self.yespinnerlayout.addStretch(1)
        self.vboxlayout.addWidget(self.yesspinnerframe)
        
        
        self.nospinnerframe = QFrame()
        self.nopinnerlayout  = QHBoxLayout() 
        self.nospinnerframe.setLayout(self.nopinnerlayout)
        self.labelno = QLabel("No frequency (Hz)")
        self.labelno.setFixedWidth(150)
        self.nopinnerlayout.addWidget(self.labelno)        
        self.spinboxno = QDoubleSpinBox()
        self.spinboxno.setMinimum(0.1)
        self.spinboxno.setMaximum(100.0)
        self.spinboxno.setSingleStep(0.1)
        self.spinboxno.setDecimals(1)
        self.spinboxno.setValue(7.0)
        self.nopinnerlayout.addWidget(self.spinboxno)    
        self.nopinnerlayout.addStretch(1)
        self.vboxlayout.addWidget(self.nospinnerframe)
                                  
        self.acquistiontimespinnerframe = QFrame()
        self.acquistiontimepinnerlayout  = QHBoxLayout() 
        self.acquistiontimespinnerframe.setLayout(self.acquistiontimepinnerlayout)
        self.labelacquistiontime = QLabel("Acquistion time (seconds)")
        self.labelacquistiontime.setFixedWidth(150)
        self.acquistiontimepinnerlayout.addWidget(self.labelacquistiontime)        
        self.spinboxacquistiontime = QDoubleSpinBox()
        self.spinboxacquistiontime.setSingleStep(0.5)
        self.spinboxacquistiontime.setValue(8.0)
        self.spinboxacquistiontime.setMinimum(0.5)
        self.spinboxacquistiontime.setMaximum(600.0)
        self.spinboxacquistiontime.setDecimals(1)
        self.acquistiontimepinnerlayout.addWidget(self.spinboxacquistiontime)    
        self.acquistiontimepinnerlayout.addStretch(1)
        self.vboxlayout.addWidget(self.acquistiontimespinnerframe)
        
        self.focuslabel = QLabel("I am focusing on:")
        self.vboxlayout.addWidget(self.focuslabel)
        
        self.yesradiobuttion = QRadioButton("Yes")
        self.yesradiobuttion.setChecked(True)
        #self.yesradiobuttion.toggled.connect(lambda:self.btnstate(self.b1))
        self.vboxlayout.addWidget(self.yesradiobuttion)
        
        self.noradiobuttion = QRadioButton("No")
        self.noradiobuttion.setChecked(False)
        #self.yesradiobuttion.toggled.connect(lambda:self.btnstate(self.b1))
        self.vboxlayout.addWidget(self.noradiobuttion)
          
        self.startbutton = QPushButton('Start acquisition')
        self.startbutton.clicked.connect(self.startBCI)
        self.vboxlayout.addWidget(self.startbutton)
        
        self.cancelbutton = QPushButton('Cancel acquisition')
        self.cancelbutton.clicked.connect(self.cancelBCI)
        self.cancelbutton.setEnabled(False)
        self.vboxlayout.addWidget(self.cancelbutton)
        
        self.vboxlayout.addWidget(self.answerpanel)    
        
        self.setLayout(self.vboxlayout)
        
        self.threadpool = QThreadPool()
        
        self.show()
            
    def startBCI(self):
        self.answerpanel.setFrequencies([self.spinboxyes.value(), self.spinboxno.value()])
        self.answerpanel.startBCIanimation()
        self.spinboxyes.setEnabled(False)
        self.spinboxno.setEnabled(False)
        self.spinboxacquistiontime.setEnabled(False)
        self.bcianimationtimeoutmillis = self.spinboxacquistiontime.value()*1000.0
        self.startbutton.setEnabled(False)
        self.cancelbutton.setEnabled(True)
        
        #self.threadpool.start(AcquisitionThread())
        #thread = AcquisitionThread()
        #thread.finished.connect(self.stopBCI)
        #thread.start()
        #
        #runnable = AcquisitionThread()
        #QThreadPool.globalInstance().start(runnable)
        
        #QTimer.singleShot(self.bcianimationtimeoutmillis, self.stopBCI)
        
    def cancelBCI(self):
        self.answerpanel.stopBCIanimation()
        self.spinboxyes.setEnabled(True)
        self.spinboxno.setEnabled(True)
        self.spinboxacquistiontime.setEnabled(True)
        self.startbutton.setEnabled(True)
        self.cancelbutton.setEnabled(False)
        
    
    def stopBCI(self):        
        self.answerpanel.stopBCIanimation()
        self.spinboxyes.setEnabled(True)
        self.spinboxno.setEnabled(True)
        self.spinboxacquistiontime.setEnabled(True)
        self.startbutton.setEnabled(True)
        self.cancelbutton.setEnabled(False)

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = AcquisitionWidget()
    sys.exit(app.exec_())