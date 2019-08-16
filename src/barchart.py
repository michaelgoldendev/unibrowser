# pip3 install PyQtChart
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def set(chart, label="Jane", values=[0.1,0.2,0.3,0.4,0.5,0.6], categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun"]):
    set0 = QBarSet(label)
    for v in values:
        set0.append(v)
    
    series = QBarSeries()
    series.append(set0)
    
    for axis in chart.axes():
        chart.removeAxis(axis)
    
    axis = QBarCategoryAxis()
    axis.append(categories)
    axis.setLabelsAngle(-60)
    
    for ser in chart.series():
        chart.removeSeries(ser)
    chart.addSeries(series)
    chart.setAxisX(axis, series)

a = QApplication([])



chart = QChart()
chart.setTitle("Simple percentbarchart example")
chart.setAnimationOptions(QChart.SeriesAnimations)



chart.createDefaultAxes()
set(chart)

chart.legend().setVisible(True)
chart.legend().setAlignment(Qt.AlignBottom)

chartView = QChartView(chart)
chartView.setRenderHint(QPainter.Antialiasing)

window = QMainWindow()
window.setCentralWidget(chartView)
window.resize(420, 300)
window.show()


def num():
    set(chart)

timer = QTimer()
timer.timeout.connect(num)
timer.start(2000)

a.exec_()