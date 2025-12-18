import sqlite3
from sqlite3 import Connection
from typing import Optional

DB_NAME = "detectives.db"


def get_connection() -> Connection:
    conn = sqlite3.connect(DB_NAME)
    # Active les clés étrangères pour chaque connexion
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ============================
    #   TABLE Ville
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Ville (
                                                        code_postal TEXT PRIMARY KEY,
                                                        nom TEXT NOT NULL
                   );
                   """)



    # ============================
    #   TABLE Affaire
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Affaire (
                                                          id_affaire INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          titre TEXT NOT NULL,
                                                          date TEXT NOT NULL,
                                                          lieu TEXT NOT NULL,
                                                          code_postal TEXT,
                                                          statut TEXT NOT NULL,
                                                          description TEXT,
                                                          pos_x INTEGER DEFAULT 40,
                                                          pos_y INTEGER DEFAULT 40
                   );
                   """)

    # ============================
    #   TABLE Suspect
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Suspect (
                                                          id_suspect INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          nom TEXT NOT NULL,
                                                          prenom TEXT NOT NULL,
                                                          age INTEGER,
                                                          adresse TEXT,
                                                          description TEXT,
                                                          casier INTEGER DEFAULT 0,
                                                          pos_x INTEGER DEFAULT 80,
                                                          pos_y INTEGER DEFAULT 80
                   );
                   """)


    # ============================
    #   TABLE Preuve
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Preuve (
                                                         id_preuve INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         type TEXT NOT NULL,
                                                         description TEXT,
                                                         date TEXT,
                                                         lieu TEXT,
                                                         id_affaire INTEGER NOT NULL,
                                                         id_suspect INTEGER,
                                                         pos_x INTEGER DEFAULT 120,
                                                         pos_y INTEGER DEFAULT 120,
                                                         FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE,
                       FOREIGN KEY (id_suspect) REFERENCES Suspect(id_suspect)
                       );
                   """)

    # ============================
    #   TABLE Arme
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Arme (
                                                       id_arme INTEGER PRIMARY KEY AUTOINCREMENT,
                                                       type TEXT NOT NULL,
                                                       description TEXT,
                                                       numero_serie TEXT,
                                                       id_affaire INTEGER NOT NULL,
                                                       pos_x INTEGER DEFAULT 160,
                                                       pos_y INTEGER DEFAULT 160,
                                                       FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE
                       );
                   """)

    # ============================
    #   TABLE Lieu
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Lieu (
                                                       id_lieu INTEGER PRIMARY KEY AUTOINCREMENT,
                                                       nom TEXT NOT NULL,
                                                       adresse TEXT,
                                                       type TEXT,
                                                       id_affaire INTEGER NOT NULL,
                                                       pos_x INTEGER DEFAULT 200,
                                                       pos_y INTEGER DEFAULT 200,
                                                       FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE
                       );
                   """)

    # ============================
    #   TABLE Agent
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Agent (
                                                        id_agent INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        identifiant TEXT NOT NULL UNIQUE,
                                                        password TEXT NOT NULL
                   );
                   """)


    # ============================
    #   TABLE AffaireSuspect (N-N)
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS AffaireSuspect (
                                                                 id_affaire INTEGER NOT NULL,
                                                                 id_suspect INTEGER NOT NULL,
                                                                 PRIMARY KEY (id_affaire, id_suspect),
                       FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE,
                       FOREIGN KEY (id_suspect) REFERENCES Suspect(id_suspect) ON DELETE CASCADE
                       );
                   """)

    # ============================
    #   TABLE AffaireArme (N-N)
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS AffaireArme (
                                                              id_affaire INTEGER NOT NULL,
                                                              id_arme INTEGER NOT NULL,
                                                              PRIMARY KEY (id_affaire, id_arme),
                       FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE,
                       FOREIGN KEY (id_arme) REFERENCES Arme(id_arme) ON DELETE CASCADE
                       );
                   """)

    # ============================
    #   TABLE AffaireLieu (N-N)
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS AffaireLieu (
                                                              id_affaire INTEGER NOT NULL,
                                                              id_lieu INTEGER NOT NULL,
                                                              PRIMARY KEY (id_affaire, id_lieu),
                       FOREIGN KEY (id_affaire) REFERENCES Affaire(id_affaire) ON DELETE CASCADE,
                       FOREIGN KEY (id_lieu) REFERENCES Lieu(id_lieu) ON DELETE CASCADE
                       );
                   """)



    conn.commit()
    conn.close()
    print("✅ Base SQLite initialisée avec succès !")


# ---------------------------------------------------------------------------
# CRUD GÉNÉRIQUE
# ---------------------------------------------------------------------------

def insert(table: str, data) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cols = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

    cursor.execute(query, tuple(data.values()))
    conn.commit()

    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id


def get_all(table: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_by_id(table: str, row_id: int, pk: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()

    if pk is None:
        pk = f"id_{table.lower()}"

    cursor.execute(f"SELECT * FROM {table} WHERE {pk} = ?", (row_id,))
    row = cursor.fetchone()

    conn.close()
    return row


def update(table: str, row_id: int, data, pk: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()

    if pk is None:
        pk = f"id_{table.lower()}"

    champs = ", ".join([f"{k} = ?" for k in data.keys()])
    values = list(data.values()) + [row_id]

    query = f"UPDATE {table} SET {champs} WHERE {pk} = ?"
    cursor.execute(query, values)

    conn.commit()
    conn.close()


def delete(table: str, row_id: int, pk: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()

    if pk is None:
        pk = f"id_{table.lower()}"

    cursor.execute(f"DELETE FROM {table} WHERE {pk} = ?", (row_id,))
    conn.commit()

    conn.close()
