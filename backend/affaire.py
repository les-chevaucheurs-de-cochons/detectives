# affaire.py
from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Affaire:
    """
    Modèle objet représentant une affaire.
    Inclut les coordonnées pos_x / pos_y pour l'affichage dans la GUI.
    """

    id_affaire: Optional[int]
    titre: str
    date: str
    lieu: str
    statut: str
    description: Optional[str] = None

    # --- POUR LE MUR VISUEL (FBI Board) ---
    pos_x: int = 40
    pos_y: int = 40

    TABLE_NAME = "Affaire"

    # --------------------------------------------------------
    # Conversion objet → dict (pour update SQL)
    # --------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "titre": self.titre,
            "date": self.date,
            "lieu": self.lieu,
            "statut": self.statut,
            "description": self.description,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    # --------------------------------------------------------
    # Construction objet depuis une ligne SQL
    # --------------------------------------------------------
    @property
    def id(self):
        return self.id_affaire

    @property
    def uid(self):
        return f"A{self.id_affaire}"



    @classmethod
    def from_row(cls, row: tuple) -> "Affaire":
        """
        row = (id_affaire, titre, date, lieu, statut, description, pos_x, pos_y)
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
            pos_x=row[6],
            pos_y=row[7],
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
            pos_x: int = 40,
            pos_y: int = 40,
    ) -> "Affaire":

        data = {
            "titre": titre,
            "date": date,
            "lieu": lieu,
            "statut": statut,
            "description": description,
            "pos_x": pos_x,
            "pos_y": pos_y,
        }

        new_id = insert(cls.TABLE_NAME, data)

        return cls(
            id_affaire=new_id,
            titre=titre,
            date=date,
            lieu=lieu,
            statut=statut,
            description=description,
            pos_x=pos_x,
            pos_y=pos_y,
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
    # CRUD : UPDATE (instance)
    # --------------------------------------------------------
    def save(self) -> None:
        """
        Persiste l'objet entier dans la DB (pos_x/pos_y compris).
        Equivalent de update().
        """
        if self.id_affaire is None:
            return  # sécurité

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
    # Liaisons avec d'autres entités
    # --------------------------------------------------------
    def get_preuves(self):
        from preuve import Preuve
        return Preuve.list_for_affaire(self.id_affaire)

    def get_armes(self):
        from arme import Arme
        return Arme.list_for_affaire(self.id_affaire)

    def get_lieux(self):
        from lieu import Lieu
        return Lieu.list_for_affaire(self.id_affaire)

    def get_suspects(self):
        from suspect import Suspect

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
