from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont

import sys

class SoundPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.notificationWindow = None  # Declare the notification window at the class level

    def initUI(self):
        self.playButton = QPushButton('Play Sound', self)
        self.playButton.clicked.connect(self.play_sound)

        self.notifButton = QPushButton('Show Notification', self)
        self.notifButton.clicked.connect(lambda: self.show_notification("Notification", "Hi"))

        layout = QVBoxLayout()
        layout.addWidget(self.playButton)
        layout.addWidget(self.notifButton)

        self.setLayout(layout)

        self.player = QMediaPlayer()

    def play_sound(self):
        url = QUrl.fromLocalFile("/Users/ale/Documents/sound.wav")
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def show_notification(self, title, message, duration=5000):
        if self.notificationWindow is not None:  # Check if a notification window is already open
            self.notificationWindow.close()  # Close the existing window before opening a new one

        self.notificationWindow = QWidget()  # Instantiate the notification window at the class level
        self.notificationWindow.setWindowTitle(title)
        self.notificationWindow.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        label = QLabel(message, self.notificationWindow)
        label.setFont(QFont('Arial', 18))
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.notificationWindow.setLayout(layout)

        self.notificationWindow.setGeometry(100, 100, 400, 200)
        self.notificationWindow.show()

        QTimer.singleShot(duration, self.notificationWindow.close)  # Close the window after 'duration' milliseconds

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = SoundPlayer()
    player.show()
    sys.exit(app.exec_())
