import unittest
from backend.suspect import Suspect


class TestSuspectCasier(unittest.TestCase):

    # Pré-condition : le setter doit refuser autre chose qu’un booléen
    def test_set_casier_non_bool_declenche_exception(self):
        s = Suspect(id_suspect=None, nom="Test", prenom="Toto")
        with self.assertRaises(ValueError):
            s.a_casier = "oui"  # pré-condition violée : doit être un bool

    # Post-condition : si on met True, la propriété retourne bien True
    def test_casier_true_bien_enregistre(self):
        s = Suspect(id_suspect=None, nom="Test", prenom="Toto")
        s.a_casier = True
        self.assertTrue(s.a_casier)


if __name__ == "__main__":
    unittest.main()
