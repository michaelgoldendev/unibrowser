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
import traceback, sys

from questionanswerwidget import AnswerPanelWidget
from questionanswerwidget import InputMethod

from datetime import datetime

RELEASE_VERSION = True

from streamingacquisition import UnicornStreamingAcquisition
startdatetime = datetime.now()

from AcquistionFunctions import process_EEG


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
            
"""       
class AcquisitionThread(QRunnable):
    def run(self):
        acquisitionmodule.acquiredata()
"""

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
        self.spinboxyes.setValue(3.0)
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
        self.spinboxno.setValue(5.0)
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
        self.spinboxacquistiontime.setValue(15.0)
        self.spinboxacquistiontime.setMinimum(0.5)
        self.spinboxacquistiontime.setMaximum(100000000.0)
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
        self.streamingacquisition = UnicornStreamingAcquisition()
        
        worker = Worker(self.streamingacquisition.startAcquisition)
        worker.signals.result.connect(self.saveResult)
        worker.signals.error.connect(self.cancelBCI)
        worker.signals.finished.connect(self.stopBCI)
        #worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
        
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
        
      
        worker = Worker(self.streamingacquisition.getNseconds, self.spinboxacquistiontime.value())
        worker.signals.result.connect(self.saveResult)
        worker.signals.error.connect(self.cancelBCI)
        worker.signals.finished.connect(self.stopBCI)
        self.threadpool.start(worker)
        """
        
        
        #thread = AcquisitionThread()
        #thread.finished.connect(self.stopBCI)
        #thread.start()
        #
        #runnable = AcquisitionThread()
        #QThreadPool.globalInstance().start(runnable)
        
        QTimer.singleShot(self.bcianimationtimeoutmillis, self.stopBCI)
        """
    def saveResult(self, result):
        logratio,scoreyes,scoreno = process_EEG(result, self.spinboxyes.value(), self.spinboxno.value())
        timestampStr = startdatetime.strftime("%d-%b-%Y_%Hh%Mm%Ss%f")
        datafolder = 'data%s/' % timestampStr
        if not os.path.exists(datafolder):
            os.makedirs(datafolder)
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y.%Hh%Mm%Ss%f")
        focus = "yes"
        if self.noradiobuttion.isChecked():
            focus = "no"
        resultFileName = "%s/data_focus-%s_yes%0.1fHz_no%0.1fHz_%0.1fseconds_%s.csv" % (datafolder,focus, self.spinboxyes.value(), self.spinboxno.value(), self.spinboxacquistiontime.value(), timestampStr)
        np.savetxt(resultFileName, result, delimiter=",")
        
        fout = open("%s/results.csv" % datafolder, "a")
        fout.write("%s,%0.1f,%0.1f,%0.1f,%s,%0.3f,%0.3f,%0.3f\n" % (focus, self.spinboxyes.value(), self.spinboxno.value(), self.spinboxacquistiontime.value(), timestampStr, logratio,scoreyes,scoreno))
        fout.close()
        
        """
        fout = open(, "w")
        fout.write(str(result))
        fout.close()
        """
        
    def cancelBCI(self):
        self.answerpanel.stopBCIanimation()
        self.spinboxyes.setEnabled(True)
        self.spinboxno.setEnabled(True)
        self.spinboxacquistiontime.setEnabled(True)
        self.startbutton.setEnabled(True)
        self.cancelbutton.setEnabled(False)
        self.streamingacquisition.cancelAcquisition()
        
    
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