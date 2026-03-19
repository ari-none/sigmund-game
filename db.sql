-- ------------------------------------------------------------ --
-- Script pour la création de la base de données du jeu Sigmund --
-- Pensez à bien lire le REDME.md !                             --
-- ------------------------------------------------------------ --


-- ----------------------------
-- Table: UTILISATEUR
-- ----------------------------
CREATE TABLE UTILISATEUR (
  id INT NOT NULL,
  pseudo VARCHAR(50) NOT NULL,
  password CHAR(64) NOT NULL,
  email VARCHAR(50),
  nb_credits INT NOT NULL,
  CONSTRAINT UTILISATEUR_PK PRIMARY KEY (id),
  CONSTRAINT id_UNQ UNIQUE (id),
  CONSTRAINT pseudo_UNQ UNIQUE (pseudo),
  CONSTRAINT email_UNQ UNIQUE (email)
)ENGINE=InnoDB;


-- ----------------------------
-- Table: PACKS
-- ----------------------------
CREATE TABLE PACKS (
  id INT NOT NULL AUTO_INCREMENT,
  libelle VARCHAR(50) NOT NULL,
  qte_credits INT NOT NULL,
  prix DECIMAL(5,2) NOT NULL,
  CONSTRAINT PACKS_PK PRIMARY KEY (id)
)ENGINE=InnoDB;


-- ----------------------------
-- Table: PARTIE
-- ----------------------------
CREATE TABLE PARTIE (
  id INT NOT NULL,
  sequence VARCHAR(255) NOT NULL,
  temps DECIMAL(10,3) NOT NULL,
  id_UTILISATEUR INT NOT NULL,
  CONSTRAINT PARTIE_PK PRIMARY KEY (id),
  CONSTRAINT id_UNQ UNIQUE (id),
  CONSTRAINT id_UTILISATEUR_UNQ UNIQUE (id_UTILISATEUR),
  CONSTRAINT PARTIE_id_UTILISATEUR_FK FOREIGN KEY (id_UTILISATEUR) REFERENCES UTILISATEUR (id)
)ENGINE=InnoDB;


-- ----------------------------
-- Table: ACHAT
-- ----------------------------
CREATE TABLE ACHAT (
  id INT NOT NULL AUTO_INCREMENT,
  date DATETIME NOT NULL,
  id_UTILISATEUR INT NOT NULL,
  id_PACKS INT NOT NULL,
  CONSTRAINT ACHAT_PK PRIMARY KEY (id),
  CONSTRAINT id_UTILISATEUR_UNQ UNIQUE (id_UTILISATEUR),
  CONSTRAINT ACHAT_id_UTILISATEUR_FK FOREIGN KEY (id_UTILISATEUR) REFERENCES UTILISATEUR (id),
  CONSTRAINT ACHAT_id_PACKS_FK FOREIGN KEY (id_PACKS) REFERENCES PACKS (id)
)ENGINE=InnoDB;