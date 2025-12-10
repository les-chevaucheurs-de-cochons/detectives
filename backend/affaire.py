from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete


@dataclass
class Affaire:
    """
    Modèle représentant une affaire criminelle.

    Attributs
    ---------
    id_affaire  : identifiant unique de l'affaire (PK, auto-incrémenté)
    titre       : titre ou nom de l'affaire
    date        : date d'ouverture / d'enregistrement de l'affaire
    lieu        : lieu principal de l'affaire
    statut      : état de l'affaire (ouverte, en cours, résolue, classée...)
    description : description détaillée (optionnelle)
    """

    id_affaire: Optional[int]
    titre: str
    date: str
    lieu: str
    statut: str
    description: Optional[str] = None

    TABLE_NAME = "Affaire"

    # ----------------------
    # Méthodes utilitaires
    # ----------------------
    def to_dict(self) -> dict:
        """Transforme l'objet en dict prêt pour la base de données."""
        return {
            "titre": self.titre,
            "date": self.date,
            "lieu": self.lieu,
            "statut": self.statut,
            "description": self.description,
        }

    @classmethod
    def from_row(cls, row: tuple) -> "Affaire":
        """Construit une Affaire à partir d'une ligne SQL.

        Ordre attendu :
        (id_affaire, titre, description, date, lieu, statut)
        """
        if row is None:
            raise ValueError(
                "Impossible de construire une Affaire à partir d'une ligne vide."
            )

        return cls(
            id_affaire=row[0],
            titre=row[1],
            description=row[2],
            date=row[3],
            lieu=row[4],
            statut=row[5],
        )

    # ----------------------
    # CRUD au niveau classe
    # ----------------------
    @classmethod
    def get(cls, id_affaire: int) -> Optional["Affaire"]:
        """Récupère une affaire par son ID."""
        row = get_by_id(cls.TABLE_NAME, id_affaire)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Affaire"]:
        """Retourne toutes les affaires."""
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    # ----------------------
    # CRUD au niveau instance
    # ----------------------
    def save(self) -> int:
        """Insère ou met à jour l'affaire dans la base.

        - Si id_affaire est None -> INSERT
        - Sinon                   -> UPDATE
        Retourne l'id de l'affaire.
        """
        if self.id_affaire is None:
            self.id_affaire = insert(self.TABLE_NAME, self.to_dict())
        else:
            update(self.TABLE_NAME, self.id_affaire, self.to_dict())
        return self.id_affaire

    def delete(self) -> None:
        """Supprime l'affaire de la base."""
        if self.id_affaire is not None:
            delete(self.TABLE_NAME, self.id_affaire)
            self.id_affaire = None
