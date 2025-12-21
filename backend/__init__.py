"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Importe la classe GestionEnquetes depuis le fichier gestion_enquete.py
# Le point (.) signifie : "dans le même dossier (backend)"
from .gestion_enquete import GestionEnquetes


# __all__ définit ce qui est exporté publiquement par le package backend
# Cela signifie que seul GestionEnquetes est accessible avec :
# from backend import *
__all__ = ["GestionEnquetes"]
