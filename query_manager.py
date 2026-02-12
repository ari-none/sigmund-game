from os import getenv
import mariadb
import dotenv
import hashlib
import re

# Charger le fichier d'environnement, qui sera utilisé pour stocker les identifiants & l'IP
# de la base de données (dans le cas où on veut utiliser le programme avec une autre base).
dotenv.load_dotenv(".env")

conn_params = {
    "user": getenv("DB_USER"),
    "password": getenv("DB_PASSWORD"),
    "host": getenv("DB_HOST"),
    "database": getenv("DB_DATABASE")
}



# Quelques snippets pour faciliter le développement
def passhash(text: str) -> str:
    """
    Alias pour hashlib.sha256(text.encode()).hexdigest()
    :param text: Le texte à hacher
    :return: Le texte haché
    """
    return hashlib.sha256(text.encode()).hexdigest()

def valid_email(email: str) -> bool:
    """
    Vérifie si le string est une adresse e-mail.
    :param email: Un string
    :return: Si c'est une adresse email ou pas (par exemple: exemple@domain.net)
    """
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))

def db_connect() -> tuple[mariadb.Connection, mariadb.Cursor]:
    """
    Connection rapide à une base de données
    :return: La connection et son curseur
    """
    _connection = mariadb.connect(**conn_params)
    _cursor = _connection.cursor()
    return _connection, _cursor

def db_disconnect(connection: mariadb.Connection) -> None:
    """
    Déconnection rapide d'une base de données
    :param connection: La connection à la base
    :return: 
    """
    connection.cursor().close()
    connection.close()