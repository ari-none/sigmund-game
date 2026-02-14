from functools import partial

from mariadb import OperationalError
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer

import query_manager

def add_score_to_list(scorewindow: QWidget, pseudo: str, sequence: str, time: str, header: bool=False) -> None:
    """
    Fonction pour ajouter un score à une liste.
    :param scorelist: La liste des scores (normalement self.list)
    :param pseudo: Le pseudo du joueur
    :param sequence: La séquence (ou un string litéral si header = True)
    :param time: Le temps (à convertir en string d'habord)
    :param header: (Optionel) Si le "score" doit être considéré comme un header (donc un string litéral)
    :return:
    """
    item = QListWidgetItem()
    item.setFlags(Qt.ItemFlag.ItemIsEnabled)

    row_widget = QWidget()
    row_layout = QHBoxLayout(row_widget)
    row_layout.setContentsMargins(5, 2, 5, 2)

    p_label = QLabel(pseudo)
    p_label.setMinimumWidth(120)
    row_layout.addWidget(p_label)
    
    s_label = QLabel(sequence if header else str(len(sequence)))
    s_label.setMinimumWidth(80)
    row_layout.addWidget(s_label)
    
    t_label = QLabel(time)
    t_label.setMinimumWidth(80)
    row_layout.addWidget(t_label)
    
    row_layout.addStretch()
    
    if not header:
        button = QPushButton("Jouer")
        button.clicked.connect(partial(scorewindow.play_press, pseudo, sequence))
        row_layout.addWidget(button)
    
    item.setSizeHint(row_widget.sizeHint())
    scorewindow.list.addItem(item)
    scorewindow.list.setItemWidget(item, row_widget)

class HighScore(QWidget):
    def __init__(self, _app: QApplication, _pwin: QWidget):
        super().__init__()
        self.app = _app
        self.main_window = _pwin
        
        self.scoredata: list[tuple[str, str, float]] = None
        try:
            con, cur = query_manager.db_connect()
            cur.execute("SELECT pseudo, sequence, temps FROM PARTIE INNER JOIN UTILISATEUR ON PARTIE.id_utilisateur = UTILISATEUR.id ORDER BY LENGTH(sequence) DESC, pseudo, temps LIMIT 150;")
            self.scoredata = cur.fetchall()
            query_manager.db_disconnect(con)
        except OperationalError:
            query_manager.query_error(self, "Il y a eu un problème lors du chargement des scores !")
            QTimer.singleShot(5, self.close)
            return
        
        self.list = QListWidget()
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list)
        self.setLayout(main_layout)

        add_score_to_list(self, "—JOUEUR—", "—SCORE—", "—TEMPS—", True)
        for gpseudo, gsequence, gtime in self.scoredata:
            add_score_to_list(self, gpseudo, gsequence, str(gtime))
    
    def play_press(self, pseudo: str, sequence: str):
        self.app.submenu_open = False # Requis pour que la fonction b_play_press marche avant d'être appelé
        QTimer.singleShot(5, self.close)
        self.main_window.b_play_press((sequence, pseudo))
        self.deleteLater()
    
    def closeEvent(self, a0):
        self.app.submenu_open = False