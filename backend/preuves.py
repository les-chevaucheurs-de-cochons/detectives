# preuve.py
from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Preuve:
    """Modèle représentant une preuve dans une enquête.

    Attributs principaux
    --------------------
    id_preuve  : identifiant auto-incrémenté dans la base (PK)
    type       : type de la preuve (ADN, témoignage, vidéo, arme, ...)
    description: description libre de la preuve
    date       : date à laquelle la preuve a été recueillie
    lieu       : lieu où la preuve a été trouvée
    id_affaire : identifiant de l'affaire (FK, obligatoire)
    id_suspect : identifiant du suspect lié (FK, optionnelle)
    """

    id_preuve: Optional[int]
    type: str
    id_affaire: int
    description: Optional[str] = None
    date: Optional[str] = None
    lieu: Optional[str] = None
    id_suspect: Optional[int] = None

    TABLE_NAME = "Preuve"

    # ----------------------
    # Méthodes utilitaires
    # ----------------------
    def to_dict(self) -> dict:
        """Retourne un dict prêt à être inséré/maj en base."""
        return {
            "type": self.type,
            "description": self.description,
            "date": self.date,
            "lieu": self.lieu,
            "id_affaire": self.id_affaire,
            "id_suspect": self.id_suspect,
        }

    @classmethod
    def from_row(cls, row: tuple) -> "Preuve":
        """Construit une instance de Preuve à partir d'une ligne SQL.

        Ordre attendu:
        (id_preuve, type, description, date, lieu, id_affaire, id_suspect)
        """
        if row is None:
            raise ValueError(
                "Impossible de construire une Preuve à partir d'une ligne vide."
            )
        return cls(
            id_preuve=row[0],
            type=row[1],
            description=row[2],
            date=row[3],
            lieu=row[4],
            id_affaire=row[5],
            id_suspect=row[6],
        )

    # ----------------------
    # CRUD au niveau classe
    # ----------------------
    @classmethod
    def get(cls, id_preuve: int) -> Optional["Preuve"]:
        """Récupère une preuve par son ID, ou None si inexistante."""
        row = get_by_id(cls.TABLE_NAME, id_preuve)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Preuve"]:
        """Retourne toutes les preuves sous forme de liste d'objets Preuve."""
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    @classmethod
    def list_for_affaire(cls, id_affaire: int) -> List["Preuve"]:
        """Retourne toutes les preuves associées à une affaire donnée."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Preuve WHERE id_affaire = ?",
            (id_affaire,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls.from_row(r) for r in rows]

    # ----------------------
    # CRUD au niveau instance
    # ----------------------
    def save(self) -> int:
        """Insère ou met à jour la preuve en base.

        - Si id_preuve est None → INSERT et maj de self.id_preuve
        - Sinon                 → UPDATE
        Retourne l'id de la preuve.
        """
        if self.id_preuve is None:
            # Insertion
            self.id_preuve = insert(self.TABLE_NAME, self.to_dict())
        else:
            # Mise à jour
            update(self.TABLE_NAME, self.id_preuve, self.to_dict())
        return self.id_preuve

    def delete(self) -> None:
        """Supprime la preuve de la base (si elle y est)."""
        if self.id_preuve is not None:
            delete(self.TABLE_NAME, self.id_preuve)
            self.id_preuve = None
