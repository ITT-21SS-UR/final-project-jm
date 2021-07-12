import pygame
import pygame_menu
from synthesizer import Player, Synthesizer, Waveform
import pyaudio
import wave
from pyo import *

from PyQt5 import QtGui, QtCore, QtWidgets

import sys
import math
import random
from enum import Enum

from DIPPID import SensorUDP, SensorSerial, SensorWiimote
from DIPPID_pyqtnode import BufferNode, DIPPIDNode

SENSOR_PORT = 5700

# state of the game
class GameState(Enum):
    INTRO = 1
    START = 2
    DONE = 3

class Songs():

    def __init__(self):
        super().__init__()
    
        

class Game(QtWidgets.QWidget):

    
    sensor = ()
    timer = ()
    c_chord = ["C4", "E4", "G4"]
    seven_nation_army = [("E4", 1.0), ("E4", 0.5),("G4", 0.5),("E4", 0.5), ("D4", 0.5),("C4", 1.0),
                            ("B3", 1.0), ("E4", 1.0), ("E4", 0.5),("G4", 0.5), ("E4", 0.5),("D4", 0.5),
                                ("C4", 0.5), ("D4", 0.5), ("C4", 0.5), ("B3", 1.0)]
    seven_nation_army_tones = ["B3", "C4", "D4","E4","G4"]
    alle_meine_entchen = [("C4", 1.0), ("D4", 1.0), ("E4", 1.0),]
    

    def __init__(self):
        super().__init__()
        self.player = Player()
        self.synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
        self.game_state = GameState.INTRO
        self.timer = QtCore.QTimer(self)
        self.init_sensor()
        self.init_timer_game_loop()
        self.init_game()

    def init_game(self):
        pygame.init()
        surface = pygame.display.set_mode((600, 600))
        menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_GREEN)

        menu.add.text_input('Name :', default='')
        menu.add.button('Play', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(surface)

    def init_sensor(self):
        BUTTON_START = 'button_1'
        self.sensor = SensorUDP(SENSOR_PORT)
        self.sensor.register_callback(BUTTON_START, self.button_start_pressed)

    def button_start_pressed(self, data):
        print("button 1 pressed")

    # game loop
    # found on https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTimer.html
    def init_timer_game_loop(self):
        self.timer = QtCore.QTimer(self)
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
            value_grav_y = value_gravitiy_sensor['y']
            print(value_y)
            print(value_grav_y)
            print("_______________")
            #self.play_tone()
            self.update()
        
    def play_tone(self):
        pass

    def start_the_game(self):
        self.player.open_stream()
        self.game_state = GameState.START
        #for i in range(len(self.seven_nation_army)):
            #self.player.play_wave(self.synthesizer.generate_constant_wave(self.seven_nation_army[i][0],self.seven_nation_army[i][1]))
   

        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = Game()
    app.exec()
