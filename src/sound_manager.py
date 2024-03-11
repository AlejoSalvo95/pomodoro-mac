from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os

class SoundManager:
    def __init__(self):
        self.player = QMediaPlayer()

    def play_sound(self, sound_file_name):
        sound_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', sound_file_name))
        url = QUrl.fromLocalFile(sound_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    
    def play_sound_break(self):
        self.play_sound('break.mp3')

    def play_sound_work(self):
        self.play_sound('work.mp3')

    def play_sound_close(self):
        self.play_sound('close.mp3')