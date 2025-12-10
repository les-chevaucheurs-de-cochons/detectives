# suspect.py
from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Suspect:
    """
    Représente un suspect.
    """
    id_suspect: Optional[int]
    nom: str
    prenom: str
    age: Optional[int] = None
    adresse: Optional[str] = None
    description: Optional[str] = None

    TABLE_NAME = "Suspect"

    # -------- utilitaire --------
    def to_dict(self) -> dict:
        return {
            "nom": self.nom,
            "prénom": self.prenom,   # même nom de colonne que dans la DB
            "âge": self.age,
            "adresse": self.adresse,
            "description": self.description,
        }

    @classmethod
    def from_row(cls, row: tuple) -> "Suspect":
        # ordre = (id_suspect, nom, prénom, âge, adresse, description)
        if row is None:
            raise ValueError("Ligne SQL vide pour Suspect")
        return cls(
            id_suspect=row[0],
            nom=row[1],
            prenom=row[2],
            age=row[3],
            adresse=row[4],
            description=row[5],
        )

    # -------- CRUD orienté classe --------
    @classmethod
    def create(
            cls,
            nom: str,
            prenom: str,
            age: Optional[int] = None,
            adresse: Optional[str] = None,
            description: Optional[str] = None,
    ) -> "Suspect":
        data = {
            "nom": nom,
            "prénom": prenom,
            "âge": age,
            "adresse": adresse,
            "description": description,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(
            id_suspect=new_id,
            nom=nom,
            prenom=prenom,
            age=age,
            adresse=adresse,
            description=description,
        )

    @classmethod
    def get(cls, id_suspect: int) -> Optional["Suspect"]:
        row = get_by_id(cls.TABLE_NAME, id_suspect)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Suspect"]:
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    # -------- Association suspect → affaire + liste des suspects d'une affaire --------
    @classmethod
    def list_for_affaire(cls, id_affaire: int) -> List["Suspect"]:
        """
        Lister les suspects d'une affaire.
        Association faite via la table Preuve (id_affaire + id_suspect).
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT s.*
            FROM Suspect s
                     JOIN Preuve p ON p.id_suspect = s.id_suspect
            WHERE p.id_affaire = ?
            """,
            (id_affaire,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls.from_row(r) for r in rows]

    # -------- CRUD orienté instance --------
    def update(self, **kwargs) -> None:
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        update(self.TABLE_NAME, self.id_suspect, self.to_dict())

    def delete(self) -> None:
        if self.id_suspect is not None:
            delete(self.TABLE_NAME, self.id_suspect)
            self.id_suspect = None
