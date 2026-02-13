from PyQt5.QtWidgets import *

class Account(QWidget):
    def __init__(self, _app:QApplication):
        super().__init__()
        self.app = _app
    
    def closeEvent(self, a0):
        self.app.submenu_open = False