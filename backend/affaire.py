# affaire.py
from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Affaire:

    id_affaire: Optional[int]
    titre: str
    date: str
    lieu: str
    statut: str
    description: Optional[str] = None

    TABLE_NAME = "Affaire"

    # --------------------------------------------------------
    # Conversion objet → dict
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "titre": self.titre,
            "date": self.date,
            "lieu": self.lieu,
            "statut": self.statut,
            "description": self.description,
        }

    # --------------------------------------------------------
    # Propriétés
    # --------------------------------------------------------
    @property
    def id(self):
        return self.id_affaire

    @property
    def uid(self):
        return f"A{self.id_affaire}"

    # --------------------------------------------------------
    # Construction objet depuis une ligne SQL (6 colonnes)
    # --------------------------------------------------------
    @classmethod
    def from_row(cls, row: tuple) -> "Affaire":
        """
        row = (id_affaire, titre, date, lieu, statut, description)
        """
        if row is None:
            raise ValueError("Ligne SQL vide pour Affaire")


        return cls(
            id_affaire=row[0],
            titre=row[1],
            date=row[2],
            lieu=row[3],
            statut=row[4],
            description=row[5],
        )

    # --------------------------------------------------------
    # CRUD : CREATE
    # --------------------------------------------------------
    @classmethod
    def create(
            cls,
            titre: str,
            date: str,
            lieu: str,
            statut: str,
            description: Optional[str] = None,
    ) -> "Affaire":

        data = {
            "titre": titre,
            "date": date,
            "lieu": lieu,
            "statut": statut,
            "description": description,
        }

        new_id = insert(cls.TABLE_NAME, data)

        return cls(
            id_affaire=new_id,
            titre=titre,
            date=date,
            lieu=lieu,
            statut=statut,
            description=description,
        )

    # --------------------------------------------------------
    # CRUD : READ
    # --------------------------------------------------------
    @classmethod
    def get(cls, id_affaire: int) -> Optional["Affaire"]:
        row = get_by_id(cls.TABLE_NAME, id_affaire)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Affaire"]:
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    # --------------------------------------------------------
    # CRUD : UPDATE
    # --------------------------------------------------------
    def save(self) -> None:
        if self.id_affaire is None:
            return
        update(self.TABLE_NAME, self.id_affaire, self.to_dict())

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    # --------------------------------------------------------
    # CRUD : DELETE
    # --------------------------------------------------------
    def delete(self) -> None:
        if self.id_affaire:
            delete(self.TABLE_NAME, self.id_affaire)
            self.id_affaire = None

    # --------------------------------------------------------
    # Liaisons
    # --------------------------------------------------------
    def get_preuves(self):
        from backend.preuves import Preuve
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Preuve WHERE id_affaire = ?", (self.id_affaire,))
        rows = cursor.fetchall()
        conn.close()
        return [Preuve.from_row(r) for r in rows]

    def get_armes(self):
        from backend.arme import Arme
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Arme WHERE id_affaire = ?", (self.id_affaire,))
        rows = cursor.fetchall()
        conn.close()
        return [Arme.from_row(r) for r in rows]

    def get_lieux(self):
        from backend.lieu import Lieu
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Lieu WHERE id_affaire = ?", (self.id_affaire,))
        rows = cursor.fetchall()
        conn.close()
        return [Lieu.from_row(r) for r in rows]

    def get_suspects(self):
        from backend.suspect import Suspect
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT DISTINCT s.*
                       FROM Suspect s
                                JOIN Preuve p ON p.id_suspect = s.id_suspect
                       WHERE p.id_affaire = ?
                       """, (self.id_affaire,))
        rows = cursor.fetchall()
        conn.close()
        return [Suspect.from_row(r) for r in rows]
