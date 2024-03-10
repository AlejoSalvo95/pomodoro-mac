from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont, QPalette, QColor
import os
import sys

class SoundPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.notificationWindow = None
        self.countdownTimer = QTimer(self)  # Timer for countdown updates
        self.countdownTimer.timeout.connect(self.update_countdown)
        self.phase = 1
        self.remainingTime = 0

    def initUI(self):
        self.notifButton = QPushButton('Pomodoro short example', self)
        self.notifButton.clicked.connect(lambda: self.pomodoro_short())

        self.notifButton = QPushButton('Pomodoro 15/5', self)
        self.notifButton.clicked.connect(lambda: self.pomodoro_short())

        layout = QVBoxLayout()
        layout.addWidget(self.notifButton)

        self.setLayout(layout)
        self.player = QMediaPlayer()

    def play_sound(self):
        sound_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'sound.wav'))
        url = QUrl.fromLocalFile(sound_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def close_first_notification(self):
        self.stop_countdown()
        self.start_second_phase(3000)

    def close_second_notification(self):
        self.stop_countdown()
        self.start_third_phase(3000)

    def close_third_notification(self):
        self.stop_countdown()
        self.start_fourth_phase(5000)

    def close_fourth_notification(self):
        self.stop_countdown()
        self.notificationWindow.close()

    def stop_countdown(self):
        self.countdownTimer.stop()
        self.play_sound()

    def set_title(self, layout):
        self.title = QLabel(f"Work", self.notificationWindow)
        self.title.setFont(QFont('Arial', 22))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

    def set_label(self, layout):
        self.label = QLabel(f"{self.remainingTime} seconds", self.notificationWindow)
        self.label.setFont(QFont('Arial', 18))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def pomodoro_short(self, duration=5000):
        self.pomodoro(duration)

    def pomodoro_long(self, duration=10000):
        self.pomodoro(duration)

    def pomodoro(self, duration):
        if self.notificationWindow is not None:
            self.notificationWindow.close()

        self.phase = 1

        self.remainingTime = duration // 1000
        self.notificationWindow = QWidget()
        self.notificationWindow.setWindowTitle('Pomodoro')
        self.notificationWindow.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.set_title(layout)
        self.set_label(layout)
        self.notificationWindow.setLayout(layout)

        self.notificationWindow.setGeometry(100, 100, 400, 200)
        self.set_notification_background(self.notificationWindow, QColor('#427126'))
        self.notificationWindow.show()

        self.countdownTimer.start(1000)
        QTimer.singleShot(duration, self.close_first_notification)

    def start_second_phase(self, duration):
        if self.phase == 1:
            self.phase = 2
            self.remainingTime = duration // 1000
            self.set_notification_background(self.notificationWindow, QColor('#5B9899'))
            self.label.setText(f"{self.remainingTime} seconds")
            self.title.setText("Relax")
            self.countdownTimer.start(1000)
            QTimer.singleShot(duration, self.close_second_notification)

    def start_third_phase(self, duration):
        if self.phase == 2:
            self.phase = 3
            self.remainingTime = duration // 1000
            self.set_notification_background(self.notificationWindow, QColor('#5D923E'))
            self.label.setText(f"{self.remainingTime} seconds")
            self.title.setText("Work")
            self.countdownTimer.start(1000)
            QTimer.singleShot(duration, self.close_third_notification)

    def start_fourth_phase(self, duration):
        if self.phase == 3:
            self.phase = 4
            self.remainingTime = duration // 1000
            self.set_notification_background(self.notificationWindow, QColor('#5B9899'))
            self.label.setText(f"{self.remainingTime} seconds")
            self.title.setText("Relax")
            self.countdownTimer.start(1000)
            QTimer.singleShot(duration, self.close_fourth_notification)

    def set_notification_background(self, window, color):
        palette = window.palette()
        palette.setColor(QPalette.Window, color)
        window.setPalette(palette)

    def update_countdown(self):
        if self.remainingTime > 0:
            self.remainingTime -= 1
            self.label.setText(f"{self.remainingTime} seconds")
        else:
            self.countdownTimer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = SoundPlayer()
    player.show()
    sys.exit(app.exec_())
