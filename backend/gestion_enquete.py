from typing import List, Optional

from .affaire import Affaire
from .suspect import Suspect
from .arme import Arme
from .lieu import Lieu


from database import insert, get_all, update, delete, get_connection


class GestionEnquetes:


    # ============================================================
    #                     AFFAIRES
    # ============================================================

    def creer_affaire(self, *args, **kwargs) -> Affaire:
        return Affaire.create(*args, **kwargs)

    def get_affaire(self, id_affaire: int) -> Optional[Affaire]:
        return Affaire.get(id_affaire)

    def get_affaires(self) -> List[Affaire]:
        return Affaire.all()

    def supprimer_affaire(self, id_affaire: int):
        a = Affaire.get(id_affaire)
        if a:
            a.delete()

    def maj_affaire(self, id_affaire: int, data: dict):
        a = Affaire.get(id_affaire)
        if a:
            a.update(**data)

    # ============================================================
    #                     SUSPECTS
    # ============================================================

    def creer_suspect(self, *args, **kwargs) -> Suspect:
        return Suspect.create(*args, **kwargs)

    def get_suspect(self, id_suspect: int) -> Optional[Suspect]:
        return Suspect.get(id_suspect)

    def get_suspects(self) -> List[Suspect]:
        return Suspect.all()

    def supprimer_suspect(self, id_suspect: int):
        s = Suspect.get(id_suspect)
        if s:
            s.delete()

    def maj_suspect(self, id_suspect: int, data: dict):
        s = Suspect.get(id_suspect)
        if s:
            s.update(**data)

    # ============================================================
    #                     ARMES
    # ============================================================

    def creer_arme(self, *args, **kwargs) -> Arme:
        return Arme.create(*args, **kwargs)

    def get_arme(self, id_arme: int) -> Optional[Arme]:
        return Arme.get(id_arme)

    def get_armes(self) -> List[Arme]:
        return Arme.all()

    def supprimer_arme(self, id_arme: int):
        a = Arme.get(id_arme)
        if a:
            a.delete()

    def maj_arme(self, id_arme: int, data: dict):
        a = Arme.get(id_arme)
        if a:
            a.update(**data)

    # ============================================================
    #                     VILLES
    # ============================================================

    def creer_ville(self, code_postal: str, nom: str):
        return insert("Ville", {"code_postal": code_postal, "nom": nom})

    def get_villes(self):
        return get_all("Ville")   # retourne liste de tuples (code_postal, nom)

    def get_ville(self, code_postal: str):
        rows = get_all("Ville")
        for cp, nom in rows:
            if cp == code_postal:
                return {"code_postal": cp, "nom": nom}
        return None




    # ============================================================
    #                     LIEUX
    # ============================================================

    def creer_lieu(self, *args, **kwargs) -> Lieu:
        return Lieu.create(*args, **kwargs)

    def get_lieu(self, id_lieu: int) -> Optional[Lieu]:
        return Lieu.get(id_lieu)

    def get_lieux(self) -> List[Lieu]:
        return Lieu.all()

    def supprimer_lieu(self, id_lieu: int):
        l = Lieu.get(id_lieu)
        if l:
            l.delete()

    def maj_lieu(self, id_lieu: int, data: dict):
        l = Lieu.get(id_lieu)
        if l:
            l.update(**data)

    # ============================================================
    #                     RELATIONS
    # ============================================================

    def creer_relation(self, type_rel, uid1, uid2, description=None):
        return insert("Relation", {
            "type": type_rel,
            "id_entite1": uid1,
            "id_entite2": uid2,
            "description": description
        })


    def get_relations(self):
        return get_all("Relation")

    def supprimer_relation(self, id_relation):
        delete("Relation", id_relation)

    # ============================================================
    #                     POSITIONS VISUELLES
    # ============================================================

    def maj_position_affaire(self, id_affaire, x, y):
        update("Affaire", id_affaire, {"pos_x": x, "pos_y": y})

    def maj_position_suspect(self, id_suspect, x, y):
        update("Suspect", id_suspect, {"pos_x": x, "pos_y": y})


# ============================================================
#            LIAISONS AFFAIRE <-> SUSPECT / ARME / LIEU
# ============================================================

    def lier_suspect_affaire(self, id_affaire: int, id_suspect: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO AffaireSuspect (id_affaire, id_suspect) VALUES (?, ?)",
            (id_affaire, id_suspect),
        )
        conn.commit()
        conn.close()

    def lier_arme_affaire(self, id_affaire: int, id_arme: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO AffaireArme (id_affaire, id_arme) VALUES (?, ?)",
            (id_affaire, id_arme),
        )
        conn.commit()
        conn.close()

    def lier_lieu_affaire(self, id_affaire: int, id_lieu: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO AffaireLieu (id_affaire, id_lieu) VALUES (?, ?)",
            (id_affaire, id_lieu),
        )
        conn.commit()
        conn.close()


    # ---------------- Liaisons : suppression ----------------

    def del_suspect_affaire(self, id_affaire: int, id_suspect: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM AffaireSuspect WHERE id_affaire = ? AND id_suspect = ?",
            (id_affaire, id_suspect),
        )
        conn.commit()
        conn.close()

    def del_arme_affaire(self, id_affaire: int, id_arme: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM AffaireArme WHERE id_affaire = ? AND id_arme = ?",
            (id_affaire, id_arme),
        )
        conn.commit()
        conn.close()

    def del_lieu_affaire(self, id_affaire: int, id_lieu: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM AffaireLieu WHERE id_affaire = ? AND id_lieu = ?",
            (id_affaire, id_lieu),
        )
        conn.commit()
        conn.close()
