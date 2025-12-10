from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete


@dataclass
class Suspect:
    """
    Modèle représentant un suspect.

    Attributs
    ---------
    id_suspect : identifiant unique (PK auto-incrémenté)
    nom        : nom de famille
    prenom     : prénom
    age        : âge (optionnel)
    adresse    : adresse du suspect (optionnelle)
    description: description physique / comportementale (optionnelle)
    """

    id_suspect: Optional[int]
    nom: str
    prenom: str
    age: Optional[int] = None
    adresse: Optional[str] = None
    description: Optional[str] = None

    TABLE_NAME = "Suspect"

    # ----------------------
    # Utilitaires
    # ----------------------
    def to_dict(self) -> dict:
        """Transforme l'objet en dict prêt pour la BDD."""
        return {
            "nom": self.nom,
            "prénom": self.prenom,   # attention : colonne avec accent en BDD
            "âge": self.age,         # idem ici
            "adresse": self.adresse,
            "description": self.description,
        }

    @classmethod
    def from_row(cls, row: tuple) -> "Suspect":
        """Construit un Suspect à partir d'une ligne SQL.

        Ordre attendu :
        (id_suspect, nom, prénom, âge, adresse, description)
        """
        if row is None:
            raise ValueError(
                "Impossible de construire un Suspect à partir d'une ligne vide."
            )

        return cls(
            id_suspect=row[0],
            nom=row[1],
            prenom=row[2],
            age=row[3],
            adresse=row[4],
            description=row[5],
        )

    # ----------------------
    # CRUD côté classe
    # ----------------------
    @classmethod
    def get(cls, id_suspect: int) -> Optional["Suspect"]:
        """Récupère un suspect par son ID."""
        row = get_by_id(cls.TABLE_NAME, id_suspect)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Suspect"]:
        """Retourne tous les suspects."""
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    # ----------------------
    # CRUD côté instance
    # ----------------------
    def save(self) -> int:
        """Insère ou met à jour le suspect.

        - Si id_suspect est None -> INSERT
        - Sinon                   -> UPDATE
        """
        if self.id_suspect is None:
            self.id_suspect = insert(self.TABLE_NAME, self.to_dict())
        else:
            update(self.TABLE_NAME, self.id_suspect, self.to_dict())
        return self.id_suspect

    def delete(self) -> None:
        """Supprime le suspect de la base."""
        if self.id_suspect is not None:
            delete(self.TABLE_NAME, self.id_suspect)
            self.id_suspect = None
