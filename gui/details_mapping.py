from backend.affaire import Affaire
from backend.suspect import Suspect
from backend.preuves import Preuve
from backend.arme import Arme
from backend.lieu import Lieu

ENTITY_TYPES = {
    "Affaire": Affaire,
    "Suspect": Suspect,
    "Preuve": Preuve,
    "Arme": Arme,
    "Lieu": Lieu,
}

DISPLAY_FIELDS = {
    "Affaire": ["titre", "date", "lieu", "statut", "description"],
    "Suspect": ["nom", "prenom", "age", "adresse", "description"],
    "Preuve": ["type", "description", "date", "lieu", "id_affaire", "id_suspect"],
    "Arme": ["type", "description", "numero_serie", "id_affaire"],
    "Lieu": ["nom", "adresse", "type", "id_affaire"],
}
