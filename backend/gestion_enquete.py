# gestion_enquete.py
from typing import List, Optional

from .affaire import Affaire
from .suspect import Suspect
from .preuves import Preuve
from .arme import Arme
from .lieu import Lieu


from database import insert, get_all, get_by_id, update, delete   # seulement pour Relation


class GestionEnquetes:
    """
    Gestionnaire central de l’application.
    Interagit avec les modèles (Affaire, Suspect, Preuve, Arme, Lieu)
    et la table Relation.
    """

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
    #                     PREUVES
    # ============================================================

    def creer_preuve(self, *args, **kwargs) -> Preuve:
        p = Preuve(
            id_preuve=None,
            type=kwargs["type"],
            id_affaire=kwargs["id_affaire"],
            description=kwargs.get("description"),
            date=kwargs.get("date"),
            lieu=kwargs.get("lieu"),
            id_suspect=kwargs.get("id_suspect"),
        )
        p.save()
        return p

    def get_preuve(self, id_preuve: int) -> Optional[Preuve]:
        return Preuve.get(id_preuve)

    def get_preuves(self) -> List[Preuve]:
        return Preuve.all()

    def supprimer_preuve(self, id_preuve: int):
        p = Preuve.get(id_preuve)
        if p:
            p.delete()

    def maj_preuve(self, id_preuve: int, data: dict):
        p = Preuve.get(id_preuve)
        if p:
            for k, v in data.items():
                setattr(p, k, v)
            p.save()

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
