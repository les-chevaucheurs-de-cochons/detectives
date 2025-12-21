"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Module standard de tests unitaires en Python
import unittest

# Permet de remplacer des fonctions par des "fausses" (mock)
from unittest.mock import patch

# Classe à tester
from backend.affaire import Affaire

# Exceptions personnalisées testées (PRE / POST)
from backend.exceptions import PreconditionError, PostconditionError


# Classe de tests unitaires pour la classe Affaire
class TestAffaireUnit(unittest.TestCase):

    # -------------------------------------------------
    # Test du @property statut avec validation
    # -------------------------------------------------
    def test_property_statut_validation_garde_en_cours_si_invalide(self):
        # Création d'une affaire avec un statut invalide
        a = Affaire(
            id_affaire=1,
            titre="Test",
            date="2025-01-01",
            lieu="LLN",
            code_postal="1348",
            statut="???",  # valeur invalide volontaire
            description=None,
            pos_x=40,
            pos_y=40
        )

        # Le statut invalide doit être remplacé par "En cours"
        self.assertEqual(a.statut, "En cours")

        # Changement vers une valeur valide
        a.statut = "classée"

        # Le statut valide doit être conservé
        self.assertEqual(a.statut, "classée")

    # -------------------------------------------------
    # Test de la PRE-condition : titre vide
    # -------------------------------------------------
    # Le décorateur patch remplace la fonction insert
    # par un mock pour éviter toute vraie insertion DB
    @patch("backend.affaire.insert")
    def test_create_precondition_titre_vide(self, mock_insert):
        # Si le titre est vide, une PreconditionError doit être levée
        with self.assertRaises(PreconditionError):
            Affaire.create(
                titre="   ",          # titre vide
                date="2025-01-01",
                lieu="LLN",
                code_postal="1348",
                statut="En cours",
                description=None
            )

        # Vérifie que l'insertion en DB n'a jamais été appelée
        mock_insert.assert_not_called()

    # -------------------------------------------------
    # Test de la POST-condition : id non généré
    # -------------------------------------------------
    @patch("backend.affaire.insert")
    def test_create_postcondition_id_non_genere(self, mock_insert):
        # Simule un insert qui échoue (retourne None)
        mock_insert.return_value = None

        # Une PostconditionError doit être levée
        with self.assertRaises(PostconditionError):
            Affaire.create(
                titre="Affaire X",
                date="2025-01-01",
                lieu="LLN",
                code_postal="1348",
                statut="En cours",
                description=None
            )

    # -------------------------------------------------
    # Test du cas nominal : création correcte
    # -------------------------------------------------
    @patch("backend.affaire.insert")
    def test_create_ok_retourne_affaire_avec_id(self, mock_insert):
        # Simule une insertion réussie avec id généré
        mock_insert.return_value = 42

        # Création de l'affaire
        a = Affaire.create(
            titre="Affaire OK",
            date="2025-01-01",
            lieu="LLN",
            code_postal="1348",
            statut="En cours",
            description="demo"
        )

        # Vérifie que l'objet retourné est bien une Affaire
        self.assertIsInstance(a, Affaire)

        # Vérifie que l'id a bien été assigné
        self.assertEqual(a.id_affaire, 42)

        # Vérifie les champs principaux
        self.assertEqual(a.titre, "Affaire OK")
        self.assertEqual(a.statut, "En cours")


# Permet de lancer les tests directement via ce fichier
if __name__ == "__main__":
    unittest.main()
