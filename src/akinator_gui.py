from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

import numpy as np
import sys
import akinator_model

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.model = akinator_model.Akinator()
        akinator_model.initialise(self.model)
        self.qkey = self.model.nextquestion_entropy()   
        self.model.usedquestions.append(self.qkey)
        self.label = QLabel(self.model.questions[self.qkey])
        
        self.initUI()
        
        self.chartwindow = QWidget()
        self.chart = QChart()
        self.initchartUI()
        
        
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
        yesbutton.clicked.connect(lambda: self.handleButton(akinator_model.YES))
        yesbutton.setToolTip('Yes')
        layout.addWidget(yesbutton)
        
        maybebutton = QPushButton('Maybe', self)
        maybebutton.clicked.connect(lambda: self.handleButton(akinator_model.MAYBE))
        maybebutton.setToolTip('Maybe')
        layout.addWidget(maybebutton)
        
        nobutton = QPushButton('No', self)
        nobutton.clicked.connect(lambda: self.handleButton(akinator_model.NO))
        nobutton.setToolTip('No')
        layout.addWidget(nobutton)
        
        self.setLayout(layout)
        self.show()
        
    def setchart(self, label="", values=[], categories=[]):
        set0 = QBarSet(label)
        for v in values:
            set0.append(v)
        set0.setColor(QColor("#ff6b6b"))
        
        series = QBarSeries()
        series.append(set0)
        series.setLabelsAngle(0.0)
        series.setLabelsPrecision(3)
        series.setLabelsVisible(True)
        
        font = QFont()
        font.setPointSize(10)
        set0.setLabelFont(font)
        set0.setLabelColor(QColor("#000000"))
        print(dir(set0))
        
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
        
        axis = QBarCategoryAxis()
        axis.append(categories)
        axis.setLabelsAngle(-90)
     
        font = QFont()
        font.setPointSize(12)        
        axis.setLabelsFont(font)
        
        
       # axis.addItem(QTextItem(text='Hello', anchor=(0.5,0.5)))
        
        for ser in self.chart.series():
            self.chart.removeSeries(ser)
        self.chart.addSeries(series)
        self.chart.setAxisX(axis, series)
        
    def initchartUI(self):
        self.chart.setTitle("Character probabilities (Top 10)")
        font = QFont()
        font.setPointSize(12)   
        self.chart.setTitleFont(font)
        
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.createDefaultAxes()
        
        self.chart.legend().setVisible(False)
        """
        self.chart.legend().setAlignment(Qt.AlignBottom)        
        font = QFont()
        font.setPointSize(12)        
        self.chart.legend().setFont(font)
        """
        
        self.updatechart()
        
        chartView = QChartView(self.chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        self.chartwindow.resize(800, 600)
        
        layout = QVBoxLayout()
        layout.addWidget(chartView)
        self.chartwindow.setLayout(layout)
        self.chartwindow.show()

        
        
    def handleButton(self, answer):
        self.model.update(self.qkey, answer)
        self.qkey = self.model.nextquestion_entropy()
        if self.qkey >= 0:
            self.model.usedquestions.append(self.qkey)
            self.label.setText(self.model.questions[self.qkey])       
            self.updatechart()
        else:
            exit()
            
    def updatechart(self):
        self.model.stateprobs = self.model.stateprobs / np.sum(self.model.stateprobs)
        sortedcharacters = [(p, character) for (p, character)  in zip(self.model.stateprobs,self.model.characters)]
        sortedcharacters.sort(reverse=True)
        vs = []
        cats = []
        for (p, character) in sortedcharacters[0:10]:
            vs.append(p)
            cats.append(character)
        self.setchart("Characters", vs, cats)
            
        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = MainWindow()    
    sys.exit(app.exec_())