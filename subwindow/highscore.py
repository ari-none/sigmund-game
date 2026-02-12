from PyQt5.QtWidgets import *

class HighScore(QWidget):
    def __init__(self, _app: QApplication, _pwin: QWidget):
        super().__init__()
        self.app = _app
        self.main_window = _pwin
        # TODO: Faire le tableau des scores
    
    def closeEvent(self, a0):
        self.app.submenu_open = False