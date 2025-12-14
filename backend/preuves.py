from dataclasses import dataclass
from typing import Optional
from database import insert, get_all, get_by_id, update, delete


@dataclass
class Preuve:
    id_preuve: Optional[int]
    type: str
    description: Optional[str]
    date: Optional[str]
    lieu: Optional[str]
    id_affaire: int
    id_suspect: Optional[int] = None
    pos_x: int = 120
    pos_y: int = 120

    TABLE_NAME = "Preuve"

    @property
    def id(self):
        return self.id_preuve

    @property
    def uid(self):
        return f"P{self.id_preuve}"


    def to_dict(self):
        return {
            "type": self.type,
            "description": self.description,
            "date": self.date,
            "lieu": self.lieu,
            "id_affaire": self.id_affaire,
            "id_suspect": self.id_suspect,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @classmethod
    def create(cls, type, description, date, lieu, id_affaire, id_suspect=None):
        data = {
            "type": type,
            "description": description,
            "date": date,
            "lieu": lieu,
            "id_affaire": id_affaire,
            "id_suspect": id_suspect,
            "pos_x": 120,
            "pos_y": 120,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(new_id, type, description, date, lieu, id_affaire, id_suspect)

    @classmethod
    def all(cls):
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        update(self.TABLE_NAME, self.id_preuve, self.to_dict())

    def update_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        update(self.TABLE_NAME, self.id_preuve, {"pos_x": x, "pos_y": y})

    def delete(self):
        delete(self.TABLE_NAME, self.id_preuve)
        self.id_preuve = None
