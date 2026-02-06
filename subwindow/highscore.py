from PyQt5.QtWidgets import *

class HScoreWindow(QWidget):
    def __init__(self, _app:QApplication):
        super().__init__()
        self.app = _app