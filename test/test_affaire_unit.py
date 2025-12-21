import unittest
from unittest.mock import patch

from backend.affaire import Affaire
from backend.exceptions import PreconditionError, PostconditionError


class TestAffaireUnit(unittest.TestCase):
    def test_property_statut_validation_garde_en_cours_si_invalide(self):
        # statut invalide -> doit être remplacé par "En cours"
        a = Affaire(
            id_affaire=1,
            titre="Test",
            date="2025-01-01",
            lieu="LLN",
            code_postal="1348",
            statut="???",  # invalide
            description=None,
            pos_x=40,
            pos_y=40
        )
        self.assertEqual(a.statut, "En cours")

        # statut valide -> reste tel quel
        a.statut = "classée"
        self.assertEqual(a.statut, "classée")

    @patch("backend.affaire.insert")
    def test_create_precondition_titre_vide(self, mock_insert):
        # PRE : titre vide -> exception, et insert ne doit même pas être appelé
        with self.assertRaises(PreconditionError):
            Affaire.create(
                titre="   ",
                date="2025-01-01",
                lieu="LLN",
                code_postal="1348",
                statut="En cours",
                description=None
            )
        mock_insert.assert_not_called()

    @patch("backend.affaire.insert")
    def test_create_postcondition_id_non_genere(self, mock_insert):
        # POST : insert retourne None -> PostconditionError
        mock_insert.return_value = None

        with self.assertRaises(PostconditionError):
            Affaire.create(
                titre="Affaire X",
                date="2025-01-01",
                lieu="LLN",
                code_postal="1348",
                statut="En cours",
                description=None
            )

    @patch("backend.affaire.insert")
    def test_create_ok_retourne_affaire_avec_id(self, mock_insert):
        mock_insert.return_value = 42

        a = Affaire.create(
            titre="Affaire OK",
            date="2025-01-01",
            lieu="LLN",
            code_postal="1348",
            statut="En cours",
            description="demo"
        )

        self.assertIsInstance(a, Affaire)
        self.assertEqual(a.id_affaire, 42)
        self.assertEqual(a.titre, "Affaire OK")
        self.assertEqual(a.statut, "En cours")


if __name__ == "__main__":
    unittest.main()
