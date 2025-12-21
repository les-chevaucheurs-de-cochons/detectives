import unittest
import os

from backend.gestion_enquete import GestionEnquetes
from database import init_db


class TestGestionEnquetes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # On supprime la base existante pour repartir sur un état propre
        if os.path.exists("detectives.db"):
            os.remove("detectives.db")

        init_db()

    def setUp(self):
        self.g = GestionEnquetes()

    # ==================================================
    # TEST 1 — CRUD AFFAIRE
    # ==================================================
    def test_crud_affaire(self):
        """
        Fonction testée : creer_affaire / maj_affaire / supprimer_affaire

        PRE :
        - Le titre est une chaîne non vide
        - La date est au format JJ-MM-AAAA
        - Le statut est valide
        - La base de données est initialisée

        POST :
        - L'affaire est créée avec un id
        - L'affaire peut être modifiée
        - L'affaire peut être supprimée
        """

        # Création
        affaire = self.g.creer_affaire(
            "Test Affaire",
            "01-01-2025",
            "TestVille",
            "9999",
            "en cours"
        )

        # Vérification création
        self.assertIsNotNone(affaire.id_affaire)

        # Modification
        self.g.maj_affaire(
            affaire.id_affaire,
            {"statut": "classée"}
        )

        affaire_mod = self.g.get_affaire(affaire.id_affaire)
        self.assertEqual(affaire_mod.statut, "classée")

        # Suppression
        self.g.supprimer_affaire(affaire.id_affaire)
        self.assertIsNone(self.g.get_affaire(affaire.id_affaire))

    # ==================================================
    # TEST 2 — UNICITÉ DU CODE POSTAL
    # ==================================================
    def test_ville_unique(self):
        """
        Fonction testée : creer_ville / get_ville

        PRE :
        - Le code postal est une chaîne non vide
        - Le nom de la ville est une chaîne non vide

        POST :
        - Une ville peut être créée
        - Le code postal est unique
        - Une exception est levée en cas de doublon
        """

        # Création valide
        self.g.creer_ville("1000", "Bruxelles")

        ville = self.g.get_ville("1000")
        self.assertIsNotNone(ville)
        self.assertEqual(ville["nom"], "Bruxelles")

        # Tentative de doublon
        with self.assertRaises(Exception):
            self.g.creer_ville("1000", "AutreVille")


if __name__ == "__main__":
    unittest.main()
