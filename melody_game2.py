import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from DIPPID import SensorUDP

PORT = 5700
sensor = SensorUDP(PORT)

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,100,800,600)
        self.initUIComponents()

    def initUIComponents(self):
        self.title_label = QLabel(self)
        self.title_label.setFont(QFont("Helvetica", 20))
        self.title_label.setText("Welcome to our Melody Game!")
        self.title_label.setMinimumSize(400,75)
        self.title_label.move(200,0)

        self.switch_mode_label = QLabel(self)
        self.switch_mode_label.setText("Press the Button below to practice or to compete!")
        self.switch_mode_label.setMinimumSize(400,50)
        self.switch_mode_label.move(220,50)

        self.help_button = QPushButton(self)
        self.help_button.setText("FAQ")
        self.help_button.setMinimumSize(10,30)
        self.help_button.setStyleSheet("background-color: lightgreen")
        self.help_button.move(700,10)
        self.help_button.clicked.connect(self.help_button_clicked)

        self.practice_button = QPushButton(self)
        self.practice_button.setText("Practice")
        self.practice_button.setMinimumSize(150,100)
        self.practice_button.setStyleSheet("background-color: blue")
        self.practice_button.move(50,150)
        self.practice_button.clicked.connect(self.practice_button_clicked)

        self.compete_button = QPushButton(self)
        self.compete_button.setText("Compete")
        self.compete_button.setMinimumSize(150,100)
        self.compete_button.setStyleSheet("background-color: red")
        self.compete_button.move(600,150)
        self.compete_button.clicked.connect(self.compete_button_clicked)

    def help_button_clicked(self):
        faq_box = QDialog(self)
        faq_box.move(0,0)
        faq_box.setMinimumSize(600,300)
        text1 = QLabel("with your DIPPID device activated you can play five tones", faq_box)
        text2 = QLabel("The following grid shows tone values with 1 very deep and 5 very high", faq_box)
        text1.move(10,10)
        text2.move(10,30)
        table = QTableWidget(faq_box)
        table.setRowCount(5)
        table.setColumnCount(1)
        table.setItem(0,0, QTableWidgetItem("left"))
        table.setItem(1,0, QTableWidgetItem("right"))
        table.setItem(2,0, QTableWidgetItem("up"))
        table.setItem(3,0, QTableWidgetItem("down"))
        table.setItem(4,0, QTableWidgetItem("steady"))
        table.move(10,80)
        faq_box.open()

    def practice_button_clicked(self):
          self.practice_button.setEnabled(False)
          self.compete_button.setEnabled(True)
          print("practice button click!")
          self.handle_dippid_input()

    def handle_dippid_input(self):
            print("hi")
#            self.sensor_data = sensor.get_value('accelerometer')
 #           print(self.sensor_data)

    def compete_button_clicked(self):
         self.practice_button.setEnabled(True)
         self.compete_button.setEnabled(False)
         print("compete button click!")


def main():
    app = QApplication(sys.argv)
    win = GameWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()