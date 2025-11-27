from database import insert, get_all, get_by_id, update, delete


class GestionEnquetes:
    """
        Moteur central de gestion des enquêtes criminelles.
        Fournit un CRUD complet pour chaque entité ainsi
        qu’un système interne de relations.
    """

    # ============================================================
    #                 CRUD : AFFAIRES
    # ============================================================

    def creer_affaire(self, titre, date, lieu, statut, description=None):
        return insert("Affaire", {
            "titre": titre,
            "date": date,
            "lieu": lieu,
            "statut": statut,
            "description": description
        })

    def get_affaires(self):
        return get_all("Affaire")

    def get_affaire(self, id_affaire):
        return get_by_id("Affaire", id_affaire)

    def maj_affaire(self, id_affaire, data: dict):
        update("Affaire", id_affaire, data)

    def supprimer_affaire(self, id_affaire):
        delete("Affaire", id_affaire)

    # ============================================================
    #                 CRUD : SUSPECTS
    # ============================================================

    def creer_suspect(self, nom, prénom, âge=None, adresse=None, description=None):
        return insert("Suspect", {
            "nom": nom,
            "prénom": prénom,
            "âge": âge,
            "adresse": adresse,
            "description": description
        })

    def get_suspects(self):
        return get_all("Suspect")

    def get_suspect(self, id_suspect):
        return get_by_id("Suspect", id_suspect)

    def maj_suspect(self, id_suspect, data: dict):
        update("Suspect", id_suspect, data)

    def supprimer_suspect(self, id_suspect):
        delete("Suspect", id_suspect)

    # ============================================================
    #                 CRUD : PREUVES
    # ============================================================

    def creer_preuve(self, type, id_affaire, description=None, date=None, lieu=None, id_suspect=None):
        return insert("Preuve", {
            "type": type,
            "description": description,
            "date": date,
            "lieu": lieu,
            "id_affaire": id_affaire,
            "id_suspect": id_suspect
        })

    def get_preuves(self):
        return get_all("Preuve")

    def get_preuve(self, id_preuve):
        return get_by_id("Preuve", id_preuve)

    def maj_preuve(self, id_preuve, data: dict):
        update("Preuve", id_preuve, data)

    def supprimer_preuve(self, id_preuve):
        delete("Preuve", id_preuve)

    # ============================================================
    #                 CRUD : ARMES
    # ============================================================

    def creer_arme(self, type, id_affaire, description=None, numéro_série=None):
        return insert("Arme", {
            "type": type,
            "description": description,
            "numéro_série": numéro_série,
            "id_affaire": id_affaire
        })

    def get_armes(self):
        return get_all("Arme")

    def get_arme(self, id_arme):
        return get_by_id("Arme", id_arme)

    def maj_arme(self, id_arme, data: dict):
        update("Arme", id_arme, data)

    def supprimer_arme(self, id_arme):
        delete("Arme", id_arme)

    # ============================================================
    #                 CRUD : LIEUX
    # ============================================================

    def creer_lieu(self, nom, id_affaire, adresse=None, type=None):
        return insert("Lieu", {
            "nom": nom,
            "adresse": adresse,
            "type": type,
            "id_affaire": id_affaire
        })

    def get_lieux(self):
        return get_all("Lieu")

    def get_lieu(self, id_lieu):
        return get_by_id("Lieu", id_lieu)

    def maj_lieu(self, id_lieu, data: dict):
        update("Lieu", id_lieu, data)

    def supprimer_lieu(self, id_lieu):
        delete("Lieu", id_lieu)

    # ============================================================
    #                 CRUD : AGENTS
    # ============================================================

    def creer_agent(self, nom, prénom, grade=None, service=None):
        return insert("Agent", {
            "nom": nom,
            "prénom": prénom,
            "grade": grade,
            "service": service
        })

    def get_agents(self):
        return get_all("Agent")

    def get_agent(self, id_agent):
        return get_by_id("Agent", id_agent)

    def maj_agent(self, id_agent, data: dict):
        update("Agent", id_agent, data)

    def supprimer_agent(self, id_agent):
        delete("Agent", id_agent)

    # ============================================================
    #                 RELATIONS ENTRE ENTITÉS
    # ============================================================

    def creer_relation(self, type, id_entite1, id_entite2, description=None):
        """
        type : ex 'connaît', 'lié à', 'a vu', 'parent de', etc.
        """
        return insert("Relation", {
            "type": type,
            "id_entite1": id_entite1,
            "id_entite2": id_entite2,
            "description": description
        })

    def get_relations(self):
        return get_all("Relation")

    def supprimer_relation(self, id_relation):
        delete("Relation", id_relation)
