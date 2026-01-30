import sys
import random as r

from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest



### Variables du jeu ###
button_map = {
    'r' : {
        "stylesheet_def" : "height: 200px; background-color: #f00; border: 5px solid #a00; border-radius: 5px;",
        "stylesheet_hilight" : "height: 200px; background-color: #f88; border: 5px solid #f44; border-radius: 5px;",
        "widget" : None,
    },
    'g' : {
        "stylesheet_def" : "height: 200px; background-color: #0f0; border: 5px solid #0a0; border-radius: 5px;",
        "stylesheet_hilight" : "height: 200px; background-color: #8f8; border: 5px solid #4f4; border-radius: 5px;",
        "widget" : None,
    },
    'b' : {
        "stylesheet_def" : "height: 200px; background-color: #00f; border: 5px solid #00a; border-radius: 5px;",
        "stylesheet_hilight" : "height: 200px; background-color: #88f; border: 5px solid #44f; border-radius: 5px;",
        "widget" : None,
    },
    'y' : {
        "stylesheet_def" : "height: 200px; background-color: #ff0; border: 5px solid #aa0; border-radius: 5px;",
        "stylesheet_hilight" : "height: 200px; background-color: #ff8; border: 5px solid #ff4; border-radius: 5px;",
        "widget" : None,
    }
}

num_map = {
    1 : 'r',
    2 : 'g',
    3 : 'b',
    4 : 'y'
}



### Fenêtre principale ###
class Main(QWidget):
    def __init__(self, _app: QApplication):
        super().__init__()
        self.app = _app
        self.debounce = False
        self.debounce_game = False
        self.last_press: str = ''
        self.game_button_pressed: bool = False
        
        ### Boutons 'menu' ###
        self.b_play = QPushButton()
        self.b_play.setText("Jouer")
        self.b_play.pressed.connect(self.b_play_press)
        
        self.b_login = QPushButton()
        self.b_login.setText("Connexion\nInscription")
        self.b_login.pressed.connect(self.b_login_press)
        
        self.b_score = QPushButton()
        self.b_score.setText("Scores")
        self.b_score.pressed.connect(self.b_score_press)

        self.b_quit = QPushButton()
        self.b_quit.setText("Quitter")
        self.b_quit.pressed.connect(self.b_quit_press)
        
        bLayout = QHBoxLayout()
        bLayout.addWidget(self.b_play)
        bLayout.addWidget(self.b_login)
        bLayout.addWidget(self.b_quit)
        bLayout.addWidget(self.b_score)
        
        ### Boutons du jeu ###
        self.g_red = QPushButton()
        self.g_red.setStyleSheet("height: 200px; background-color: #f00; border: 5px solid #a00; border-radius: 5px;")
        self.g_red.pressed.connect(lambda: self.g_button_press('r'))
        button_map['r']['widget'] = self.g_red
        
        self.g_green = QPushButton()
        self.g_green.setStyleSheet("height: 200px; background-color: #0f0; border: 5px solid #0a0; border-radius: 5px;")
        self.g_green.pressed.connect(lambda: self.g_button_press('g'))
        button_map['g']['widget'] = self.g_green
        
        self.g_blue = QPushButton()
        self.g_blue.setStyleSheet("height: 200px; background-color: #00f; border: 5px solid #00a; border-radius: 5px;")
        self.g_blue.pressed.connect(lambda: self.g_button_press('b'))
        button_map['b']['widget'] = self.g_blue
        
        self.g_yellow = QPushButton()
        self.g_yellow.setStyleSheet("height: 200px; background-color: #ff0; border: 5px solid #aa0; border-radius: 5px;")
        self.g_yellow.pressed.connect(lambda: self.g_button_press('y'))
        button_map['y']['widget'] = self.g_yellow
        
        gLayout = QGridLayout()
        gLayout.addWidget(self.g_red, 0, 0)
        gLayout.addWidget(self.g_green, 0, 1)
        gLayout.addWidget(self.g_blue, 1, 0)
        gLayout.addWidget(self.g_yellow, 1, 1)
        
        ### Labels ###
        self.label1 = QLabel()
        self.label1.setText("Niveau : 0")
        
        self.label2 = QLabel()
        self.label2.setText("Appuyez sur [Jouer] pour jouer.")
        
        ### Layout principal ###
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(bLayout)
        mainLayout.addLayout(gLayout)
        mainLayout.addWidget(self.label1)
        mainLayout.addWidget(self.label2)
        mainLayout.addSpacing(5)
        
        self.setLayout(mainLayout)
    
    
    
    ### Fonctions boutons 'menu' ###
    def b_play_press(self):
        print("ok")
        if self.debounce_game:
            return
        self.debounce_game = True
        game_running = True
        game_sequence: list[str] = []
        print("ok")
        while game_running:
            print("ok")
            game_sequence.append(num_map[r.randint(1, 4)])
            level = len(game_sequence)
            self.label1.setText(f"Niveau : {level}")
            self.label2.setText("Mémorisez la séquence")
            QTest.qWait(750)
            
        
            for i in game_sequence:
                selected_button = button_map[i]
                selected_button["widget"].setStyleSheet(selected_button["stylesheet_hilight"])
                QTest.qWait(200)
                selected_button["widget"].setStyleSheet(selected_button["stylesheet_def"])
                QTest.qWait(200)
        
            self.label2.setText("Maintenant cliquez sur chaque bouton")
            
            for i in game_sequence:
                while not self.game_button_pressed:
                    QTest.qWait(1)
                self.game_button_pressed = False
                
                if self.last_press != i:
                    self.label2.setText(f"Perdu ! Veuillez recommencer une partie. (SCORE : {level})")
                    game_running = False
                    self.game_button_pressed = False
                    return
    
    def b_login_press(self):
        if self.debounce:
            return
        self.debounce = True
        pass
    
    def b_quit_press(self):
        sys.exit(self.app.exec_())
    
    def b_score_press(self):
        pass
    
    def g_button_press(self, col: str):
        if self.debounce_game:
            return
        self.debounce_game = True
        
        self.last_press = col
        self.game_button_pressed = True
        selected_button = button_map[col]
        selected_button["widget"].setStyleSheet(selected_button["stylesheet_hilight"])
        QTest.qWait(200)
        selected_button["widget"].setStyleSheet(selected_button["stylesheet_def"])
        QTest.qWait(200)
        self.debounce_game = False
            
            



### Démarrage du programme ###
app = QApplication(sys.argv)
window = Main(app)
window.setWindowTitle("Jeu su sigmund")
window.setMinimumSize(500, 750)
window.show()
sys.exit(app.exec_())