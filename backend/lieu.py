from dataclasses import dataclass
from typing import Optional, List, Tuple

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Lieu:
    """
    Modèle représentant un lieu lié à une affaire.

    Attributs
    ---------
    id_lieu   : identifiant unique du lieu (PK auto-incrémenté)
    nom       : nom du lieu (ex: 'Banque centrale', 'Parc du Cinquantenaire')
    adresse   : adresse du lieu (optionnelle)
    type      : type de lieu (domicile, scène de crime, planque, ...)
    id_affaire: identifiant de l'affaire liée (FK, obligatoire)
    """

    id_lieu: Optional[int]
    nom: str
    id_affaire: int
    adresse: Optional[str] = None
    type: Optional[str] = None

    TABLE_NAME = "Lieu"

    # ----------------------
    # Utilitaires
    # ----------------------
    def to_dict(self) -> dict:
        """Transforme l'objet en dict prêt pour la base de données."""
        return {
            "nom": self.nom,
            "adresse": self.adresse,
            "type": self.type,
            "id_affaire": self.id_affaire,
        }

    @classmethod
    def from_row(cls, row: tuple) -> "Lieu":
        """
        Construit un Lieu à partir d'une ligne SQL.

        Ordre attendu :
        (id_lieu, nom, adresse, type, id_affaire)
        """
        if row is None:
            raise ValueError("Ligne SQL vide pour Lieu")

        return cls(
            id_lieu=row[0],
            nom=row[1],
            adresse=row[2],
            type=row[3],
            id_affaire=row[4],
        )

    # ----------------------
    # CRUD orienté classe
    # ----------------------
    @classmethod
    def create(
            cls,
            nom: str,
            id_affaire: int,
            adresse: Optional[str] = None,
            type: Optional[str] = None,
    ) -> "Lieu":
        """Création d'un lieu (create() dans l'issue)."""
        data = {
            "nom": nom,
            "adresse": adresse,
            "type": type,
            "id_affaire": id_affaire,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(
            id_lieu=new_id,
            nom=nom,
            adresse=adresse,
            type=type,
            id_affaire=id_affaire,
        )

    @classmethod
    def get(cls, id_lieu: int) -> Optional["Lieu"]:
        row = get_by_id(cls.TABLE_NAME, id_lieu)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Lieu"]:
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    @classmethod
    def list_for_affaire(cls, id_affaire: int) -> List["Lieu"]:
        """Lister les lieux d'une affaire (FK id_affaire)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Lieu WHERE id_affaire = ?",
            (id_affaire,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [cls.from_row(r) for r in rows]

    # ----------------------
    # Lister les affaires par lieux
    # ----------------------
    @classmethod
    def list_affaires_par_lieux(cls) -> List[Tuple["Lieu", "Affaire"]]:
        """
        Retourne une liste de couples (Lieu, Affaire) pour
        pouvoir afficher facilement "les affaires par lieux".

        Exemple d’utilisation :
            for lieu, affaire in Lieu.list_affaires_par_lieux():
                print(lieu.nom, '->', affaire.titre)
        """
        from affaire import Affaire  # import local pour éviter les imports circulaires

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT l.*, a.*
                       FROM Lieu l
                                JOIN Affaire a ON l.id_affaire = a.id_affaire
                       """)
        rows = cursor.fetchall()
        conn.close()

        result: List[Tuple[Lieu, Affaire]] = []
        for row in rows:
            lieu_row = row[:5]      # Lieu a 5 colonnes
            affaire_row = row[5:11] # Affaire en a 6

            lieu = cls.from_row(lieu_row)
            affaire = Affaire.from_row(affaire_row)
            result.append((lieu, affaire))

        return result

    # ----------------------
    # CRUD orienté instance
    # ----------------------
    def update(self, **kwargs) -> None:
        """Met à jour le lieu avec les valeurs données."""
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        update(self.TABLE_NAME, self.id_lieu, self.to_dict())

    def delete(self) -> None:
        """Supprime le lieu de la base."""
        if self.id_lieu is not None:
            delete(self.TABLE_NAME, self.id_lieu)
            self.id_lieu = None

    # ----------------------
    # Lien vers l'affaire
    # ----------------------
    def get_affaire(self):
        """Retourne l'affaire liée à ce lieu."""
        from affaire import Affaire
        return Affaire.get(self.id_affaire)
