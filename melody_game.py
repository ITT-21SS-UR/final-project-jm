import pygame
import pygame_menu
from synthesizer import Player, Synthesizer, Waveform
import pyaudio
import wave
from pyo import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import math
import random
from enum import Enum

from DIPPID import SensorUDP, SensorSerial, SensorWiimote

SENSOR_PORT = 5700

# state of the game
class GameState(Enum):
    INTRO = 1
    START = 2
    DONE = 3

class Game(QMainWindow):
    sensor = ()
    timer = ()
    song = []
    points = 0
    song_list = ["seven_nation_army", "amours_toujours", "satisfaction"]
    played_songs = []
    played_tones = []
    current_song = ""
    round = 0
    c_chord = ["C4", "E4", "G4"]
    seven_nation_army = [("E4", 0.7), ("E4", 0.3),("G4", 0.3),("E4", 0.3), ("D4", 0.3),("C4", 0.7),
                            ("B3", 0.7), ("E4", 0.7), ("E4", 0.3),("G4", 0.3), ("E4", 0.3),("D4", 0.3),
                                ("C4", 0.3), ("D4", 0.3), ("C4", 0.3), ("B3", 0.7)]
    seven_nation_army_tones = ["B3", "C4", "D4", "E4", "G4"]

    alle_meine_entchen = [("C4", 0.5), ("D4", 0.5), ("E4", 0.5),("F4", 0.5),("G4", 1.0),("G4", 1.0),
                            ("A4", 0.4),("A4", 0.4),("A4", 0.4),("A4", 0.4),("G4", 0.5),
                                ("A4", 0.4),("A4", 0.4),("A4", 0.4),("A4", 0.4),("G4", 0.5),
                                    ("F4", 0.3),("F4", 0.3),("F4", 0.3),("F4", 0.3),("E4", 0.5),
                                        ("E4", 0.5),("D4", 0.3),("D4", 0.3),("D4", 0.3),("D4", 0.3),
                                            ("C4", 0.8)]
    alle_meine_entchen_tones = ["C4", "D4", "E4", "F4", "G4", "A4"]

    amours_toujours = [("E4", 0.4),("E4", 0.4),("C5", 0.4),("B4", 0.7),("B4", 0.4),("B4", 0.4),("C5", 0.4),
                        ("A4", 0.7),("A4", 0.4),("A4", 0.4),("G4", 0.4),("A4", 0.4),("A4", 0.4),("A4", 0.4),
                            ("G4", 0.4),("A4", 0.4),("G4", 0.4),("A4", 0.4),("G4", 0.4),("E4", 0.7),]
    amours_toujours_tones = ["E4", "G4", "A4", "B4", "C5"]

    satisfaction= [("D4", 0.7),("D4", 0.7),("D4", 0.4),("E4", 0.4),("F4", 0.7),("F4", 0.4),("F4", 0.4),
                    ("E4", 0.4),("E4", 0.4),("D4", 0.7),("D4", 0.7),("D4", 0.4),("E4", 0.4),("F4", 0.7),
                    ("F4", 0.4),("F4", 0.4), ("E4", 0.4),("E4", 0.4),("D4", 0.7),("D4", 0.7)]
    satisfaction_tones = ["D4", "E4", "F4"]

    

    def __init__(self):
        super().__init__()
        self.setGeometry(700,100,800,600)
        self.player = Player()
        self.synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
        self.game_state = GameState.INTRO
        self.timer = QTimer(self)
        self.current_song_tones = []
        self.default = "off"
        self.init_sensor()
        self.init_timer_game_loop()
        self.init_game()
        self.initUIComponents()
    
    def initUIComponents(self):
        self.title_label = QLabel(self)
        self.title_label.setFont(QFont("Helvetica", 20))
        self.title_label.setText("Welcome to our Melody Game!")
        self.title_label.setMinimumSize(400,75)
        self.title_label.move(220,0)

        self.switch_mode_label = QLabel(self)
        self.switch_mode_label.setText("Press the Button below to practice or to compete!")
        self.switch_mode_label.setMinimumSize(400,50)
        self.switch_mode_label.move(220,50)
        
        self.game_info = QLabel(self)
        self.game_info.setText("Rotate your dippid device to play different tones \nand follow the melody")
        self.game_info.setMinimumSize(400,50)
        self.game_info.move(220,50)
        self.game_info.setVisible(False)
        
        self.help_button = QPushButton(self)
        self.help_button.setText("FAQ")
        self.help_button.setMinimumSize(10,30)
        self.help_button.setStyleSheet("background-color: lightgreen")
        self.help_button.move(700,10)
        self.help_button.clicked.connect(self.help_button_clicked)

        self.play_melody = QPushButton(self)
        self.play_melody.setText("Play Melody")
        self.play_melody.setMinimumSize(150,100)
        self.play_melody.setStyleSheet("background-color: green")
        self.play_melody.move(50,150)
        self.play_melody.clicked.connect(self.play_current_melody)
        self.play_melody.setVisible(False)

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

    def paintEvent(self,event):
        painter = QPainter(self)
        #painter.begin(self)
        painter.setPen(QPen(Qt.blue))
        painter.translate(400, 300)
        for i in range(6):
            painter.drawLine(0, 0, 150, 0)
            painter.rotate(60)
        painter.end()


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
        #self.handle_dippid_input()
    
    def compete_button_clicked(self):
        self.practice_button.setVisible(False)
        self.compete_button.setVisible(False)
        self.switch_mode_label.setVisible(False)
        self.game_info.setVisible(True)
        self.play_melody.setVisible(True)
        print("compete button click!")
        self.start_the_game()

    def init_game(self):
        #pygame.init()
        #surface = pygame.display.set_mode((600, 600))
        #menu = pygame_menu.Menu('Welcome', 400, 300,
                        #theme=pygame_menu.themes.THEME_GREEN)

        #menu.add.text_input('Name :', default='')
        #menu.add.button('Play', self.start_the_game)
        #menu.add.button('Quit', pygame_menu.events.EXIT)
        #menu.mainloop(surface)
        pass

    def init_sensor(self):
        BUTTON_START = 'button_1'
        self.sensor = SensorUDP(SENSOR_PORT)
        self.sensor.register_callback(BUTTON_START, self.button_start_pressed)

    def button_start_pressed(self, data):
        print("button 1 pressed")

    # game loop
    # found on https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTimer.html
    def init_timer_game_loop(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(30)

    def game_loop(self):
        if self.game_state == GameState.START:
            if self.sensor.has_capability('accelerometer'):
                value_sensor = self.sensor.get_value('accelerometer')
            else:
                return
            if self.sensor.has_capability('gravity'):
                value_gravitiy_sensor = self.sensor.get_value('gravity')
            else:
                return
            value_y = value_sensor['y']
            value_z = value_sensor['z']
            value_x = value_sensor['x']
            value_grav_y = value_gravitiy_sensor['y']
            self.play_tone(value_x, value_y, value_z)
            self.update()
        
    """ 
    old moves

        def play_tone(self, x,y,z):
        self.current_song_tones = self.seven_nation_army_tones
        tone = ''
        if x > 0 and z < 0.5 and (0.2 > y > -0.2) :
            tone = self.current_song_tones[0]
        elif x < 0  and z < 0.5 and (0.2 > y > -0.2):
            tone = self.current_song_tones[1]
        elif y > 0.7 and (-0.2 < x < 0.2):
            tone = self.current_song_tones[2]
        elif y < -0.7 and (-0.2 < x < 0.2):
            tone = self.current_song_tones[3]
        elif x > 0 and z < 0.5 and ((0.7 > y > 0.2) or (-0.2 > y > -0.7)):
            tone = self.current_song_tones[4]
        elif x < 0  and z < 0.5 and ((0.7 > y > 0.2) or (-0.2 > y > -0.7)):
            tone = self.current_song_tones[5]
        if tone is not '':
            self.synth_play_tone(tone)
        print(tone) """
    
    def play_current_melody(self):
        song = getattr(self,self.current_song)
        self.play_song(song)


    def play_tone(self, x,y,z):
        #self.current_song_tones = self.seven_nation_army_tones
        tone = ''
        if (0.33 > x > -0.33) and (0.76 < y < 1) :
            tone = ''
            self.default = "on"
        elif (0.33 < x < 1) and (0.76 > y > 0):
            try: 
                tone = self.current_tones[0]
            except IndexError:
                tone = ''
            self.default = "off"
        elif (0.33 < x < 1) and (-0.76 < y < 0):
            try: 
                tone = self.current_tones[1]
            except IndexError:
                tone = ''
            self.default = "off"
        elif (0.33 > x > -0.33) and (-0.76 > y < -1):
            try: 
                tone = self.current_tones[2]
            except IndexError:
                tone = ''
            self.default = "off"
        elif (-0.33 > x > -1) and (-0-76 < y < 0):
            try: 
                tone = self.current_tones[3]
            except IndexError:
                tone = ''
            self.default = "off"
        elif (-1 < x < -0.33) and (0 < y < 0.76):
            try: 
                tone = self.current_tones[4]
            except IndexError:
                tone = ''            
            self.default = "off"
        if tone != '':
            self.synth_play_tone(tone)
        self.played_tones += tone
    
    def start_the_game(self):
        self.player.open_stream()
        self.game_state = GameState.START
        self.new_round()
        #self.paintEvent()

    
    def play_song(self,song):
        for i in range(len(song)):
            self.synth_play_tone(song[i][0],song[i][1])
    
    def calc_points(self):
        song = getattr(self,self.current_song)
        for i in range(len(song)):
            if song[i][0] == self.played_tones[i]:
                self.points += 1


    
    def synth_play_tone(self,tone,length=0.5):
        self.player.play_wave(self.synthesizer.generate_constant_wave(tone, length))

    def new_round(self):
        if self.round != 0:
            self.played_songs += self.current_song
            self.calc_points()
        self.select_new_song()
        self.round += 1

    def select_new_song(self):
        self.current_song = random.choice(self.song_list)
        self.current_tones = getattr(self,self.current_song + "_tones")
        if (self.current_song in self.played_songs):
            self.select_new_song()

    def game_done(self):
        pass
    
    def new_game(self):
        self.points = 0
        self.current_song = ""
        self.current_tones = []
        self.played_songs = []

   

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Game()
    win.show()
    app.exec()
