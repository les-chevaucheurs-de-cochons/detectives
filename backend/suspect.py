"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Génère automatiquement __init__, __repr__, etc.
from dataclasses import dataclass

# Types optionnels pour lisibilité
from typing import Optional, List

# Fonctions utilitaires DB
from database import insert, get_all, get_by_id, update, delete


# Exception personnalisée pour validation du suspect
class ValidationSuspectError(Exception):
    """Exception levée lors d'une validation Suspect invalide."""
    pass


# Décorateur pour forcer une valeur booléenne
def ensure_bool(func):
    def wrapper(self, value):
        # Vérifie que la valeur est bien un booléen
        if not isinstance(value, bool):
            raise ValidationSuspectError(
                "Le casier doit être un booléen (True/False)."
            )
        return func(self, value)
    return wrapper


# Représente un suspect
@dataclass
class Suspect:
    # Identifiant unique du suspect
    id_suspect: Optional[int]

    # Informations personnelles
    nom: str
    prenom: str
    age: Optional[int] = None
    adresse: Optional[str] = None
    description: Optional[str] = None

    # Indique si le suspect a un casier judiciaire
    casier: bool = False

    # Position graphique dans le GUI
    pos_x: int = 80
    pos_y: int = 80

    # Nom de la table SQL
    TABLE_NAME = "Suspect"

    # Alias pour l'id
    @property
    def id(self):
        return self.id_suspect

    # Identifiant lisible (ex: S4)
    @property
    def uid(self):
        return f"S{self.id_suspect}"

    # Getter du casier
    @property
    def a_casier(self) -> bool:
        return self.casier

    # Setter du casier avec validation via décorateur
    @a_casier.setter
    @ensure_bool
    def a_casier(self, value: bool):
        self.casier = value

    # Convertit l’objet Suspect en dictionnaire
    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "age": self.age,
            "adresse": self.adresse,
            "description": self.description,
            "casier": int(self.casier),
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    # Crée un suspect à partir d’une ligne SQL
    @classmethod
    def from_row(cls, row):
        return cls(
            id_suspect=row[0],
            nom=row[1],
            prenom=row[2],
            age=row[3],
            adresse=row[4],
            description=row[5],
            casier=bool(row[6]),
            pos_x=row[7],
            pos_y=row[8],
        )

    # Crée un suspect et l’insère en DB
    @classmethod
    def create(cls, nom, prenom, age=None, adresse=None, description=None, casier: bool = False):
        data = {
            "nom": nom,
            "prenom": prenom,
            "age": age,
            "adresse": adresse,
            "description": description,
            "casier": int(casier),
            "pos_x": 80,
            "pos_y": 80,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(new_id, nom, prenom, age, adresse, description, casier)

    # Récupère un suspect par id
    @classmethod
    def get(cls, id_suspect: int) -> Optional["Suspect"]:
        row = get_by_id(cls.TABLE_NAME, id_suspect, pk="id_suspect")
        return cls.from_row(row) if row else None

    # Récupère tous les suspects
    @classmethod
    def all(cls) -> List["Suspect"]:
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    # Met à jour les champs du suspect
    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        update(self.TABLE_NAME, self.id_suspect, self.to_dict(), pk="id_suspect")

    # Met à jour la position graphique
    def update_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        update(
            self.TABLE_NAME,
            self.id_suspect,
            {"pos_x": x, "pos_y": y},
            pk="id_suspect"
        )

    # Supprime le suspect
    def delete(self):
        delete(self.TABLE_NAME, self.id_suspect, pk="id_suspect")
        self.id_suspect = None
