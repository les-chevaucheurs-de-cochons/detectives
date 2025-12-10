# backend/lieu.py
from dataclasses import dataclass
from typing import Optional
from database import insert, get_all, get_by_id, update, delete


@dataclass
class Lieu:
    id_lieu: Optional[int]
    nom: str
    adresse: Optional[str]
    type: Optional[str]
    id_affaire: int
    pos_x: int = 200
    pos_y: int = 200

    TABLE_NAME = "Lieu"

    @property
    def id(self):
        return self.id_lieu

    @property
    def uid(self):
        return f"L{self.id_lieu}"


    def to_dict(self):
        return {
            "nom": self.nom,
            "adresse": self.adresse,
            "type": self.type,
            "id_affaire": self.id_affaire,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @classmethod
    def create(cls, nom, adresse, type, id_affaire):
        data = {
            "nom": nom,
            "adresse": adresse,
            "type": type,
            "id_affaire": id_affaire,
            "pos_x": 200,
            "pos_y": 200,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(new_id, nom, adresse, type, id_affaire)

    @classmethod
    def all(cls):
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        update(self.TABLE_NAME, self.id_lieu, self.to_dict())

    def update_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        update(self.TABLE_NAME, self.id_lieu, {"pos_x": x, "pos_y": y})

    def delete(self):
        delete(self.TABLE_NAME, self.id_lieu)
        self.id_lieu = None
