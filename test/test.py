import unittest
import os

from backend.gestion_enquete import GestionEnquetes
from database import init_db, get_connection


class TestGestionEnquetes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Initialisation avant tous les tests
        """
        # Supprimer la base pour repartir propre
        if os.path.exists("detectives.db"):
            os.remove("detectives.db")

        init_db()

    def setUp(self):
        """
        Nouvelle instance pour chaque test
        """
        self.g = GestionEnquetes()

    # ==================================================
    # TEST 1 — CRUD AFFAIRE
    # ==================================================
    def test_crud_affaire(self):
        affaire = self.g.creer_affaire(
            "Test Affaire",
            "01-01-2025",
            "TestVille",
            "9999",
            "en cours"
        )

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
    # TEST 2 — UNICITÉ CODE POSTAL
    # ==================================================
    def test_ville_unique(self):
        self.g.creer_ville("1000", "Bruxelles")

        ville = self.g.get_ville("1000")
        self.assertIsNotNone(ville)
        self.assertEqual(ville["nom"], "Bruxelles")

        # Tentative de doublon
        with self.assertRaises(Exception):
            self.g.creer_ville("1000", "AutreVille")

    # ==================================================
    # TEST 3 — LIAISON AFFAIRE / SUSPECT (BDD)
    # ==================================================
    def test_liaison_suspect_affaire(self):
        affaire = self.g.creer_affaire(
            "Affaire lien",
            "01-01-2024",
            "VilleLien",
            "8888",
            "en cours"
        )

        suspect = self.g.creer_suspect(
            "Doe",
            "John",
            30,
            "Rue test",
            None
        )

        # Création de la liaison
        self.g.lier_suspect_affaire(affaire.id_affaire, suspect.id_suspect)

        # Vérification directe en base
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM AffaireSuspect WHERE id_affaire = ? AND id_suspect = ?",
            (affaire.id_affaire, suspect.id_suspect)
        )
        row = cur.fetchone()
        conn.close()

        self.assertIsNotNone(row)


if __name__ == "__main__":
    unittest.main()
