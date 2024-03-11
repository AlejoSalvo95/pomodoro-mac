from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont, QPalette, QColor
import os
import sys

class PomodoroWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.notificationWindow = None
        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.update_countdown)
        self.phase = 1
        self.remainingTime = 0
        self.long = False

    def initUI(self):
        self.setWindowTitle('Pomodoro Timer')
        self.resize(300, 100)
        self.move(50, self.get_window_height() - 350)

        self.notifButton = QPushButton('Pomodoro short example', self)
        self.notifButton.clicked.connect(lambda: self.pomodoro_short())

        self.notifButton2 = QPushButton('Pomodoro 15/5', self)
        self.notifButton2.clicked.connect(lambda: self.pomodoro_long())

        layout = QVBoxLayout()
        layout.addWidget(self.notifButton)
        layout.addWidget(self.notifButton2)

        self.setLayout(layout)
        self.player = QMediaPlayer()

    def play_sound(self, sound_file_name):
        sound_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', sound_file_name))
        url = QUrl.fromLocalFile(sound_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def close_first_phase(self):
        self.stop_countdown()
        self.play_sound_break()
        self.start_second_phase()

    def close_second_phase(self):
        self.stop_countdown()
        self.play_sound_work()
        self.start_third_phase()

    def close_third_phase(self):
        self.stop_countdown()
        self.play_sound_break()
        self.start_fourth_phase()

    def close_fourth_phase(self):
        self.stop_countdown()
        self.play_sound_close()
        self.notificationWindow.close()

    def stop_countdown(self):
        self.countdownTimer.stop()

    def play_sound_break(self):
        self.play_sound('break.mp3')

    def play_sound_work(self):
        self.play_sound('work.mp3')

    def play_sound_close(self):
        self.play_sound('close.mp3')

    def set_title(self, layout):
        self.title = QLabel(f"Work", self.notificationWindow)
        self.title.setFont(QFont('Arial', 22))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

    def label_format(self):
        mins, secs = divmod(self.remainingTime, 60)
        return f"{mins:02d}:{secs:02d}"

    def set_label(self, layout):
        self.label = QLabel(self.label_format(), self.notificationWindow)
        self.label.setFont(QFont('Arial', 18))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def pomodoro_short(self):
        self.pomodoro()

    def pomodoro_long(self):
        self.long = True
        self.pomodoro()

    def get_window_height(self):
        screen = QApplication.desktop().screenGeometry()
        y = screen.height()
        return y

    def pomodoro(self):
        if self.notificationWindow is not None:
            self.notificationWindow.close()

        self.phase = 1

        if self.long == True:
            duration = 900000
        else:
            duration = 5000
        self.remainingTime = duration // 1000
        self.notificationWindow = QWidget()
        self.notificationWindow.setWindowTitle('Pomodoro')
        self.notificationWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()
        self.set_title(layout)
        self.set_label(layout)
        self.notificationWindow.setLayout(layout)

        windowHeight = 150
        windowWidth = 250
        x = 50
        y = self.get_window_height() - windowHeight - 50

        self.notificationWindow.setGeometry(x, y, windowWidth, windowHeight)
        self.set_notification_background(self.notificationWindow, QColor('#427126'))
        self.notificationWindow.show()

        self.countdownTimer.start(1000)
        QTimer.singleShot(duration, self.close_first_phase)

    def start_second_phase(self):
        if self.phase == 1:
            self.phase = 2
            if self.long == True:
                duration = 300000 
            else:
                duration = 3000
            self.remainingTime = duration // 1000
            self.set_notification_background(self.notificationWindow, QColor('#5B9899'))
            self.label.setText(self.label_format())
            self.title.setText("Relax")
            self.countdownTimer.start(1000)
            QTimer.singleShot(duration, self.close_second_phase)

    def start_third_phase(self):
        if self.phase == 2:
            self.phase = 3

            if self.long == True:
                duration = 900000
            else:
                duration = 5000
            self.remainingTime = duration // 1000
            self.set_notification_background(self.notificationWindow, QColor('#5D923E'))
            self.label.setText(self.label_format())
            self.title.setText("Work")
            self.countdownTimer.start(1000)
            QTimer.singleShot(duration, self.close_third_phase)

    def start_fourth_phase(self):
        if self.phase == 3:
            self.phase = 4

            if self.long == True:
                duration = 300000
            else:
                duration = 3000
            self.remainingTime = duration // 1000
            self.set_notification_background(self.notificationWindow, QColor('#5B9899'))
            self.label.setText(self.label_format())
            self.title.setText("Relax")
            self.countdownTimer.start(1000)
            QTimer.singleShot(duration, self.close_fourth_phase)

    def set_notification_background(self, window, color):
        palette = window.palette()
        palette.setColor(QPalette.Window, color)
        window.setPalette(palette)

    def update_countdown(self):
        if self.remainingTime > 0:
            self.remainingTime -= 1
            self.label.setText(self.label_format())
        else:
            self.countdownTimer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = PomodoroWindow()
    player.show()
    sys.exit(app.exec_())
