"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Génère automatiquement __init__, __repr__, etc.
from dataclasses import dataclass

# Types optionnels pour plus de clarté
from typing import Optional, List

# Fonctions utilitaires pour la base de données
from database import insert, get_all, get_by_id, update, delete


# Représente une arme liée à une affaire
@dataclass
class Arme:
    # Identifiant unique de l’arme (None si pas encore en DB)
    id_arme: Optional[int]

    # Type d’arme (ex: couteau, pistolet, etc.)
    type: str

    # Description libre de l’arme
    description: Optional[str]

    # Numéro de série éventuel
    numero_serie: Optional[str]

    # Identifiant de l’affaire à laquelle l’arme est liée
    id_affaire: int

    # Nom de la table SQL correspondante
    TABLE_NAME = "Arme"

    # Alias pratique pour accéder à l’id
    @property
    def id(self):
        return self.id_arme

    # Identifiant lisible (ex: R5)
    @property
    def uid(self):
        return f"R{self.id_arme}"

    # Convertit l’objet Arme en dictionnaire (utile pour update/insert)
    def to_dict(self):
        return {
            "type": self.type,
            "description": self.description,
            "numero_serie": self.numero_serie,
            "id_affaire": self.id_affaire,
        }

    # Crée une instance d’Arme à partir d’une ligne SQL
    @classmethod
    def from_row(cls, row):
        # Le *row permet de passer tous les champs directement
        return cls(*row)

    # Crée une arme et l’insère en base de données
    @classmethod
    def create(cls, type, description, numero_serie, id_affaire):
        # Données à insérer en DB
        data = {
            "type": type,
            "description": description,
            "numero_serie": numero_serie,
            "id_affaire": id_affaire,
        }

        # Insertion dans la table Arme
        new_id = insert(cls.TABLE_NAME, data)

        # Retourne l’objet Arme créé
        return cls(new_id, type, description, numero_serie, id_affaire)

    # Récupère une arme via son identifiant
    @classmethod
    def get(cls, id_arme: int) -> Optional["Arme"]:
        row = get_by_id(cls.TABLE_NAME, id_arme, pk="id_arme")
        return cls.from_row(row) if row else None

    # Récupère toutes les armes de la base
    @classmethod
    def all(cls) -> List["Arme"]:
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    # Met à jour les champs de l’arme
    def update(self, **kwargs):
        # Parcourt les champs à modifier
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

        # Sauvegarde les modifications en DB
        update(self.TABLE_NAME, self.id_arme, self.to_dict(), pk="id_arme")

    # Supprime l’arme de la base
    def delete(self):
        delete(self.TABLE_NAME, self.id_arme, pk="id_arme")

        # L’objet n’a plus d’id après suppression
        self.id_arme = None
