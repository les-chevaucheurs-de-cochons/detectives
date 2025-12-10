# arme.py
from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Arme:
    """
    Représente une arme liée à une affaire.
    """
    id_arme: Optional[int]
    type: str
    id_affaire: int
    description: Optional[str] = None
    numero_serie: Optional[str] = None

    TABLE_NAME = "Arme"

    # -------- utilitaire --------
    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "description": self.description,
            "numéro_série": self.numero_serie,  # nom exact de la colonne
            "id_affaire": self.id_affaire,
        }

    @classmethod
    def from_row(cls, row: tuple) -> "Arme":
        # ordre = (id_arme, type, description, numéro_série, id_affaire)
        if row is None:
            raise ValueError("Ligne SQL vide pour Arme")
        return cls(
            id_arme=row[0],
            type=row[1],
            description=row[2],
            numero_serie=row[3],
            id_affaire=row[4],
        )

    # -------- CRUD orienté classe --------
    @classmethod
    def create(
            cls,
            type: str,
            id_affaire: int,
            description: Optional[str] = None,
            numero_serie: Optional[str] = None,
    ) -> "Arme":
        data = {
            "type": type,
            "description": description,
            "numéro_série": numero_serie,
            "id_affaire": id_affaire,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(
            id_arme=new_id,
            type=type,
            description=description,
            numero_serie=numero_serie,
            id_affaire=id_affaire,
        )

    @classmethod
    def get(cls, id_arme: int) -> Optional["Arme"]:
        row = get_by_id(cls.TABLE_NAME, id_arme)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Arme"]:
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    # -------- Association arme → affaire + liste des armes d'une affaire --------
    @classmethod
    def list_for_affaire(cls, id_affaire: int) -> List["Arme"]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Arme WHERE id_affaire = ?",
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
        update(self.TABLE_NAME, self.id_arme, self.to_dict())

    def delete(self) -> None:
        if self.id_arme is not None:
            delete(self.TABLE_NAME, self.id_arme)
            self.id_arme = None
