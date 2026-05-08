from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from random import randint
 
app = QApplication([])
 
# main window:
my_win = QWidget()
my_win.setWindowTitle('Winner Identifier')
my_win.move(100, 100)
my_win.resize(400, 200)


#window widgets: button dan label
button = QPushButton('Generate')
text = QLabel('Klik untuk mengetahui pemenang')
winner = QLabel('?')


#widget layout
line = QVBoxLayout()
line.addWidget(text, alignment = Qt.AlignCenter)
line.addWidget(winner, alignment = Qt.AlignCenter)
line.addWidget(button, alignment = Qt.AlignCenter)
my_win.setLayout(line)
 
#fungsi yang menghasilkan dan menampilkan angka
def show_winner():
    number = randint(0, 99)
    winner.setText(str(number))
    text.setText('Pemenang:')
 
#pemrosesan klik tombol
button.clicked.connect(show_winner)


my_win.show()
app.exec_()
