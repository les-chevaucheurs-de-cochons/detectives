from dataclasses import dataclass
from typing import Optional, List
from backend.exceptions import PreconditionError, PostconditionError

from database import insert, get_all, get_by_id, update, delete, get_connection


@dataclass
class Affaire:
    id_affaire: Optional[int]
    titre: str
    date: str
    lieu: str
    code_postal: Optional[str]
    statut: str
    description: Optional[str] = None
    pos_x: int = 40
    pos_y: int = 40

    TABLE_NAME = "Affaire"

    def __post_init__(self):
        self._statut = self.statut

    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, value):
        # validation douce : si valeur étrange, on garde "En cours"
        allowed = {"en cours", "classée", "classee"}
        v = str(value).strip().lower()
        self._statut = value if v in allowed else "En cours"

    # =========================
    #  CONVERSIONS
    # =========================

    def to_dict(self) -> dict:
        return {
            "titre": self.titre,
            "date": self.date,
            "lieu": self.lieu,
            "code_postal": self.code_postal,
            "statut": self.statut,
            "description": self.description,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    @property
    def id(self):
        return self.id_affaire

    @property
    def uid(self):
        return f"A{self.id_affaire}"

    # =========================
    #  FACTORY / CRUD
    # =========================

    @classmethod
    def from_row(cls, row: tuple) -> "Affaire":
        """
        Ordre SQL attendu :
        (id_affaire, titre, date, lieu, code_postal, statut, description, pos_x, pos_y)
        """
        if row is None:
            raise ValueError("Ligne SQL vide pour Affaire")

        return cls(
            id_affaire=row[0],
            titre=row[1],
            date=row[2],
            lieu=row[3],
            code_postal=row[4],
            statut=row[5],
            description=row[6],
            pos_x=row[7],
            pos_y=row[8],
        )

    @classmethod
    def create(
            cls,
            titre: str,
            date: str,
            lieu: str,
            code_postal: Optional[str],
            statut: str,
            description: Optional[str] = None,
    ) -> "Affaire":

        # -------- PRE --------
        if not titre or not str(titre).strip():
            raise PreconditionError(
                "PRE: le titre de l'affaire ne peut pas être vide."
            )

        data = {
            "titre": titre,
            "date": date,
            "lieu": lieu,
            "code_postal": code_postal,
            "statut": statut,
            "description": description,
            "pos_x": 40,
            "pos_y": 40,
        }

        new_id = insert(cls.TABLE_NAME, data)

        # -------- POST --------
        if new_id is None:
            raise PostconditionError(
                "POST: l'id de l'affaire n'a pas été généré après l'insertion."
            )

        return cls(
            id_affaire=new_id,
            titre=titre,
            date=date,
            lieu=lieu,
            code_postal=code_postal,
            statut=statut,
            description=description,
            pos_x=40,
            pos_y=40,
        )

    @classmethod
    def get(cls, id_affaire: int) -> Optional["Affaire"]:
        row = get_by_id(cls.TABLE_NAME, id_affaire, pk="id_affaire")
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Affaire"]:
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    def save(self) -> None:
        if self.id_affaire is None:
            return
        update(self.TABLE_NAME, self.id_affaire, self.to_dict(), pk="id_affaire")

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def delete(self) -> None:
        if self.id_affaire is not None:
            delete(self.TABLE_NAME, self.id_affaire, pk="id_affaire")
            self.id_affaire = None

    # =========================
    #  POSITION VISUELLE (GUI)
    # =========================

    def update_position(self, x: int, y: int):
        self.pos_x = x
        self.pos_y = y
        update(
            self.TABLE_NAME,
            self.id_affaire,
            {"pos_x": x, "pos_y": y},
            pk="id_affaire"
        )

    # =========================
    #  LIAISONS
    # =========================

    def get_suspects(self):
        from backend.suspect import Suspect
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
                    SELECT s.*
                    FROM Suspect s
                             JOIN AffaireSuspect asj ON asj.id_suspect = s.id_suspect
                    WHERE asj.id_affaire = ?
                    """, (self.id_affaire,))
        rows = cur.fetchall()
        conn.close()
        return [Suspect.from_row(r) for r in rows]

    def get_armes(self):
        from backend.arme import Arme
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
                    SELECT a.*
                    FROM Arme a
                             JOIN AffaireArme aj ON aj.id_arme = a.id_arme
                    WHERE aj.id_affaire = ?
                    """, (self.id_affaire,))
        rows = cur.fetchall()
        conn.close()
        return [Arme.from_row(r) for r in rows]

    def get_lieux(self):
        from backend.lieu import Lieu
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
                    SELECT l.*
                    FROM Lieu l
                             JOIN AffaireLieu al ON al.id_lieu = l.id_lieu
                    WHERE al.id_affaire = ?
                    """, (self.id_affaire,))
        rows = cur.fetchall()
        conn.close()
        return [Lieu.from_row(r) for r in rows]
