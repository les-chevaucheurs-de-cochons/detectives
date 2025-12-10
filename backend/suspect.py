from dataclasses import dataclass
from typing import Optional, List
from database import insert, get_all, get_by_id, update, delete


@dataclass
class Suspect:
    id_suspect: Optional[int]
    nom: str
    prenom: str
    age: Optional[int] = None
    adresse: Optional[str] = None
    description: Optional[str] = None
    pos_x: int = 80
    pos_y: int = 80

    TABLE_NAME = "Suspect"

    @property
    def id(self):
        return self.id_suspect

    @property
    def uid(self):
        return f"S{self.id_suspect}"


    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,      # ✔ corrigé
            "age": self.age,            # ✔ corrigé
            "adresse": self.adresse,
            "description": self.description,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    @classmethod
    def from_row(cls, row):
        return cls(
            id_suspect=row[0],
            nom=row[1],
            prenom=row[2],
            age=row[3],
            adresse=row[4],
            description=row[5],
            pos_x=row[6],
            pos_y=row[7],
        )

    @classmethod
    def create(cls, nom, prenom, age=None, adresse=None, description=None):
        data = {
            "nom": nom,
            "prenom": prenom,     # ✔ corrigé
            "age": age,           # ✔ corrigé
            "adresse": adresse,
            "description": description,
            "pos_x": 80,
            "pos_y": 80,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(new_id, nom, prenom, age, adresse, description)

    @classmethod
    def all(cls):
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        update(self.TABLE_NAME, self.id_suspect, self.to_dict())

    def update_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        update(self.TABLE_NAME, self.id_suspect, {"pos_x": x, "pos_y": y})

    def delete(self):
        delete(self.TABLE_NAME, self.id_suspect)
        self.id_suspect = None
