from PyQt5.QtWidgets import *

import query_manager

class Signup(QWidget):
    def __init__(self, _app: QApplication, _pwin: QWidget):
        super().__init__()
        self.app = _app
        self.login_window = _pwin

        # Champs de texte
        self.username = QLineEdit()
        self.username.setPlaceholderText("Nom d'utilisateur")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Adresse e-mail (optionel)")

        # Boutons
        self.signup_button = QPushButton()
        self.signup_button.setText("S'inscrire")
        self.signup_button.clicked.connect(self.signup_button_press)

        self.output_label = QLabel("foobar")
        self.output_label.setStyleSheet("color: white; background-color: red;")
        self.output_label.hide()


        # Layouts & fenêtre
        layout = QVBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.email)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.output_label)

        self.setLayout(layout)

    def signup_button_press(self):
        hashed_password = query_manager.passhash(self.password.text())
        email_address = self.email.text() if query_manager.valid_email(self.email.text()) else None
        
        if self.app.logged_user > 0:
            self.output_label.setText("Il faut se déconnecter avant !")
            self.output_label.show()


        if self.username.text() == "" or self.username.text().isspace() or self.username.text() is None or not self.username.text().isalnum() or not 5 <= len(self.username.text()) <= 50:
            self.output_label.setText("Vous devez entrer un nom d'utilisateur correct ! (Alphanumérique uniquement et entre 5–50 caractères inclusif)")
            self.output_label.show()
            return


        if len(self.password.text()) < 14 or self.password.text().isspace() or self.password.text() is None:
            self.output_label.setText("Vous devez entrer un mot de passe ! (Minimum 14 caractères)")
            self.output_label.show()
            return


        con, cur = query_manager.db_connect()
        cur.execute("SELECT pseudo FROM UTILISATEUR WHERE pseudo = ? LIMIT 1;", [self.username.text()])
        userdata = cur.fetchone()
        query_manager.db_disconnect(con)

        if userdata is not None and userdata != []:
            if userdata[0] == self.username.text():
                self.output_label.setText("Nom d'utilisateur déjà pris ! Veuillez en choisir un autre.")
                self.output_label.show()
                return

        
        con, cur = query_manager.db_connect()
        cur.execute("INSERT INTO UTILISATEUR(pseudo, password, email) VALUES (?, ?, ?);", [self.username.text(), hashed_password, email_address])
        con.commit()
        query_manager.db_disconnect(con)
        
        
        self.close()
        QMessageBox.information(self.login_window, "Inscription réussie", f"Inscription réussie, {self.username.text()} ! Vous pouvez maintenant vous connecter.")
        

    def closeEvent(self, a0):
        self.login_window.show()