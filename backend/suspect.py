from dataclasses import dataclass
from typing import Optional, List
from database import insert, get_all, get_by_id, update, delete


def ensure_bool(func):
    def wrapper(self, value):
        if not isinstance(value, bool):
            raise ValueError("Le casier doit être un booléen (True/False).")
        return func(self, value)
    return wrapper


@dataclass
class Suspect:
    id_suspect: Optional[int]
    nom: str
    prenom: str
    age: Optional[int] = None
    adresse: Optional[str] = None
    description: Optional[str] = None
    casier: bool = False
    pos_x: int = 80
    pos_y: int = 80

    TABLE_NAME = "Suspect"

    @property
    def id(self):
        return self.id_suspect

    @property
    def uid(self):
        return f"S{self.id_suspect}"

    @property
    def a_casier(self) -> bool:
        return self.casier

    @a_casier.setter
    @ensure_bool
    def a_casier(self, value: bool):
        self.casier = value

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

    @classmethod
    def from_row(cls, row):
        # adapter les index si ta colonne casier n'est pas à cette position
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

    @classmethod
    def get(cls, id_suspect: int) -> Optional["Suspect"]:
        row = get_by_id(cls.TABLE_NAME, id_suspect, pk="id_suspect")
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Suspect"]:
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        update(self.TABLE_NAME, self.id_suspect, self.to_dict(), pk="id_suspect")

    def update_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        update(self.TABLE_NAME, self.id_suspect, {"pos_x": x, "pos_y": y}, pk="id_suspect")

    def delete(self):
        delete(self.TABLE_NAME, self.id_suspect, pk="id_suspect")
        self.id_suspect = None
