from typing import List
from backend.affaire import Affaire


class FiltreAffairesCLI:
    def __init__(self, affaires: List[Affaire]):
        self.affaires = affaires

    def en_cours(self) -> List[Affaire]:
        return [a for a in self.affaires if a.statut.lower() == "en cours"]

    def classees(self) -> List[Affaire]:
        return [a for a in self.affaires if a.statut.lower() == "classée"]
