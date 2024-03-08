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
        self.countdownTimer = QTimer(self)  # Timer for countdown updates
        self.countdownTimer.timeout.connect(self.update_countdown)
        self.remainingTime = 0

    def initUI(self):
        self.notifButton = QPushButton('Show Notification', self)
        self.notifButton.clicked.connect(lambda: self.show_notification("Work", "Hi", 5000))

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

    def close_notification(self):
        self.countdownTimer.stop()
        self.play_sound()
        self.notificationWindow.close()

    def set_label(self, message, layout):
        self.label = QLabel(f"{message}\nClosing in {self.remainingTime} seconds", self.notificationWindow)
        self.label.setFont(QFont('Arial', 18))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def show_notification(self, title, message, duration=5000):
        if self.notificationWindow is not None:
            self.notificationWindow.close()

        self.remainingTime = duration // 1000
        self.notificationWindow = QWidget()
        self.notificationWindow.setWindowTitle(title)
        self.notificationWindow.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.set_label(message, layout)
        self.notificationWindow.setLayout(layout)

        self.notificationWindow.setGeometry(100, 100, 400, 200)
        self.notificationWindow.show()

        self.countdownTimer.start(1000)
        QTimer.singleShot(duration, self.close_notification)

    def update_countdown(self):
        if self.remainingTime > 0:
            self.remainingTime -= 1
            self.label.setText(f"Notification\nClosing in {self.remainingTime} seconds")
        else:
            self.countdownTimer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = SoundPlayer()
    player.show()
    sys.exit(app.exec_())
