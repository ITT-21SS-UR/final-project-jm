import time
import sys
import melodies

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from synthesizer import Player, Synthesizer, Waveform
from enum import Enum
from DIPPID import SensorUDP

"""
Script evenly written by Marco Beetz & Joshua Benker

Melody Game
_________________

Play famous melodies
Rotate your dippid device like a clock and jam your favorite classic melodies

"""

SENSOR_PORT = 5700


# state of the game
class GameState(Enum):
    INTRO = 1
    START = 2
    DONE = 3
    PRACTICE = 4

# main game class
# all important variables and functions


class Game(QMainWindow):
    amount_rounds = 5
    sensor = ()
    timer = ()
    song = []
    points = 0
    round_points = 0
    song_list = ["seven_nation_army",
                 "amours_toujours",
                 "i_cant_get_no_satisfaction",
                 "come_as_you_are",
                 "smoke_on_the_water",
                 "another_one_bites_the_dust"]
    played_songs = []
    played_tones = []
    played_tone = ""
    current_song = ""
    round = 0
    note_to_play = ""
    button_pressed = False
    c_chord = ["C4", "E4", "G4"]

    def __init__(self):
        super().__init__()
        self.setGeometry(700, 100, 800, 600)
        self.player = Player()
        self.synthesizer = Synthesizer(
            osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
        self.game_state = GameState.INTRO
        self.timer = QTimer(self)
        self.current_tones = []
        self.song = []
        self.last_played_tone = ""
        self.points_to_calc = "on"
        self.sensor = SensorUDP(SENSOR_PORT)
        self.init_timer_game_loop()
        self.initUIComponents()

    # main ui function for initializing and configuring the UI components
    # especially buttons and labels
    def initUIComponents(self):
        self.title_label = QLabel(self)
        self.title_label.setFont(QFont("Helvetica", 20))
        self.title_label.setText("Welcome to our Melody Game!")
        self.title_label.setMinimumSize(400, 75)
        self.title_label.move(240, 0)
        self.help_button = QPushButton(self)
        self.help_button.setGeometry(750, 20, 30, 30)
        self.help_button.clicked.connect(self.help_button_clicked)
        self.help_button.setIcon(QIcon('info_icon.png'))

        self.game_info_label = QLabel(self)
        self.game_info_label.setText(
            "Press the Button below to play or practice the game! \n"
            "  You can play melodies by moving your dippid device!")
        self.game_info_label.setMinimumSize(400, 50)
        self.game_info_label.move(220, 50)

        self.dippid_info_label = QLabel(self)
        self.dippid_info_label.setText(
            "Rotate your dippid device to play different tones"
            " nand follow the melody")
        self.dippid_info_label.setMinimumSize(400, 50)
        self.dippid_info_label.move(220, 50)
        self.dippid_info_label.setVisible(False)

        self.song_name = QLabel(self)
        self.song_name.setText("Song name: " + self.current_song)
        self.song_name.setMinimumSize(400, 50)
        self.song_name.move(220, 80)
        self.song_name.setVisible(False)

        self.points_info = QLabel(self)
        self.points_info.setText("Points: " + str(self.points))
        self.points_info.setMinimumSize(400, 50)
        self.points_info.move(220, 110)
        self.points_info.setVisible(False)
        self.played_tones_label = QLabel(self)
        self.played_tones_label.setText("Played notes: ")
        self.played_tones_label.setMinimumSize(400, 50)
        self.played_tones_label.move(220, 130)
        self.played_tones_label.setVisible(False)

        self.play_melody = QPushButton(self)
        self.play_melody.setText("Play Melody")
        self.play_melody.setMinimumSize(150, 100)
        self.play_melody.setStyleSheet("background-color: green")
        self.play_melody.move(600, 150)
        self.play_melody.clicked.connect(self.play_song)
        self.play_melody.setVisible(False)

        self.next_round_button = QPushButton(self)
        self.next_round_button.setText("Next Round")
        self.next_round_button.setMinimumSize(150, 100)
        self.next_round_button.setStyleSheet("background-color: lightgreen")
        self.next_round_button.move(600, 150)
        self.next_round_button.clicked.connect(self.new_round)
        self.next_round_button.setVisible(False)

        self.practice_button = QPushButton(self)
        self.practice_button.setText("Practice")
        self.practice_button.setMinimumSize(150, 100)
        self.practice_button.setStyleSheet("background-color: lightblue")
        self.practice_button.move(50, 150)
        self.practice_button.clicked.connect(self.practice_button_clicked)

        self.round_info = QPushButton(self)
        self.round_info.setMinimumSize(160, 100)
        self.round_info.setStyleSheet("background-color: lightblue")
        self.round_info.move(50, 150)
        self.round_info.setVisible(False)

        self.start_button = QPushButton(self)
        self.start_button.setText("Start the game")
        self.start_button.setMinimumSize(150, 100)
        self.start_button.setStyleSheet("background-color: lightgreen")
        self.start_button.move(600, 150)
        self.start_button.clicked.connect(self.start_button_clicked)

        self.game_done_info = QLabel(self)
        self.game_done_info.setText(
            "Congratz! You made " + str(self.points) +
            " Points. Let's play another one?")
        self.game_done_info.setMinimumSize(400, 50)
        self.game_done_info.move(220, 300)
        self.game_done_info.setVisible(False)

    # inits the help button content
    def help_button_clicked(self):
        self.help_box = QDialog(self)
        self.help_box.setGeometry(0, 0, 650, 400)
        line1 = QLabel(
            "1) Put your phone steady in front of the computer", self.help_box)
        line1.move(10, 10)
        line2 = QLabel(
            "2) Get DIPPID ready and activate send data function",
            self.help_box)
        line2.move(10, 40)
        line3 = QLabel(
            "3) Go into practice mode and play some sounds",
            self.help_box)
        line3.move(10, 70)
        line4 = QLabel(
            "4) Turn the phone around like a clock towards the circles",
            self.help_box)
        line4.move(10, 100)
        line5 = QLabel(
            "5) After turning the phone press button 1 or button 2 once",
            self.help_box)
        line5.move(10, 130)
        line6 = QLabel(
            "6) The sound is played according to your position"
            " when you pressed the button",
            self.help_box)
        line6.move(10, 160)
        line7 = QLabel(
            "If you feel comfortable, switch to play mode and"
            " try to recreate a well-known melody",
            self.help_box)
        line7.move(10, 230)
        line8 = QLabel(
            "Play one sound after another and "
            " get feedback how well you performed",
            self.help_box)
        line8.move(10, 260)
        line9 = QLabel(
            "Wait: Do not press and hold the button, "
            "press it only once when you turned your phone",
            self.help_box)
        font = PyQt5.QtGui.QFont()
        font.setBold(True)
        line9.setFont(font)
        line9.setStyleSheet("color: rgb(255,0,0)")
        line9.move(10, 300)
        self.help_box.open()

    # paint function
    # paints the clock-alike design for visualizing the played tones
    def paintEvent(self, event):
        pt = QPainter()
        pt.begin(self)
        background_rect = QRect(0, 0, 800, 600)
        background_brush = QBrush(QColor(255, 170, 255), Qt.SolidPattern)
        pt.fillRect(background_rect, background_brush)

        if (self.game_state == GameState.START) or\
                (self.game_state == GameState.PRACTICE):
            self.tone_rect_0 = QRect(365, 200, 75, 75)
            self.tone_rect_1 = QRect(240, 300, 75, 75)
            self.tone_rect_2 = QRect(240, 400, 75, 75)
            self.tone_rect_3 = QRect(365, 500, 75, 75)
            self.tone_rect_4 = QRect(490, 400, 75, 75)
            self.tone_rect_5 = QRect(490, 300, 75, 75)
            pt.setPen(QPen(Qt.black))
            pt.drawEllipse(self.tone_rect_0)
            pt.drawEllipse(self.tone_rect_1)
            pt.drawEllipse(self.tone_rect_2)
            pt.drawEllipse(self.tone_rect_3)
            pt.drawEllipse(self.tone_rect_4)
            pt.drawEllipse(self.tone_rect_5)

            if self.played_tone != "":
                tone_rect = "tone_rect_" + self.played_tone
                played_tone_rect = getattr(self, tone_rect)
                brush = QBrush(Qt.yellow)
                pt.setBrush(brush)
                pt.drawEllipse(played_tone_rect)

            for i in range(5):
                tone_rect = "tone_rect_" + str(i + 1)
                try:
                    pt.drawText(getattr(self, tone_rect),
                                Qt.AlignCenter, self.current_tones[i])
                except IndexError:
                    pass
        pt.end()
        self.update()

    # gets called when the player wants to practice
    # adjusts the UI
    def practice_button_clicked(self):
        self.practice_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.game_state = GameState.PRACTICE
        self.current_tones = melodies.select_practice_tones()

    # adjusts the UI when the "start game" button was clicked
    # calls the start_game function
    def start_button_clicked(self):
        self.practice_button.setVisible(False)
        self.start_button.setVisible(False)
        self.game_info_label.setVisible(False)
        self.dippid_info_label.setVisible(True)
        self.play_melody.setVisible(True)
        self.song_name.setVisible(True)
        self.points_info.setVisible(True)
        self.played_tones_label.setVisible(True)
        self.game_done_info.setVisible(False)
        self.start_the_game()

    # game loop
    # found on https://doc.qt.io/qtforpython-5/PySide2/QtCore/QTimer.html
    def init_timer_game_loop(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(30)

    # main game loop
    # inits the sensor data
    # calls the "play_tone" func and checks if the round is finished
    def game_loop(self):
        if self.game_state == GameState.START:
            self.display_next_note()
            self.get_sensor_data()
            if len(self.played_tones) < len(self.song):
                if self.state_of_button == 1 and self.button_pressed == False:
                    self.play_tone(self.value_x, self.value_y, self.value_z)
                    self.button_pressed = True
                elif self.state_of_button == 0:
                    self.button_pressed = False
            else:
                self.show_round_result()
            self.update()
        elif self.game_state == GameState.PRACTICE:
            self.get_sensor_data()
            if self.state_of_button == 1 and self.button_pressed == False:
                    self.play_tone(self.value_x, self.value_y, self.value_z)
                    self.button_pressed = True
            elif self.state_of_button == 0:
                    self.button_pressed = False

        elif self.game_state == GameState.DONE:
            pass

    # function for receiving the sensor data for accelerometer and the button
    def get_sensor_data(self):
        try:
                self.state_of_button = self.sensor.get_value('button_1')
                self.value_sensor = self.sensor.get_value('accelerometer')
                time.sleep(0.1)
                self.value_y = self.value_sensor['y']
                self.value_z = self.value_sensor['z']
                self.value_x = self.value_sensor['x']
        except TypeError:
            pass

    # shows the results of the past round
    # checks if player has played the given amount of rounds -> game done
    # calls the calculate points function
    # adjusts the UI
    def show_round_result(self):
        if self.round == self.amount_rounds:
            self.game_state = GameState.DONE
            self.game_done()
        else:
            if self.points_to_calc == "on":
                self.calc_points()
            self.points_to_calc = "off"
            self.next_round_button.setVisible(True)
            text1 = "Round no " + \
                str(self.round) + " done.  \n You made " + \
                str(self.round_points) + " of " + str(len(self.song)) + " !"
            self.round_info.setText(text1)
            self.round_info.setVisible(True)
            self.points_info.setText("Points: " + str(self.points))

    # handles the sensor DIPPID data
    # plays different tone depending to the angle of the DIPPID device
    # appends the tone to the played tone list
    # prepares further calculating the points
    def play_tone(self, x, y, z):
        tone = ''
        self.played_tone = ""
        if (0.33 > x > -0.33) and (0.76 < y < 1):
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
            self.played_tone = "3"
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
        if (tone != ''):
            self.synth_play_tone(tone)
            self.played_tones.append(tone)

    # displays the tone that the player hast to play next
    def display_next_note(self):
        self.note_to_play = self.song[len(self.played_tones)+1][0]
        self.played_tones_label.setText("Next note: " + str(self.note_to_play))

    # sets the game state to "start" when a new game is started
    def start_the_game(self):
        self.player.open_stream()
        self.game_state = GameState.START
        self.new_game()
        self.new_round()

    # plays a song by calling the synthesizer with MIDI notes
    def play_song(self):
        for i in range(len(self.song)):
            self.synth_play_tone(self.song[i][0], self.song[i][1])

    # calculates the general and round points
    def calc_points(self):
        for i in range(len(self.played_tones)):
            if self.song[i][0] == self.played_tones[i]:
                self.points += 1
                self.round_points += 1

    # calls the synthesizer to play a given tone
    def synth_play_tone(self, tone, length=0.5):
        self.player.play_wave(
            self.synthesizer.generate_constant_wave(tone, length))

    # new round function
    # selects a new song and updates the UI
    def new_round(self):
        self.round_points = 0
        if self.round != 0:
            self.played_songs.append(self.current_song)
        self.next_round_button.setVisible(False)
        self.round_info.setVisible(False)
        self.select_new_song()
        self.song = self.current_values
        song_name = self.current_song.replace("_", " ")
        song_name = song_name.capitalize()
        self.song_name.setText("Song name: " + song_name)
        self.played_tones = []
        self.points_to_calc = "on"
        self.round += 1

    # selects a new random song from the song list
    # the tuples from the dictionary in melodies.py is "unpacked"
    def select_new_song(self):
        self.current_song, values = melodies.select_new_song()
        self.current_values = values[0]
        self.current_tones = values[1]
        if (self.current_song in self.played_songs):
            self.select_new_song()

    # gets called when the game is done
    # adjusts the UI components
    # mainly visibility
    def game_done(self):
        self.dippid_info_label.setVisible(False)
        self.play_melody.setVisible(False)
        self.game_done_info.setVisible(True)
        self.points_info.setVisible(False)
        self.practice_button.setVisible(True)
        self.start_button.setVisible(True)
        self.game_info_label.setVisible(True)
        self.played_tones_label.setVisible(False)
        self.song_name.setText("Song name: ")

    # gets called when a new is started.
    # set all variables to the start state
    def new_game(self):
        self.points = 0
        self.current_song = ""
        self.current_tones = []
        self.played_songs = []
        self.round = 0
        self.points_info.setText("Points: " + str(self.points))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Game()
    win.show()
    app.exec()
