from PyQt5.QtWidgets import QApplication

def get_window_height():
    screen = QApplication.desktop().screenGeometry()
    return screen.height()