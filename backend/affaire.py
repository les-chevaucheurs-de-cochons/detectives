# affaire.py
from dataclasses import dataclass
from typing import Optional, List

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Affaire:
    """
    Représente une affaire et ses interactions avec la DB.
    """
    id_affaire: Optional[int]
    titre: str
    date: str
    lieu: str
    statut: str
    description: Optional[str] = None

    TABLE_NAME = "Affaire"

    # -------- utilitaire --------
    def to_dict(self) -> dict:
        return {
            "titre": self.titre,
            "date": self.date,
            "lieu": self.lieu,
            "statut": self.statut,
            "description": self.description,
        }

    @classmethod
    def from_row(cls, row: tuple) -> "Affaire":
        # ordre = (id_affaire, titre, date, lieu, statut, description)
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

    # -------- CRUD orienté classe --------
    @classmethod
    def create(
            cls,
            titre: str,
            date: str,
            lieu: str,
            statut: str,
            description: Optional[str] = None,
    ) -> "Affaire":
        """create() attendu dans l’issue."""
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

    @classmethod
    def get(cls, id_affaire: int) -> Optional["Affaire"]:
        """get() attendu dans l’issue."""
        row = get_by_id(cls.TABLE_NAME, id_affaire)
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Affaire"]:
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    # -------- CRUD orienté instance --------
    def update(self, **kwargs) -> None:
        """update() attendu dans l’issue."""
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
        update(self.TABLE_NAME, self.id_affaire, self.to_dict())

    def delete(self) -> None:
        """delete() attendu dans l’issue."""
        if self.id_affaire is not None:
            delete(self.TABLE_NAME, self.id_affaire)
            self.id_affaire = None

    # -------- Lien affaire ↔ suspects / preuves / armes / lieux --------
    def get_preuves(self):
        """Toutes les preuves de cette affaire."""
        from preuve import Preuve  # import local pour éviter les cycles
        return Preuve.list_for_affaire(self.id_affaire)

    def get_armes(self):
        """Toutes les armes de cette affaire."""
        from arme import Arme
        return Arme.list_for_affaire(self.id_affaire)

    def get_lieux(self):
        """Tous les lieux de cette affaire."""
        from lieu import Lieu
        return Lieu.list_for_affaire(self.id_affaire)

    def get_suspects(self):
        """Lister les suspects liés à l’affaire via les preuves."""
        from suspect import Suspect
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT s.*
            FROM Suspect s
                     JOIN Preuve p ON p.id_suspect = s.id_suspect
            WHERE p.id_affaire = ?
            """,
            (self.id_affaire,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [Suspect.from_row(r) for r in rows]
