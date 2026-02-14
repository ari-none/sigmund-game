import sys
import random as r
import time

from mariadb import OperationalError
from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest

import query_manager
from query_manager import db_connect, db_disconnect
from subwindow.account import Account
from subwindow.highscore import HighScore
from subwindow.login import Login
# from subwindow.account import Account TODO: Terminer les comptes & inscriptions



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
        self.debounce_button = False
        self.debounce_game = False
        self.game_running = False
        self.last_press: str = ''
        self.game_button_pressed: bool = False
        
        ### Boutons 'menu' ###
        self.b_play = QPushButton()
        self.b_play.setText("Jouer")
        self.b_play.pressed.connect(self.b_play_press)
        
        self.b_account = QPushButton()
        self.b_account.setText("Compte")
        self.b_account.pressed.connect(self.b_account_press)
        
        self.b_score = QPushButton()
        self.b_score.setText("Scores")
        self.b_score.pressed.connect(self.b_score_press)

        self.b_quit = QPushButton()
        self.b_quit.setText("Quitter")
        self.b_quit.pressed.connect(self.b_quit_press)
        
        bLayout = QHBoxLayout()
        bLayout.addWidget(self.b_play)
        bLayout.addWidget(self.b_account)
        bLayout.addWidget(self.b_score)
        bLayout.addWidget(self.b_quit)
        
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
        self.label1.setStyleSheet("font-size: 30px;")
        
        self.label2 = QLabel()
        self.label2.setText("Appuyez sur [Jouer] pour jouer.")
        self.label2.setStyleSheet("font-size: 25px;")
        
        ### Layout principal ###
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(bLayout)
        mainLayout.addLayout(gLayout)
        mainLayout.addWidget(self.label1)
        mainLayout.addWidget(self.label2)
        mainLayout.addSpacing(5)
        
        self.setLayout(mainLayout)
    
    
    
    ### Fonctions boutons 'menu' ###
    def b_play_press(self, sequence: tuple[str, str] | None = None):
        if self.debounce_game or self.app.submenu_open:
            return
        self.debounce_game = True
        self.game_running = True
        
        game_set_sequence = sequence is not None
        seed_sequence: list[str] | None = list(sequence[0]) if game_set_sequence else None
        seed_og_user: str | None = sequence[1] if game_set_sequence else None
        
        game_sequence: list[str] = []
        temps_d = time.time()
        while self.game_running:
            level = len(game_sequence) + 1
            self.label1.setText(f"Niveau : {level}/{len(seed_sequence)}" if game_set_sequence else f"Niveau : {level}")
            
            if game_set_sequence and level == len(seed_sequence):
                temps_f = min(round(time.time() - temps_d, 3), 9999999.999)
                self.label2.setText(f"Vous avez gagné la partie de {seed_og_user} !\n(SCORE : {level})\n(TEMPS : {temps_f})")

                self.game_running = False
                self.game_button_pressed = False
                self.debounce_game = False
                return
            
            if game_set_sequence:
                game_sequence.append(seed_sequence[level-1])
            else:
                game_sequence.append(num_map[r.randint(1, 4)])
            self.label2.setText("Mémorisez la séquence")
            QTest.qWait(1000)
            
            
            if len(game_sequence) >= 250:
                temps_f = min(round(time.time() - temps_d, 3), 9999999.999)
                self.label2.setText(f"Oké, oké ! T'as gagné ! Va toucher de l'herbe maintenant.\n(SCORE : {level})\n(TEMPS : {temps_f})")

                if app.logged_user > 0:
                    try:
                        con, cur = query_manager.db_connect()
                        cur.execute("INSERT INTO PARTIE(sequence, temps, id_utilisateur) VALUES (?, ?, ?);", ["".join(game_sequence), temps_f, self.app.logged_user])
                        con.commit()
                        query_manager.db_disconnect(con)
                    except OperationalError:
                        query_manager.query_error(self, "Le score n'a pas pu être enregistré en ligne !")

                self.game_running = False
                self.game_button_pressed = False
                self.debounce_game = False
                return
            
        
            for i in game_sequence:
                selected_button = button_map[i]
                selected_button["widget"].setStyleSheet(selected_button["stylesheet_hilight"])
                QTest.qWait(250)
                selected_button["widget"].setStyleSheet(selected_button["stylesheet_def"])
                QTest.qWait(250)
        
            self.label2.setText("Maintenant cliquez sur chaque bouton")
            
            for i in game_sequence:
                self.game_button_pressed = False
                while not self.game_button_pressed:
                    QTest.qWait(1)
                self.game_button_pressed = False
                
                if self.last_press != i:
                    temps_f = min(round(time.time() - temps_d, 3), 9999999.999)
                    self.label2.setText(f"Perdu ! Veuillez recommencer une partie.\n(SCORE : {level})\n(TEMPS : {temps_f})")
                    
                    if app.logged_user > 0 and not game_set_sequence:
                        try:
                            con, cur = query_manager.db_connect()
                            cur.execute("INSERT INTO PARTIE(sequence, temps, id_utilisateur) VALUES (?, ?, ?);", ["".join(game_sequence), temps_f, self.app.logged_user])
                            con.commit()
                            query_manager.db_disconnect(con)
                        except OperationalError:
                            query_manager.query_error(self, "Le score n'a pas pu être enregistré en ligne !")
                    
                    self.game_running = False
                    self.game_button_pressed = False
                    self.debounce_game = False
                    return
    
    def b_account_press(self):
        if self.debounce_game or self.app.submenu_open:
            return

        try:
            con, _ = query_manager.db_connect()
            query_manager.db_disconnect(con)
        except OperationalError:
            query_manager.query_error(self, "Il y a eu un problème de connection !")
            return

        
        if self.app.logged_user > 0:
            self.app.submenu_open = True
            self.new_win = Account(self.app)
            self.new_win.setWindowTitle("Compte")
            self.new_win.setMinimumSize(500, 750)
            self.new_win.show()
        else:
            self.app.submenu_open = True
            self.new_win = Login(self.app)
            self.new_win.setWindowTitle("Connexion")
            self.new_win.setMinimumSize(500, 150)
            self.new_win.show()
    
    def b_score_press(self):
        if self.debounce_game or self.app.submenu_open:
            return
        if self.app.logged_user > 0:
            self.app.submenu_open = True
            self.new_win = HighScore(self.app, self)
            self.new_win.setWindowTitle("Scores")
            self.new_win.setMinimumSize(500, 500)
            self.new_win.show()
        else:
            QMessageBox.critical(self, "Compte requis", "Vous devez créer un compte pour accéder à cette fonctionalité !")

    def b_quit_press(self):
        result = QMessageBox.warning(self, "Confirmer", "Êtes-vous sûr de quitter le jeu du Sigmund ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            sys.exit(self.app.exec_())
    
    
    def g_button_press(self, col: str):
        if self.debounce_button:
            return
        self.debounce_button = True
        
        self.last_press = col
        self.game_button_pressed = True
        selected_button = button_map[col]
        selected_button["widget"].setStyleSheet(selected_button["stylesheet_hilight"])
        QTest.qWait(200)
        selected_button["widget"].setStyleSheet(selected_button["stylesheet_def"])
        QTest.qWait(200)
        self.debounce_button = False
            
            



### Démarrage du programme ###
app = QApplication(sys.argv)
app.logged_user = -1 # Sécurité de la NASA
app.submenu_open = False
window = Main(app)
window.setWindowTitle("Jeu su sigmund")
window.setMinimumSize(500, 750)
window.show()
sys.exit(app.exec_())