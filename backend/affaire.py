"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Permet de créer automatiquement __init__, __repr__, etc.
from dataclasses import dataclass

# Types pour annotations (meilleure lisibilité, pas obligatoire à l’exécution)
from typing import Optional, List

# Exceptions personnalisées pour PRE / POST conditions
from backend.exceptions import PreconditionError, PostconditionError

# Fonctions utilitaires pour accéder à la base de données
from database import insert, get_all, get_by_id, update, delete, get_connection


# @dataclass génère automatiquement le constructeur (__init__)
@dataclass
class Affaire:
    # Identifiant unique de l’affaire (None si pas encore en DB)
    id_affaire: Optional[int]

    # Données principales de l’affaire
    titre: str
    date: str
    lieu: str
    code_postal: Optional[str]
    statut: str

    # Données optionnelles
    description: Optional[str] = None

    # Position utilisée dans le GUI
    pos_x: int = 40
    pos_y: int = 40

    # Nom de la table SQL associée à cette classe
    TABLE_NAME = "Affaire"

    # Méthode appelée automatiquement après __init__ (dataclass)
    def __post_init__(self):
        # Stockage interne du statut (pour @property)
        self._statut = self.statut

    # Getter du statut (lecture contrôlée)
    @property
    def statut(self):
        return self._statut

    # Setter du statut avec validation
    @statut.setter
    def statut(self, value):
        # Valeurs autorisées pour le statut
        allowed = {"en cours", "classée", "classee"}

        # Normalisation de la valeur reçue
        v = str(value).strip().lower()

        # Si invalide → valeur par défaut
        self._statut = value if v in allowed else "En cours"

    # =========================
    #  CONVERSIONS
    # =========================

    # Convertit l’objet Affaire en dictionnaire (utile pour la DB)
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

    # Alias pratique pour accéder à l’id
    @property
    def id(self):
        return self.id_affaire

    # Identifiant lisible (ex: A12)
    @property
    def uid(self):
        return f"A{self.id_affaire}"

    # =========================
    #  FACTORY / CRUD
    # =========================

    # Crée une Affaire à partir d’une ligne SQL
    @classmethod
    def from_row(cls, row: tuple) -> "Affaire":
        # Sécurité : ligne SQL absente
        if row is None:
            raise ValueError("Ligne SQL vide pour Affaire")

        # Création de l’objet Affaire à partir de la ligne SQL
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

    # Méthode factory : crée et insère une nouvelle affaire en DB
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
        # Le titre est obligatoire
        if not titre or not str(titre).strip():
            raise PreconditionError(
                "PRE: le titre de l'affaire ne peut pas être vide."
            )

        # Données à insérer en base
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

        # Insertion dans la DB
        new_id = insert(cls.TABLE_NAME, data)

        # -------- POST --------
        # Vérification que l’ID a bien été généré
        if new_id is None:
            raise PostconditionError(
                "POST: l'id de l'affaire n'a pas été généré après l'insertion."
            )

        # Retourne l’objet Affaire créé
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

    # Récupère une affaire par son id
    @classmethod
    def get(cls, id_affaire: int) -> Optional["Affaire"]:
        row = get_by_id(cls.TABLE_NAME, id_affaire, pk="id_affaire")
        return cls.from_row(row) if row else None

    # Récupère toutes les affaires
    @classmethod
    def all(cls) -> List["Affaire"]:
        rows = get_all(cls.TABLE_NAME)
        return [cls.from_row(r) for r in rows]

    # Sauvegarde les modifications de l’objet en DB
    def save(self) -> None:
        if self.id_affaire is None:
            return
        update(self.TABLE_NAME, self.id_affaire, self.to_dict(), pk="id_affaire")

    # Met à jour dynamiquement plusieurs attributs
    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    # Supprime l’affaire de la DB
    def delete(self) -> None:
        if self.id_affaire is not None:
            delete(self.TABLE_NAME, self.id_affaire, pk="id_affaire")
            self.id_affaire = None

    # =========================
    #  POSITION VISUELLE (GUI)
    # =========================

    # Met à jour la position graphique de l’affaire
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

    # Récupère les suspects liés à l’affaire
    def get_suspects(self):
        from backend.suspect import Suspect
        conn = get_connection()
        cur = conn.cursor()

        # Requête SQL de jointure Affaire / Suspect
        cur.execute("""
                    SELECT s.*
                    FROM Suspect s
                             JOIN AffaireSuspect asj ON asj.id_suspect = s.id_suspect
                    WHERE asj.id_affaire = ?
                    """, (self.id_affaire,))

        rows = cur.fetchall()
        conn.close()

        return [Suspect.from_row(r) for r in rows]

    # Récupère les armes liées à l’affaire
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

    # Récupère les lieux liés à l’affaire
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
