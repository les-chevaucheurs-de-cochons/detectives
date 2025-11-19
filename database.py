import sqlite3
from sqlite3 import Connection

# Nom du fichier SQLite
DB_NAME = "detectives.db"


def get_connection() -> Connection:
    """
    Ouvre une connexion vers la base SQLite.
    Active également les clés étrangères (désactivées par défaut dans SQLite).
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")  # Activation des clés étrangères
    return conn


def init_db():
    """
    Initialise la base de données :
    - Crée toutes les tables si elles n'existent pas encore
    - Définit les PK et FK
    - Garantit l'intégrité référentielle
    """
    conn = get_connection()
    cursor = conn.cursor()

    # --- TABLE Affaire ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Affaire (
                      id_affaire INTEGER PRIMARY KEY AUTOINCREMENT,
                      titre TEXT NOT NULL,
                      date TEXT NOT NULL,
                      lieu TEXT NOT NULL,
                      statut TEXT NOT NULL,
                      description TEXT
                   );
                   """)

    # --- TABLE Suspect ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Suspect (
                      id_suspect INTEGER PRIMARY KEY AUTOINCREMENT,
                      nom TEXT NOT NULL,
                      prénom TEXT NOT NULL,
                      âge INTEGER,
                      adresse TEXT,
                      description TEXT
                   );
                   """)

    # --- TABLE Preuve ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Preuve (
                     id_preuve INTEGER PRIMARY KEY AUTOINCREMENT,
                     type TEXT NOT NULL,
                     description TEXT,
                     date TEXT,
                     lieu TEXT,
                     id_affaire INTEGER NOT NULL,
                     id_suspect INTEGER,
                       -- Liens vers Affaire et Suspect
                       FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE,
                       FOREIGN KEY (id_suspect) REFERENCES Suspect(id_suspect)
                       );
                   """)

    # --- TABLE Arme ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Arme (
                       id_arme INTEGER PRIMARY KEY AUTOINCREMENT,
                       type TEXT NOT NULL,
                       description TEXT,
                       numéro_série TEXT,
                       id_affaire INTEGER NOT NULL,
                       -- L'arme appartient forcément à une affaire
                        FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE
                       );
                   """)

    # --- TABLE Lieu ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Lieu (
                       id_lieu INTEGER PRIMARY KEY AUTOINCREMENT,
                       nom TEXT NOT NULL,
                       adresse TEXT,
                       type TEXT,
                       id_affaire INTEGER NOT NULL,
                       -- Un lieu peut être lié à une affaire
                        FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE
                       );
                   """)

    # --- TABLE Agent ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Agent (
                        id_agent INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        prénom TEXT NOT NULL,
                        grade TEXT,
                        service TEXT
                   );
                   """)

    # --- TABLE Relation ---
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Relation (
                       id_relation INTEGER PRIMARY KEY AUTOINCREMENT,
                       type TEXT NOT NULL,
                       id_entite1 INTEGER NOT NULL,
                       id_entite2 INTEGER NOT NULL,
                       description TEXT
                   );
                   """)

    conn.commit()
    conn.close()
    print("✅ Base SQLite initialisée avec succès !")


# ---------------------------------------------------------------------------
# CRUD GÉNÉRIQUE : fonctions pour simplifier les opérations sur toutes les tables
# ---------------------------------------------------------------------------

def insert(table: str, data: dict) -> int:
    """
    Insère une ligne dans une table.
    - table : nom de la table
    - data : dictionnaire { colonne: valeur }
    Retourne l'ID de la nouvelle entrée.
    """
    conn = get_connection()
    cursor = conn.cursor()

    colonnes = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO {table} ({colonnes}) VALUES ({placeholders})"

    cursor.execute(query, tuple(data.values()))
    conn.commit()

    inserted_id = cursor.lastrowid  # ID auto-incrémenté
    conn.close()

    return inserted_id


def get_all(table: str):
    """
    Récupère toutes les lignes d'une table.
    Retourne une liste de tuples.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_by_id(table: str, row_id: int):
    """
    Récupère une ligne d'une table selon son ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table} WHERE rowid = ?", (row_id,))
    row = cursor.fetchone()

    conn.close()
    return row


def update(table: str, row_id: int, data: dict):
    """
    Met à jour une ligne dans une table.
    - row_id : ID de la ligne à modifier
    - data : dictionnaire { colonne: nouvelle_valeur }
    """
    conn = get_connection()
    cursor = conn.cursor()

    champs = ", ".join([f"{k} = ?" for k in data.keys()])
    valeurs = list(data.values()) + [row_id]

    query = f"UPDATE {table} SET {champs} WHERE rowid = ?"
    cursor.execute(query, valeurs)

    conn.commit()
    conn.close()


def delete(table: str, row_id: int):
    """
    Supprime une entrée dans une table selon son ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table} WHERE rowid = ?", (row_id,))
    conn.commit()

    conn.close()
