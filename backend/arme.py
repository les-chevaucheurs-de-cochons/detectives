from dataclasses import dataclass
from typing import Optional, List
from database import insert, get_all, get_by_id, update, delete


@dataclass
class Arme:
    id_arme: Optional[int]
    type: str
    description: Optional[str]
    numero_serie: Optional[str]
    id_affaire: int
    pos_x: int = 160
    pos_y: int = 160

    TABLE_NAME = "Arme"

    @property
    def id(self):
        return self.id_arme

    @property
    def uid(self):
        return f"R{self.id_arme}"

    def to_dict(self):
        return {
            "type": self.type,
            "description": self.description,
            "numero_serie": self.numero_serie,
            "id_affaire": self.id_affaire,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
        }

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @classmethod
    def create(cls, type, description, numero_serie, id_affaire):
        data = {
            "type": type,
            "description": description,
            "numero_serie": numero_serie,
            "id_affaire": id_affaire,
            "pos_x": 160,
            "pos_y": 160,
        }
        new_id = insert(cls.TABLE_NAME, data)
        return cls(new_id, type, description, numero_serie, id_affaire)

    @classmethod
    def get(cls, id_arme: int) -> Optional["Arme"]:
        row = get_by_id(cls.TABLE_NAME, id_arme, pk="id_arme")
        return cls.from_row(row) if row else None

    @classmethod
    def all(cls) -> List["Arme"]:
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        update(self.TABLE_NAME, self.id_arme, self.to_dict(), pk="id_arme")

    def update_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
        update(self.TABLE_NAME, self.id_arme, {"pos_x": x, "pos_y": y}, pk="id_arme")

    def delete(self):
        delete(self.TABLE_NAME, self.id_arme, pk="id_arme")
        self.id_arme = None
