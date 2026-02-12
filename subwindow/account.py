from PyQt5.QtWidgets import *

class Account(QWidget):
    def __init__(self, _app:QApplication):
        super().__init__()
        self.app = _app