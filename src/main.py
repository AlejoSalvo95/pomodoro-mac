from PyQt5.QtWidgets import QApplication
import sys 
from pomodoro_window import PomodoroWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PomodoroWindow()
    window.show()
    sys.exit(app.exec_())
