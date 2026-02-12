from PyQt5.QtWidgets import *

import query_manager
from .signup import Signup

class Login(QWidget):
    def __init__(self, _app: QApplication):
        super().__init__()
        self.app = _app
        
        # Champs de texte
        self.username = QLineEdit()
        self.username.setPlaceholderText("Nom d'utilisateur")
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Boutons
        self.confirm_button = QPushButton()
        self.confirm_button.setText("Se connecter")
        self.confirm_button.clicked.connect(self.confirm_button_press)

        self.signup_button = QPushButton()
        self.signup_button.setText("Pas de compte ?\nCliquez ici")
        self.signup_button.clicked.connect(self.signup_button_press)
        
        self.output_label = QLabel("foobar")
        self.output_label.setStyleSheet("color: white; background-color: red;")
        self.output_label.hide()
        
        
        # Layouts & fenêtre
        blayout = QHBoxLayout()
        blayout.addWidget(self.confirm_button)
        blayout.addWidget(self.signup_button)
        
        layout = QVBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addLayout(blayout)
        layout.addWidget(self.output_label)
        
        self.setLayout(layout)
    
    def signup_button_press(self):
        self.new_win = Signup(self.app, self)
        self.new_win.setWindowTitle("Inscription")
        self.new_win.setMinimumSize(500, 150)
        self.new_win.show()
        self.hide()
    
    def confirm_button_press(self):
        if self.app.logged_user > 0:
            self.output_label.setText("Déjà connecté !")
            self.output_label.show()
        
        
        if self.username.text() == "" or self.username.text().isspace() or self.username.text() is None:
            self.output_label.setText("Vous devez entrer votre nom d'utilisateur !")
            self.output_label.show()
            return 
        if not self.username.text().isalnum():
            self.output_label.setText("Vous devez entrer un nom d'utilisateur valide ! (Que des lettres & des chiffres)")
            self.output_label.show()
            return


        if self.password.text() == "" or self.password.text().isspace() or self.password.text() is None:
            self.output_label.setText("Vous devez entrer votre mot de passe !")
            self.output_label.show()
            return


        con, cur = query_manager.db_connect()
        cur.execute("SELECT pseudo, password, id FROM UTILISATEUR WHERE pseudo = ? LIMIT 1;", [self.username.text()])
        userdata = cur.fetchone()
        query_manager.db_disconnect(con)        
        
        if userdata is None or userdata == []:
            self.output_label.setText("Utilisateur non trouvé ! Si vous n'avez pas de compte, veuillez en créer un.")
            self.output_label.show()
            return 
        
        if userdata[1] != query_manager.passhash(self.password.text()):
            self.output_label.setText("Mot de passe invalide !")
            self.output_label.show()
            return
        
        
        self.app.logged_user = userdata[2]
        self.close()

    def closeEvent(self, a0):
        self.app.submenu_open = False