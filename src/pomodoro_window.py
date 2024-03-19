from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from sound_manager import SoundManager
import sys
from utils import get_window_height

class PomodoroWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pomodoroWindow = None
        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.update_countdown)
        self.phase = 1
        self.remainingTime = 0
        self.long = False
        self.soundManager = SoundManager()

    def initUI(self):
        self.setWindowTitle('Pomodoro Timer')
        self.resize(300, 100)
        self.move(50, get_window_height() - 350)

        self.notifButton = QPushButton('Pomodoro short example', self)
        self.notifButton.clicked.connect(lambda: self.pomodoro_short())

        self.notifButton2 = QPushButton('Pomodoro 15/5', self)
        self.notifButton2.clicked.connect(lambda: self.pomodoro_long())

        layout = QVBoxLayout()
        layout.addWidget(self.notifButton)
        layout.addWidget(self.notifButton2)

        self.setLayout(layout)

    def increase_timer(self):
        self.remainingTime += 60
        if self.pomodoroWindow:
            self.label.setText(self.label_format())

    def decrease_timer(self):
        if self.remainingTime > 60:
            self.remainingTime -= 60
            if self.pomodoroWindow:
                self.label.setText(self.label_format())

    def set_title(self, layout):
        self.title = QLabel(f"Work", self.pomodoroWindow)
        self.title.setFont(QFont('Arial', 22))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

    def label_format(self):
        mins, secs = divmod(self.remainingTime, 60)
        return f"{mins:02d}:{secs:02d}"

    def set_label(self, layout):
        self.label = QLabel(self.label_format(), self.pomodoroWindow)
        self.label.setFont(QFont('Arial', 18))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def pomodoro_short(self):
        self.pomodoro()

    def pomodoro_long(self):
        self.long = True
        self.pomodoro()

    def pomodoro(self):
        if self.pomodoroWindow is not None:
            self.pomodoroWindow.close()

        self.phase = 1
        duration = self.set_main_window()

        layout = QVBoxLayout()
        self.set_title(layout)
        self.set_label(layout)
        self.set_plus_minus(layout)

        self.pomodoroWindow.setLayout(layout)

        windowHeight = 150
        windowWidth = 250
        x = 50
        y = get_window_height() - windowHeight - 50

        self.pomodoroWindow.setGeometry(x, y, windowWidth, windowHeight)
        self.set_notification_background(self.pomodoroWindow, QColor('#427126'))
        self.pomodoroWindow.show()

        self.countdownTimer.start(1000)

    def set_main_window(self):
        if self.long == True:
            duration = 900000
        else:
            duration = 5000
        self.remainingTime = duration // 1000
        self.pomodoroWindow = QWidget()
        self.pomodoroWindow.setWindowTitle('Pomodoro')
        self.pomodoroWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        return duration

    def set_plus_minus(self, layout):
        self.plusButton = QPushButton('+', self.pomodoroWindow)
        self.plusButton.clicked.connect(self.increase_timer)
        self.plusButton.setFixedWidth(40)
        layout.addWidget(self.plusButton)

        self.minusButton = QPushButton('-', self.pomodoroWindow)
        self.minusButton.clicked.connect(self.decrease_timer)
        self.minusButton.setFixedWidth(40)
        layout.addWidget(self.minusButton)

    def start_second_phase(self):
            if self.long == True:
                duration = 300000 
            else:
                duration = 3000
            self.remainingTime = duration // 1000
            self.set_notification_background(self.pomodoroWindow, QColor('#5B9899'))
            self.label.setText(self.label_format())
            self.title.setText("Relax")

    def start_third_phase(self):
            if self.long == True:
                duration = 900000
            else:
                duration = 5000
            self.remainingTime = duration // 1000
            self.set_notification_background(self.pomodoroWindow, QColor('#5D923E'))
            self.label.setText(self.label_format())
            self.title.setText("Work")

    def start_fourth_phase(self):
            if self.long == True:
                duration = 300000
            else:
                duration = 3000
            self.remainingTime = duration // 1000
            self.set_notification_background(self.pomodoroWindow, QColor('#5B9899'))
            self.label.setText(self.label_format())
            self.title.setText("Relax")

    def set_notification_background(self, window, color):
        palette = window.palette()
        palette.setColor(QPalette.Window, color)
        window.setPalette(palette)

    def update_countdown(self):
        if self.remainingTime > 0:
            self.remainingTime -= 1
            self.label.setText(self.label_format())
        else:
            self.next_phase()

    def next_phase(self):
        if self.phase == 1:
            self.close_first_phase()
        elif self.phase == 2:
            self.close_second_phase()
        elif self.phase == 3:
            self.close_third_phase()
        elif self.phase == 4:
            self.close_fourth_phase()

    def close_first_phase(self):
        self.phase += 1
        self.soundManager.play_sound_break()
        self.start_second_phase()

    def close_second_phase(self):
        self.phase += 1
        self.soundManager.play_sound_work()
        self.start_third_phase()

    def close_third_phase(self):
        self.phase += 1
        self.soundManager.play_sound_break()
        self.start_fourth_phase()

    def close_fourth_phase(self):
        self.phase += 1
        self.soundManager.play_sound_close()
        self.pomodoroWindow.close()