import sqlite3
from sqlite3 import Connection

DB_NAME = "detectives.db"


def get_connection() -> Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # ============================
    #   TABLE Affaire
    # ============================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Affaire (
                                                          id_affaire INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          titre TEXT NOT NULL,
                                                          date TEXT NOT NULL,
                                                          lieu TEXT NOT NULL,
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
                                                        nom TEXT NOT NULL,
                                                        prenom TEXT NOT NULL,
                                                        grade TEXT,
                                                        service TEXT
                   );
                   """)

    # ============================
    #   TABLE Relation
    # ============================
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
# CRUD GÉNÉRIQUE
# ---------------------------------------------------------------------------
def insert(table: str, data: dict) -> int:
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


def get_by_id(table: str, row_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table} WHERE rowid = ?", (row_id,))
    row = cursor.fetchone()

    conn.close()
    return row


def update(table: str, row_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    champs = ", ".join([f"{k} = ?" for k in data.keys()])
    values = list(data.values()) + [row_id]

    query = f"UPDATE {table} SET {champs} WHERE rowid = ?"
    cursor.execute(query, values)

    conn.commit()
    conn.close()


def delete(table: str, row_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {table} WHERE rowid = ?", (row_id,))
    conn.commit()

    conn.close()
