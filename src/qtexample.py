from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

@pyqtSlot()
def on_click():
    print('PyQt5 button click')

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
#layout.addWidget(QPushButton('Top'))
#layout.addWidget(QPushButton('Bottom'))

font = QFont()
font.setPointSize(18)
font.setBold(True)
font.setWeight(75)

label = QLabel('Is your character real?')
label.setFont(font)
label.setAlignment(Qt.AlignCenter)
layout.addWidget(label)

yesbutton = QPushButton('Yes', window)
yesbutton.clicked.connect(on_click)
yesbutton.setToolTip('Yes')
layout.addWidget(yesbutton)

maybebutton = QPushButton('Maybe', window)
maybebutton.clicked.connect(on_click)
maybebutton.setToolTip('Maybe')
layout.addWidget(maybebutton)

nobutton = QPushButton('No', window)
nobutton.clicked.connect(on_click)
nobutton.setToolTip('No')
layout.addWidget(nobutton)

window.setLayout(layout)
#window.showFullScreen()
window.show()
app.exec_()