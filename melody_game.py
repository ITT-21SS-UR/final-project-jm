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
    round_points = 0
    song_list = ["seven_nation_army", "amours_toujours", "i_cant_get_no_satisfaction"]
    played_songs = []
    played_tones = []
    played_tone = ""
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

    i_cant_get_no_satisfaction= [("D4", 0.7),("D4", 0.7),("D4", 0.4),("E4", 0.4),("F4", 0.7),("F4", 0.4),("F4", 0.4),
                    ("E4", 0.4),("E4", 0.4),("D4", 0.7),("D4", 0.7),("D4", 0.4),("D4", 0.4),("E4", 0.4),("F4", 0.7),
                    ("F4", 0.4),("F4", 0.4), ("E4", 0.4),("E4", 0.4),("D4", 0.7),("D4", 0.7),("D4", 0.7)]
    i_cant_get_no_satisfaction_tones = ["D4", "E4", "F4"]

    

    def __init__(self):
        super().__init__()
        self.setGeometry(700,100,800,600)
        self.player = Player()
        self.synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
        self.game_state = GameState.INTRO
        self.timer = QTimer(self)
        self.current_tones = []
        self.last_played_tone = ""
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
        
        self.song_name = QLabel(self)
        self.song_name.setText("Song name: "+ self.current_song)
        self.song_name.setMinimumSize(400,50)
        self.song_name.move(220,80)
        self.song_name.setVisible(False)
        
        self.points_info = QLabel(self)
        self.points_info.setText("Points: " + str(self.points))
        self.points_info.setMinimumSize(400,50)
        self.points_info.move(220,110)
        self.points_info.setVisible(False)
        
        """ self.help_button = QPushButton(self)
        self.help_button.setText("FAQ")
        self.help_button.setMinimumSize(10,30)
        self.help_button.setStyleSheet("background-color: lightgreen")
        self.help_button.move(700,10)
        self.help_button.clicked.connect(self.help_button_clicked) """

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
        self.tone_rect_0 = QRect(375,200,75,75)
        self.tone_rect_1 = QRect(250,300,75,75)
        self.tone_rect_2 = QRect(250,400,75,75)
        self.tone_rect_3 = QRect(375,500,75,75)
        self.tone_rect_4 = QRect(500,400,75,75)
        self.tone_rect_5 = QRect(500,300,75,75)
        pt = QPainter()
        pt.begin(self)
        pt.setPen(QPen(Qt.black))
        pt.drawEllipse(self.tone_rect_0)
        pt.drawEllipse(self.tone_rect_1)
        pt.drawEllipse(self.tone_rect_2)
        pt.drawEllipse(self.tone_rect_3)
        pt.drawEllipse(self.tone_rect_4)
        pt.drawEllipse(self.tone_rect_5)

        if self.played_tone != "":
            tone_rect = "tone_rect_" + self.played_tone
            played_tone_rect = getattr(self,tone_rect)
            brush = QBrush(Qt.yellow)
            pt.setBrush(brush)
            pt.drawEllipse(played_tone_rect)

        if self.game_state == GameState.START:
            for i in range(5):
                tone_rect = "tone_rect_" + str(i +1)
                try:
                    pt.drawText(getattr(self, tone_rect), Qt.AlignCenter,self.current_tones[i])
                except IndexError:
                    pass


        pt.end()

        """ painter = QPainter(self)
        #painter.begin(self)
        painter.setPen(QPen(Qt.blue))
        painter.translate(400, 300)
        for i in range(6):
            painter.drawLine(0, 0, 150, 0)
            painter.rotate(60)
        painter.end() """


    def round_done(self):
        self.round_ended_box = QDialog(self)
        self.round_ended_box.move(0,0)
        self.round_ended_box.setMinimumSize(400,200)
        text1 = QLabel("Round no " + str(self.round) + " done. You made " + str(self.round_points) + " Points. \n"
                            "Press the Button below to start a new round", self.round_ended_box)
        text1.move(10,10)
        self.new_round_button = QPushButton(self.round_ended_box)
        self.new_round_button.setText("New Round")
        self.new_round_button.setMinimumSize(100,60)
        self.new_round_button.setStyleSheet("background-color: lightgreen")
        self.new_round_button.move(150,100)
        self.new_round_button.clicked.connect(self.new_round) 
        self.round_ended_box.open()
    
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
        self.song_name.setVisible(True)
        self.points_info.setVisible(True)
        print("compete button click!")
        self.start_the_game()

    def init_game(self):
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
            if len(self.played_tones) < len(self.current_song):
                self.play_tone(value_x, value_y, value_z)
            else:
                self.show_round_result()
            self.update()
        
    def show_round_result(self):
        self.points_info.setText("Points: " + str(self.points))
        self.round_done()

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
        tone = ''
        self.played_tone = ""
        if (0.33 > x > -0.33) and (0.76 < y < 1) :
            tone = ''
            self.played_tone = "0"
        elif (0.33 < x < 1) and (0.76 > y > 0):
            try: 
                tone = self.current_tones[0]
            except IndexError:
                tone = ''
            self.played_tone = "1"
        elif (0.33 < x < 1) and (-0.76 < y < 0):
            try: 
                tone = self.current_tones[1]
            except IndexError:
                tone = ''
            self.played_tone = "2"
        elif (0.33 > x > -0.33) and (-0.76 > y < -1):
            try: 
                tone = self.current_tones[2]
            except IndexError:
                tone = ''
            self.played_tone="3"
        elif (-0.33 > x > -1) and (-0-76 < y < 0):
            try: 
                tone = self.current_tones[3]
            except IndexError:
                tone = ''
            self.played_tone = "4"
        elif (-1 < x < -0.33) and (0 < y < 0.76):
            try: 
                tone = self.current_tones[4]
            except IndexError:
                tone = ''            
            self.played_tone = "5"
        if (tone != '') and (self.last_played_tone != self.played_tone):
            self.synth_play_tone(tone)
            self.played_tones += tone
        self.last_played_tone = self.played_tone
    
    def start_the_game(self):
        self.player.open_stream()
        self.game_state = GameState.START
        self.new_round()

    
    def play_song(self,song):
        for i in range(len(song)):
            self.synth_play_tone(song[i][0],song[i][1])
            self.played_tone = song[i][0]
    
    def calc_points(self):
        song = getattr(self,self.current_song)
        for i in range(len(song)):
            if song[i][0] == self.played_tones[i]:
                self.points += 1


    
    def synth_play_tone(self,tone,length=0.5):
        self.player.play_wave(self.synthesizer.generate_constant_wave(tone, length))

    def new_round(self):
        print(self.round)
        print("new round")
        if self.round != 0:
            self.played_songs += self.current_song
            self.calc_points()
            self.round_ended_box.close()
        self.select_new_song()
        song_name = self.current_song.replace("_", " ")
        song_name = song_name.capitalize()
        self.song_name.setText("Song name: " + song_name)
        self.played_tones = []
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
