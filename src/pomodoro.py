from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont
import os
import sys

class SoundPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.notificationWindow = None
        self.remainingTime = 0

    def initUI(self):
        self.notifButton = QPushButton('Start Pomodoro 25/5', self)
        self.notifButton.clicked.connect(lambda: self.show_notification("Pomodoro", "Time left: 00:05", 5))

        layout = QVBoxLayout()
        layout.addWidget(self.notifButton)

        self.setLayout(layout)
        self.player = QMediaPlayer()


    def play_sound(self):
        # Construct an absolute path to the sound file
        sound_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'sound.wav'))
        url = QUrl.fromLocalFile(sound_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
        
    def show_notification(self, title, message, duration):
        if self.notificationWindow is not None:
            self.notificationWindow.close()

        self.remainingTime = duration

        self.notificationWindow = QWidget()
        self.notificationWindow.setWindowTitle(title)
        self.notificationWindow.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.timeLabel = QLabel(message, self.notificationWindow)
        self.timeLabel.setFont(QFont('Arial', 18))
        self.timeLabel.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.timeLabel)
        self.notificationWindow.setLayout(layout)

        self.notificationWindow.setGeometry(100, 100, 400, 200)
        self.notificationWindow.show()

        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.update_countdown)
        self.countdownTimer.start(1000)

    def update_countdown(self):
        self.remainingTime -= 1
        minutes, seconds = divmod(self.remainingTime, 60)
        self.timeLabel.setText(f"Time left: {minutes:02d}:{seconds:02d}")
        if self.remainingTime <= 0:
            self.countdownTimer.stop()
            self.play_sound()
            self.notificationWindow.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = SoundPlayer()
    player.show()
    sys.exit(app.exec_())
