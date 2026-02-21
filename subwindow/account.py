from typing import Literal

from mariadb import OperationalError, Cursor
from PyQt5.QtWidgets import *

import query_manager

def del_email(self: QWidget) -> None:
    try:
        con, cur = query_manager.db_connect()
        cur.execute("UPDATE UTILISATEUR SET email = NULL WHERE id = ?;", [self.app.logged_user])
        con.commit()
        query_manager.db_disconnect(con)

        QMessageBox.information(self, "E-mail supprimés", "Le compte n'est désormais plus associé à une adresse e-mail !", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        self.email_label.setText("")
    except OperationalError:
        query_manager.query_error(self, "L'adresse e-mail n'a pas pu être supprimée !")

def del_score(self: QWidget, msg: bool) -> None:
    try:
        con, cur = query_manager.db_connect()
        cur.execute("DELETE FROM PARTIE WHERE id_utilisateur = ?;", [self.app.logged_user])
        con.commit()
        query_manager.db_disconnect(con)
        
        if msg:
            QMessageBox.information(self, "Scores supprimés", "Tous vos scores ont bien été supprimés !", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
    except OperationalError:
        query_manager.query_error(self, "Les scores n'ont pas pu être supprimés !")

def del_user(self: QWidget, msg: bool) -> None:
    try:
        con, cur = query_manager.db_connect()
        cur.execute("DELETE FROM UTILISATEUR WHERE id = ?;", [self.app.logged_user])
        con.commit()
        query_manager.db_disconnect(con)
        
        self.app.logged_user = -1

        if msg:
            QMessageBox.information(self, "Compte supprimé", "Votre compte avec tous vos scores ont bien été supprimés !", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
    except OperationalError:
        query_manager.query_error(self, "Le compte n'a pas pu être supprimé !")



class _ChangeForm(QWidget):
    def __init__(self, _app: QApplication, _pwin: QWidget, form_type: Literal["email", "password", "username"]):
        super().__init__()
        self.app = _app
        self.account_window = _pwin
        
        self.input_field = QLineEdit()
        match form_type:
            case "email":
                self.input_field.setPlaceholderText("Nouvelle adresse e-mail")
            case "password":
                self.input_field.setPlaceholderText("Nouveau mot de passe (au moins 14 caractères)")
                self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            case "username":
                self.input_field.setPlaceholderText("Nouveau nom d'utilisateur (entre 5 et 50 caractères)")
        
        self.submit = QPushButton()
        self.submit.setText("Changer")
        match form_type:
            case "email":
                self.submit.clicked.connect(self._email)
            case "password":
                self.submit.clicked.connect(self._password)
            case "username":
                self.submit.clicked.connect(self._username)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.submit)
        
        self.setLayout(main_layout)
    
    def _email(self):
        inp: str = self.input_field.text()
        if not query_manager.valid_email(inp):
            QMessageBox.critical(self, "Erreur", "Entrez une adresse e-mail valide ! (ex: toto@gmail.com)", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return 

        try:
            con, cur = query_manager.db_connect()
            cur.execute("UPDATE UTILISATEUR SET email = ? WHERE id = ?;", [inp, self.app.logged_user])
            con.commit()
            query_manager.db_disconnect(con)
    
            QMessageBox.information(self, "E-mail mis à jour", "Votre adresse e-mail a bien été changée !", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            self.account_window.email_label.setText(inp)
            self.close()
        except OperationalError:
            query_manager.query_error(self, "L'adresse e-mail n'a pas pu être mit à jour !")

    def _password(self):
        inp: str = self.input_field.text()
        if len(inp) < 14 or inp.isspace() or inp is None:
            QMessageBox.critical(self, "Erreur", "Vous devez entrer un mot de passe valide ! (Minimum 14 caractères)", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return

        try:
            con, cur = query_manager.db_connect()
            cur.execute("UPDATE UTILISATEUR SET password = ? WHERE id = ?;", [query_manager.passhash(inp), self.app.logged_user])
            con.commit()
            query_manager.db_disconnect(con)

            QMessageBox.information(self, "Mot de passe mis à jour", "Votre mot de passe a bien été changée !", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            self.close()
        except OperationalError:
            query_manager.query_error(self, "Le mot de passe n'a pas pu être mit à jour !")

    def _username(self):
        inp: str = self.input_field.text()
        if inp == "" or inp.isspace() or inp is None or not inp.isalnum() or not 5 <= len(inp) <= 50:
            QMessageBox.critical(self, "Erreur", "Vous devez entrer un nom d'utilisateur correct ! (Alphanumérique uniquement et entre 5–50 caractères inclusif)", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return
        
        try:
            con, cur = query_manager.db_connect()
            cur.execute("SELECT pseudo FROM UTILISATEUR WHERE pseudo = ? LIMIT 1;", [inp])
            userdata = cur.fetchone()
            query_manager.db_disconnect(con)
        except OperationalError:
            query_manager.query_error(self, "Il y a eu un problème lors du changement du nom d'utilisateur !")
            return

        if userdata is not None and userdata != []:
            QMessageBox.critical(self, "Erreur", "Nom d'utilisateur déjà pris ! Veuillez en choisir un autre.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return

        try:
            con, cur = query_manager.db_connect()
            cur.execute("UPDATE UTILISATEUR SET pseudo = ? WHERE id = ?;", [inp, self.app.logged_user])
            con.commit()
            query_manager.db_disconnect(con)

            QMessageBox.information(self, "Nom d'utilisateur mis à jour", "Votre nom d'utilisateur a bien été changé !", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            self.account_window.username_label.setText(inp)
            self.close()
        except OperationalError:
            query_manager.query_error(self, "Le nom d'utilisateur n'a pas pu être mit à jour !")
    
    def closeEvent(self, a0):
        self.account_window.show()



class Account(QWidget):
    def __init__(self, _app: QApplication):
        super().__init__()
        self.app = _app
        userdata: tuple[str, str] | None = None
        
        try:
            con, cur = query_manager.db_connect()
            cur.execute("SELECT pseudo, email FROM UTILISATEUR WHERE id = ?;", [self.app.logged_user])
            userdata = cur.fetchone()
            query_manager.db_disconnect(con)
        except OperationalError:
            query_manager.query_error(self, "Un problème est survenu lors de l'acquisition de vos données.")
            self.close()
        
        # Labels
        self.username_label = QLabel()
        self.username_label.setText(userdata[0])
        self.username_label.setStyleSheet("font-size: 40px; text-align: center; background-color: coral;")

        self.email_label = QLabel()
        self.email_label.setText(userdata[1])
        self.email_label.setStyleSheet("font-size: 15px; text-align: center; color: grey;")

        # Boutons
        self.b_disconnect = QPushButton()
        self.b_disconnect.setText("Se\ndéconnecter")
        self.b_disconnect.clicked.connect(self.user_disconnect)
        
        self.b_chemail = QPushButton()
        self.b_chemail.setText("Changer l'adresse\ne-mail")
        self.b_chemail.clicked.connect(self.change_email)

        self.b_chpassword = QPushButton()
        self.b_chpassword.setText("Changer le\nmot de passe")
        self.b_chpassword.clicked.connect(self.change_password)

        self.b_chuname = QPushButton()
        self.b_chuname.setText("Changer le nom\nd'utilisateur")
        self.b_chuname.clicked.connect(self.change_username)

        self.b_delemail = QPushButton()
        self.b_delemail.setText("Supprimer\nl'adresse e-mail")
        self.b_delemail.setStyleSheet("color: white; background-color: crimson;")
        self.b_delemail.clicked.connect(self.delete_email)
        
        self.b_delscore = QPushButton()
        self.b_delscore.setText("Supprimer tous\nles scores")
        self.b_delscore.setStyleSheet("color: white; background-color: crimson;")
        self.b_delscore.clicked.connect(self.delete_scores)
        
        self.b_delaccount = QPushButton()
        self.b_delaccount.setText("Supprimer\nle compte")
        self.b_delaccount.setStyleSheet("color: white; background-color: crimson;")
        self.b_delaccount.clicked.connect(self.delete_account)
        
        # Layouts
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.b_disconnect)
        hbox1.addWidget(self.b_chemail)
        hbox1.addWidget(self.b_chpassword)
        hbox1.addWidget(self.b_chuname)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.b_delscore)
        hbox2.addWidget(self.b_delemail)
        hbox2.addWidget(self.b_delaccount)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.username_label)
        main_layout.addWidget(self.email_label)
        main_layout.addLayout(hbox1)
        main_layout.addLayout(hbox2)
        
        self.setLayout(main_layout)
    
    
    
    def user_disconnect(self):
        self.app.logged_user = 0
        self.close()
    
    def change_email(self):
        self.new_win = _ChangeForm(self.app, self, "email")
        self.new_win.setWindowTitle("Changer")
        self.new_win.setMinimumSize(500, 100)
        self.new_win.show()
        self.hide()

    def change_password(self):
        self.new_win = _ChangeForm(self.app, self, "password")
        self.new_win.setWindowTitle("Changer")
        self.new_win.setMinimumSize(500, 100)
        self.new_win.show()
        self.hide()

    def change_username(self):
        self.new_win = _ChangeForm(self.app, self, "username")
        self.new_win.setWindowTitle("Changer")
        self.new_win.setMinimumSize(500, 100)
        self.new_win.show()
        self.hide()
    
    def delete_email(self):
        result = QMessageBox.warning(self, "Confirmation", "Êtes-vous sûr de vouloir supprimer votre adresse e-mail ? (Cela ne supprimera pas votre compte)", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            del_email(self)

    def delete_scores(self):
        result = QMessageBox.warning(self, "Confirmation", "Êtes-vous sûr de vouloir supprimer tous vos scores ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            del_score(self, True)

    def delete_account(self):
        result = QMessageBox.warning(self, "Confirmation", "Êtes-vous sûr de vouloir supprimer votre compte ? (Cela supprimera aussi tous vos scores !)", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            del_score(self, False)
            del_user(self, True)
            self.close()
    
    def closeEvent(self, a0):
        self.app.submenu_open = False