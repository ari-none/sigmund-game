-- --- --
-- Script pour la création de la base de données du jeu Sigmund --
-- --
-- --- --


-- ---------------------- --
-- Base de données: Simon --
-- ---------------------- --
DROP DATABASE IF EXISTS Simon;
CREATE DATABASE Simon;
USE Simon;


-- ------------------ --
-- Table: UTILISATEUR --
-- ------------------ --
CREATE TABLE UTILISATEUR (
        id INT NOT NULL,
        pseudo VARCHAR(50) NOT NULL,
        password CHAR(64) NOT NULL,
        email VARCHAR(50),
        CONSTRAINT UTILISATEUR_PK PRIMARY KEY (id),
        CONSTRAINT id_UNQ UNIQUE (id),
        CONSTRAINT pseudo_UNQ UNIQUE (pseudo),
        CONSTRAINT email_UNQ UNIQUE (email)
)ENGINE=InnoDB;


-- ------------- --
-- Table: PARTIE --
-- ------------- --
CREATE TABLE PARTIE (
        id INT NOT NULL,
        sequence VARCHAR(255) NOT NULL,
        temps TIME NOT NULL,
        id_utilisateur INT NOT NULL,
        CONSTRAINT PARTIE_PK PRIMARY KEY (id),
        CONSTRAINT id_UNQ UNIQUE (id),
        CONSTRAINT id_utilisateur_UNQ UNIQUE (id_utilisateur),
        CONSTRAINT PARTIE_id_utilisateur_FK FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR (id)
)ENGINE=InnoDB;