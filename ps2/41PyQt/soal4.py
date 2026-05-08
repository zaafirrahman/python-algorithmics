from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from random import randint
 
app = QApplication([])
 
# main window:
my_win = QWidget()
my_win.setWindowTitle('Drawing')
my_win.move(100, 100)
my_win.resize(400, 200)


#window widgets: button dan label
button = QPushButton('Try your luck')
text = QLabel('Klik untuk berpartisipasi')
number1 = QLabel('?')
number2 = QLabel('?')


#widget layout
line = QVBoxLayout()
line.addWidget(text, alignment = Qt.AlignCenter)
line.addWidget(number1, alignment = Qt.AlignCenter)
line.addWidget(number2, alignment = Qt.AlignCenter)
line.addWidget(button, alignment = Qt.AlignCenter)
my_win.setLayout(line)
 
#fungsi yang menghasilkan dan menampilkan angka
def start_lottery():
    n1 = randint(0, 9)
    n2 = randint(0, 9)
    number1.setText(str(n1))
    number2.setText(str(n2))
    if n1 == n2:
        text.setText('Anda menang! Main lagi')
    else:
        text.setText('Anda kalah! Main lagi')
 
#pemrosesan klik tombol
button.clicked.connect(start_lottery)


my_win.show()
app.exec_()
