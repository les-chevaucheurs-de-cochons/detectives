"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Génère automatiquement __init__, __repr__, etc.
from dataclasses import dataclass

# Types optionnels pour une meilleure lisibilité
from typing import Optional, List

# Fonctions utilitaires pour la base de données
from database import insert, get_all, get_by_id, update, delete


# Représente un lieu lié à une affaire
@dataclass
class Lieu:
    # Identifiant unique du lieu (None si pas encore en DB)
    id_lieu: Optional[int]

    # Nom du lieu (ex: Maison, Rue, Entrepôt)
    nom: str

    # Adresse éventuelle
    adresse: Optional[str]

    # Type de lieu (ex: public, privé, crime, etc.)
    type: Optional[str]

    # Identifiant de l’affaire liée
    id_affaire: int

    # Nom de la table SQL associée
    TABLE_NAME = "Lieu"

    # Alias pratique pour l'id
    @property
    def id(self):
        return self.id_lieu

    # Identifiant lisible (ex: L3)
    @property
    def uid(self):
        return f"L{self.id_lieu}"

    # Convertit l’objet Lieu en dictionnaire (pour la DB)
    def to_dict(self):
        return {
            "nom": self.nom,
            "adresse": self.adresse,
            "type": self.type,
            "id_affaire": self.id_affaire,
        }

    # Crée un objet Lieu à partir d’une ligne SQL
    @classmethod
    def from_row(cls, row):
        return cls(*row)

    # Crée un lieu et l’insère en base de données
    @classmethod
    def create(cls, nom, adresse, type, id_affaire):
        # Données à insérer
        data = {
            "nom": nom,
            "adresse": adresse,
            "type": type,
            "id_affaire": id_affaire,
        }

        # Insertion en DB
        new_id = insert(cls.TABLE_NAME, data)

        # Retourne l’objet Lieu créé
        return cls(new_id, nom, adresse, type, id_affaire)

    # Récupère un lieu via son id
    @classmethod
    def get(cls, id_lieu: int) -> Optional["Lieu"]:
        row = get_by_id(cls.TABLE_NAME, id_lieu, pk="id_lieu")
        return cls.from_row(row) if row else None

    # Récupère tous les lieux
    @classmethod
    def all(cls) -> List["Lieu"]:
        return [cls.from_row(r) for r in get_all(cls.TABLE_NAME)]

    # Met à jour les champs du lieu
    def update(self, **kwargs):
        # Met à jour dynamiquement les attributs existants
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

        # Sauvegarde les modifications en DB
        update(self.TABLE_NAME, self.id_lieu, self.to_dict(), pk="id_lieu")

    # Supprime le lieu de la base
    def delete(self):
        delete(self.TABLE_NAME, self.id_lieu, pk="id_lieu")
        self.id_lieu = None
