from PyQt5.QtWidgets import *

class Account(QWidget):
    def __init__(self, _app:QApplication):
        super().__init__()
        self.app = _app

    def closeEvent(self, a0):
        self.app.submenu_open = False
        self.setWindowTitle("Modifier le mot de passe")
        self.setGeometry(600, 300, 300, 200)

        # Champs de texte
        self.label_info = QLabel("Entrez votre nouveau mot de passe :")

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Nouveau mot de passe")
        self.new_password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_password.setEchoMode(QLineEdit.Password)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.change_password)

        # Layouts & fenêtre
        layout = QVBoxLayout()
        layout.addWidget(self.label_info)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm_password)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def change_password(self):
        if self.new_password.text() == self.confirm_password.text():
            QMessageBox.information(self, "Succès", "Mot de passe modifié avec succès ")
            self.close()
        else:
            QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas ")