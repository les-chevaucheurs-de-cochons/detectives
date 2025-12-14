from backend import GestionEnquetes
from datetime import datetime
import re
from typing import Optional

gestion = GestionEnquetes()


# ================================
#  UTILITAIRES
# ================================

def valider_date_fr(date_str: str) -> bool:
    """Valide format JJ-MM-AAAA"""
    if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
        return False
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def saisie_obligatoire(prompt: str) -> str:
    while True:
        valeur = input(prompt).strip()
        if valeur:
            return valeur
        print("❌ Ce champ est obligatoire.")


def saisie_date(prompt: str, valeur_defaut: Optional[str] = None) -> str:
    while True:
        if valeur_defaut is not None:
            saisie = input(f"{prompt} [{valeur_defaut}] : ").strip()
            if not saisie:
                return valeur_defaut
        else:
            saisie = input(f"{prompt} : ").strip()

        if valider_date_fr(saisie):
            return saisie
        print("❌ Date invalide. Attendu : JJ-MM-AAAA (ex: 12-12-2025).")


def saisie_libre_ou_defaut(prompt: str, valeur_defaut: str) -> str:
    saisie = input(f"{prompt} [{valeur_defaut}] : ").strip()
    return saisie or valeur_defaut


def saisie_statut() -> str:
    """1 = en cours, 0 = classée"""
    while True:
        choix = input("Statut (1=en cours, 0=classée) : ").strip()
        if choix == "1":
            return "en cours"
        elif choix == "0":
            return "classée"
        print("❌ Tapez 1 ou 0")


def lister_affaires_court():
    affaires = gestion.get_affaires()
    if not affaires:
        print("❌ Aucune affaire trouvée.")
        return []
    print(f"\n📂 {len(affaires)} affaire(s) :")
    for a in affaires:
        ville_str = f"{a.code_postal or '----'} {a.lieu or ''}".strip()
        print(f"🆔 {a.id_affaire} | {a.titre} | {ville_str} | {a.statut}")
    return affaires



def choisir_ou_creer_suspects(id_affaire: int):
    while True:
        affaire = gestion.get_affaire(id_affaire)
        suspects_actuels = affaire.get_suspects()

        print(f"\n👥 SUSPECTS pour l'affaire {id_affaire}")
        if suspects_actuels:
            print("   Actuels :")
            for s in suspects_actuels:
                desc = f" — {s.description}" if s.description else ""
                print(f"   [{s.id_suspect}] {s.prenom} {s.nom}{desc}")
        else:
            print("   Aucun suspect pour l'instant.")

        print("\n1. Lier un suspect existant")
        print("2. Créer un nouveau suspect et le lier")
        print("3. Retirer un suspect de l'affaire")
        print("0. Terminer les suspects")
        choix = input("Votre choix : ").strip()

        if choix == "0":
            break

        elif choix == "1":
            suspects = gestion.get_suspects()
            if not suspects:
                print("❌ Aucun suspect existant.")
                continue
            for s in suspects:
                print(f"[{s.id_suspect}] {s.prenom} {s.nom}")
            try:
                sid = int(input("ID suspect à lier : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue
            if not gestion.get_suspect(sid):
                print("❌ Suspect introuvable.")
                continue
            gestion.lier_suspect_affaire(id_affaire, sid)
            print("✅ Suspect lié.")

        elif choix == "2":
            prenom = saisie_obligatoire("Prénom suspect : ")
            nom = saisie_obligatoire("Nom suspect : ")
            description = input("Description (optionnelle) : ").strip() or None
            s = gestion.creer_suspect(nom, prenom, description=description)
            gestion.lier_suspect_affaire(id_affaire, s.id_suspect)
            print(f"✅ Suspect créé et lié (ID {s.id_suspect}).")

        elif choix == "3":
            if not suspects_actuels:
                print("❌ Aucun suspect à retirer.")
                continue
            try:
                sid = int(input("ID du suspect à retirer : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue
            if not any(s.id_suspect == sid for s in suspects_actuels):
                print("❌ Ce suspect n'est pas lié à cette affaire.")
                continue
            gestion.del_suspect_affaire(id_affaire, sid)
            print("✅ Suspect retiré de l'affaire.")
        else:
            print("❌ Choix invalide.")




def choisir_ou_creer_armes(id_affaire: int):
    while True:
        affaire = gestion.get_affaire(id_affaire)
        armes_actuelles = affaire.get_armes()

        print(f"\n🔪 ARMES pour l'affaire {id_affaire}")
        if armes_actuelles:
            print("   Actuelles :")
            for a in armes_actuelles:
                pieces = [a.type]
                if a.numero_serie:
                    pieces.append(f"n° {a.numero_serie}")
                if a.description:
                    pieces.append(a.description)
                print(f"   [{a.id_arme}] " + " — ".join(pieces))
        else:
            print("   Aucune arme pour l'instant.")

        print("\n1. Lier une arme existante")
        print("2. Créer une nouvelle arme et la lier")
        print("3. Retirer une arme de l'affaire")
        print("0. Terminer les armes")
        choix = input("Votre choix : ").strip()

        if choix == "0":
            break

        elif choix == "1":
            armes = gestion.get_armes()
            if not armes:
                print("❌ Aucune arme existante.")
                continue
            for a in armes:
                print(f"[{a.id_arme}] {a.type} (n° série: {a.numero_serie or 'N/A'})")
            try:
                aid = int(input("ID arme à lier : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue
            if not gestion.get_arme(aid):
                print("❌ Arme introuvable.")
                continue
            gestion.lier_arme_affaire(id_affaire, aid)
            print("✅ Arme liée.")

        elif choix == "2":
            type_arme = saisie_obligatoire("Type d'arme : ")
            numero = input("Numéro de série (optionnel) : ").strip() or None
            description = input("Description (optionnelle) : ").strip() or None
            a = gestion.creer_arme(type_arme, description, numero, id_affaire)
            gestion.lier_arme_affaire(id_affaire, a.id_arme)
            print(f"✅ Arme créée et liée (ID {a.id_arme}).")

        elif choix == "3":
            if not armes_actuelles:
                print("❌ Aucune arme à retirer.")
                continue
            try:
                aid = int(input("ID de l'arme à retirer : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue
            if not any(a.id_arme == aid for a in armes_actuelles):
                print("❌ Cette arme n'est pas liée à cette affaire.")
                continue
            gestion.del_arme_affaire(id_affaire, aid)
            print("✅ Arme retirée de l'affaire.")
        else:
            print("❌ Choix invalide.")



def choisir_ou_creer_lieux(id_affaire: int):
    while True:
        affaire = gestion.get_affaire(id_affaire)
        lieux_actuels = affaire.get_lieux()

        print(f"\n📍 LIEUX pour l'affaire {id_affaire}")
        if lieux_actuels:
            print("   Actuels :")
            for l in lieux_actuels:
                adr = l.adresse if l.adresse else "adresse inconnue"
                print(f"   [{l.id_lieu}] {l.nom} ({adr})")
        else:
            print("   Aucun lieu pour l'instant.")

        print("\n1. Lier un lieu existant")
        print("2. Créer un nouveau lieu et le lier")
        print("3. Retirer un lieu de l'affaire")
        print("0. Terminer les lieux")
        choix = input("Votre choix : ").strip()

        if choix == "0":
            break

        elif choix == "1":
            lieux = gestion.get_lieux()
            if not lieux:
                print("❌ Aucun lieu existant.")
                continue
            for l in lieux:
                print(f"[{l.id_lieu}] {l.nom} ({l.adresse or 'sans adresse'})")
            try:
                lid = int(input("ID lieu à lier : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue
            if not gestion.get_lieu(lid):
                print("❌ Lieu introuvable.")
                continue
            gestion.lier_lieu_affaire(id_affaire, lid)
            print("✅ Lieu lié.")

        elif choix == "2":
            nom = saisie_obligatoire("Nom du lieu : ")
            adresse = input("Adresse (optionnelle) : ").strip() or None
            l = gestion.creer_lieu(nom, adresse, type=None, id_affaire=id_affaire)
            gestion.lier_lieu_affaire(id_affaire, l.id_lieu)
            print(f"✅ Lieu créé et lié (ID {l.id_lieu}).")

        elif choix == "3":
            if not lieux_actuels:
                print("❌ Aucun lieu à retirer.")
                continue
            try:
                lid = int(input("ID du lieu à retirer : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue
            if not any(l.id_lieu == lid for l in lieux_actuels):
                print("❌ Ce lieu n'est pas lié à cette affaire.")
                continue
            gestion.del_lieu_affaire(id_affaire, lid)
            print("✅ Lieu retiré de l'affaire.")
        else:
            print("❌ Choix invalide.")



def choisir_ou_creer_ville(code_postal_actuel: Optional[str], lieu_actuel: Optional[str]):

    while True:
        ville_str = f"{code_postal_actuel or '----'} {lieu_actuel or ''}".strip()
        print(f"\n🏙 Ville actuelle : {ville_str or 'Non définie'}")
        print("1. Choisir une ville existante")
        print("2. Créer une nouvelle ville")
        print("0. Garder la ville actuelle")
        choix = input("Votre choix : ").strip()

        if choix == "0" or choix == "":
            return code_postal_actuel, lieu_actuel

        elif choix == "1":
            villes = gestion.get_villes()
            if not villes:
                print("❌ Aucune ville existante. Créez-en une d'abord.")
                continue

            print("\nVilles existantes :")
            for cp, nom in villes:
                print(f"[{cp}] {nom}")

            cp = input("Code postal de la ville à utiliser (Entrée = annuler) : ").strip()
            if not cp:
                continue

            match = [v for v in villes if v[0] == cp]
            if not match:
                print("❌ Code postal inconnu.")
                continue

            return cp, match[0][1]

        elif choix == "2":
            cp = saisie_obligatoire("Nouveau code postal : ")
            nom_ville = saisie_obligatoire("Nom de la ville : ")
            gestion.creer_ville(cp, nom_ville)
            print("✅ Ville enregistrée.")
            return cp, nom_ville

        else:
            print("❌ Choix invalide.")



# ================================
#  AFFICHAGE
# ================================

def afficher_banniere():
    print("\n" + "="*50)
    print("🔍 GESTIONNAIRE D'AFFAIRES - ENQUÊTEUR")
    print("="*50)


def afficher_menu():
    print("\n1. Lister toutes les affaires")
    print("2. Filtrer les affaires")
    print("3. Créer une nouvelle affaire")
    print("4. Modifier une affaire")
    print("5. Supprimer une affaire")
    print("6. Visualiser les liens d'une affaire")
    print("0. Quitter")
    print("-"*50)


# ================================
#  ACTIONS
# ================================

def action_lister():
    affaires = gestion.get_affaires()
    if not affaires:
        print("❌ Aucune affaire trouvée.")
        return

    print("\n" + "═" * 60)
    print("📂 LISTE DES AFFAIRES")
    print("═" * 60)

    for a in affaires:
        suspects = a.get_suspects()
        armes = a.get_armes()
        lieux = a.get_lieux()

        # Ville (nom + CP)
        ville_str = "Non définie"
        if a.code_postal:
            vrows = gestion.get_villes()
            for cp, nom in vrows:
                if cp == a.code_postal:
                    ville_str = f"{nom} ({cp})"
                    break

        if lieux:
            texte_lieux = []
            for l in lieux:
                adr = l.adresse if l.adresse else "adresse inconnue"
                texte_lieux.append(f"{l.nom} ({adr})")
            lieux_str = "; ".join(texte_lieux)
        else:
            adr = "adresse inconnue"
            lieux_str = f"{a.lieu} ({adr})" if a.lieu else "Non précisé"

        print(f"\n🆔 Affaire #{a.id_affaire}  |  {a.titre}")
        print("─" * 60)
        print(f"📅 Date      : {a.date}")
        print(f"🏙 Ville     : {ville_str}")
        print(f"📍 Lieu(x)   : {lieux_str}")
        print(f"⚖️  Statut   : {a.statut}")
        print(f"📝 Desc.     : {a.description or 'Aucune description'}")


        if suspects:
            print("👥 Suspects  : ", end="")
            first = True
            for s in suspects:
                desc = f" — {s.description}" if s.description else ""
                line = f"{s.prenom} {s.nom}{desc}"
                if first:
                    print(line)
                    first = False
                else:
                    print(f"               {line}")
        else:
            print("👥 Suspects  : Aucun")

        if armes:
            print("🔪 Armes     : ", end="")
            first = True
            for ar in armes:
                pieces = [ar.type]
                if ar.numero_serie:
                    pieces.append(f"n° {ar.numero_serie}")
                if ar.description:
                    pieces.append(ar.description)
                line = " — ".join(pieces)
                if first:
                    print(line)
                    first = False
                else:
                    print(f"               {line}")
        else:
            print("🔪 Armes     : Aucune")

        print("─" * 60)

    print()




def action_filtre():
    print("\n📋 AFFAIRES DISPONIBLES :")
    lister_affaires_court()


    print("\n🔍 FILTRES DISPONIBLES:")
    print("1. Affaires en cours")
    print("2. Affaires classées")
    print("3. Rechercher un mot (titre/lieu/ville)")
    print("4. Entre deux dates")
    print("5. Par suspect")
    print("6. Par arme")
    print("0. Retour")
    print()

    choix = input("Votre choix : ").strip()

    if choix == "0":
        return

    affaires = gestion.get_affaires()


    if choix == "1":
        affaires = [a for a in affaires if a.statut.lower() == "en cours"]

    elif choix == "2":
        affaires = [a for a in affaires if a.statut.lower() == "classée"]

    elif choix == "3":
        texte = input("Mot à chercher : ").strip().lower()
        resultats = []
        for a in affaires:
            # titre + champ lieu
            haystack = [a.titre.lower(), (a.lieu or "").lower()]

            # ajouter le nom de ville si on le trouve
            nom_ville = None
            if a.code_postal:
                villes = gestion.get_villes()
                for cp, nom in villes:
                    if cp == a.code_postal:
                        nom_ville = nom
                        break
            if nom_ville:
                haystack.append(nom_ville.lower())

            if any(texte in h for h in haystack):
                resultats.append(a)
        affaires = resultats

    elif choix == "4":
        dmin = input("Date minimum (JJ-MM-AAAA, Entrée pour annuler) : ").strip()
        if dmin and not valider_date_fr(dmin):
            print("❌ Date minimum invalide, filtre annulé.")
            return

        dmax = input("Date maximum (JJ-MM-AAAA, Entrée pour annuler) : ").strip()
        if dmax and not valider_date_fr(dmax):
            print("❌ Date maximum invalide, filtre annulé.")
            return

        # si les deux sont vides, on annule aussi
        if not dmin and not dmax:
            print("ℹ️ Aucun intervalle fourni, retour au menu.")
            return

        # appliquer le filtre
        if dmin:
            affaires = [a for a in affaires if a.date >= dmin]
        if dmax:
            affaires = [a for a in affaires if a.date <= dmax]


    elif choix == "5":

        tous_suspects = gestion.get_suspects()
        if not tous_suspects:
            print("❌ Aucun suspect dans la base.")
            return

        print("\n👥 SUSPECTS DISPONIBLES :")
        for s in tous_suspects:
            print(f"[{s.id_suspect}] {s.prenom} {s.nom}")

        id_str = input("ID du suspect à filtrer : ").strip()
        try:
            sid = int(id_str)
        except ValueError:
            print("❌ ID invalide.")
            return


        resultats = []
        for a in affaires:
            ids = {s.id_suspect for s in a.get_suspects()}
            if sid in ids:
                resultats.append(a)
        affaires = resultats

    elif choix == "6":
        # Lister TOUTES les armes disponibles
        toutes_armes = gestion.get_armes()
        if not toutes_armes:
            print("❌ Aucune arme dans la base.")
            return

        print("\n🔪 ARMES DISPONIBLES :")
        for ar in toutes_armes:
            label = ar.type
            if ar.numero_serie:
                label += f" (n° {ar.numero_serie})"
            print(f"[{ar.id_arme}] {label}")

        id_str = input("ID de l'arme à filtrer : ").strip()
        try:
            aid = int(id_str)
        except ValueError:
            print("❌ ID invalide.")
            return

        # Filtrer les affaires qui ont cette arme liée
        resultats = []
        for a in affaires:
            ids = {ar.id_arme for ar in a.get_armes()}
            if aid in ids:
                resultats.append(a)
        affaires = resultats


    else:
        print("❌ Choix invalide.")
        return

    if not affaires:
        print("❌ Aucun résultat.")
        return

    print(f"\n📋 {len(affaires)} résultat(s):")
    print("═" * 60)
    for a in affaires:
        print(f"\n🆔 Affaire #{a.id_affaire}  |  {a.titre}")
        print("─" * 60)
        print(f"📅 Date      : {a.date}")
        ville_str = f"{a.lieu or 'Non définie'} ({a.code_postal or '----'})"
        print(f"🏙 Ville     : {ville_str}")
        print(f"⚖️  Statut   : {a.statut}")
        print(f"📝 Desc.     : {a.description or 'Aucune description'}")
        print("─" * 60)
    print()



def action_ajouter():
    print("\n➕ Création d'une nouvelle affaire")

    titre = saisie_obligatoire("Titre : ")
    date = saisie_date("Date (JJ-MM-AAAA) : ")
    statut = saisie_statut()
    description = input("Description (Entrée pour aucune) : ").strip() or None

    # Choix ville + code postal (obligatoire en création)
    while True:
        code_postal, nom_ville = choisir_ou_creer_ville(None, None)
        if code_postal and nom_ville:
            break
        print("❌ La ville est obligatoire pour créer une affaire.")

    lieu = nom_ville  # lieu principal par défaut = nom de la ville


    affaire = gestion.creer_affaire(titre, date, lieu, code_postal, statut, description)
    print(f"✅ Affaire créée ! ID: {affaire.id_affaire}\n")

    choisir_ou_creer_suspects(affaire.id_affaire)
    choisir_ou_creer_armes(affaire.id_affaire)
    choisir_ou_creer_lieux(affaire.id_affaire)




def action_modifier():
    # D'abord liste des affaires
    print("\n📋 LISTE DES AFFAIRES :")
    lister_affaires_court()

    id_str = input("\nID de l'affaire à modifier (0 pour retour) : ").strip()
    if id_str == "0":
        return

    try:
        id_affaire = int(id_str)
    except ValueError:
        print("❌ ID invalide.")
        return

    affaire = gestion.get_affaire(id_affaire)
    if not affaire:
        print("❌ Affaire introuvable.")
        return

    print(f"\n✏️ MODIFICATION COMPLÈTE [{affaire.id_affaire}] {affaire.titre}")
    print("Entrée = garder la valeur actuelle\n")

    # 1) Champs simples
    titre = saisie_libre_ou_defaut("Titre", affaire.titre)

    date_input = input(f"Date (JJ-MM-AAAA) [{affaire.date}] : ").strip()
    if date_input:
        if valider_date_fr(date_input):
            date = date_input
        else:
            print("❌ Date invalide, ancienne valeur conservée.")
            date = affaire.date
    else:
        date = affaire.date

    # Statut
    statut_input = input(f"Statut [{affaire.statut}] (1=en cours, 0=classée ou Entrée) : ").strip()
    if statut_input == "":
        statut = affaire.statut
    elif statut_input == "1":
        statut = "en cours"
    elif statut_input == "0":
        statut = "classée"
    else:
        print("❌ Saisie invalide, ancien statut conservé.")
        statut = affaire.statut

    description = saisir_desc = input(f"Description [{affaire.description or ''}] : ").strip()
    if saisir_desc == "":
        description = affaire.description

    # 2) Ville + code postal (menu complet)
    code_postal, lieu = choisir_ou_creer_ville(affaire.code_postal, affaire.lieu)


    # Application des modifications de base
    data = {
        "titre": titre,
        "date": date,
        "lieu": lieu,
        "code_postal": code_postal,
        "statut": statut,
        "description": description,
    }
    gestion.maj_affaire(id_affaire, data)
    print("✅ Informations générales de l'affaire mises à jour.\n")

    # 3) Modifier les suspects liés
    print("👥 Modification des suspects liés (optionnel)")
    print("Entrée = passer cette étape.")
    if input("Modifier les suspects ? (o/N) : ").strip().lower() == "o":

        choisir_ou_creer_suspects(id_affaire)

    # 4) Modifier les armes liées
    print("\n🔪 Modification des armes liées (optionnel)")
    if input("Modifier les armes ? (o/N) : ").strip().lower() == "o":
        choisir_ou_creer_armes(id_affaire)

    # 5) Modifier les lieux liés
    print("\n📍 Modification des lieux liés (optionnel)")
    if input("Modifier les lieux ? (o/N) : ").strip().lower() == "o":
        choisir_ou_creer_lieux(id_affaire)

    print("\n✅ Affaire modifiée !\n")



def action_supprimer():
    # D'abord liste des affaires
    print("\n📋 LISTE DES AFFAIRES :")
    lister_affaires_court()

    id_str = input("\nID de l'affaire à supprimer (0 pour retour) : ").strip()
    if id_str == "0":
        return

    try:
        id_affaire = int(id_str)
    except ValueError:
        print("❌ ID invalide.")
        return

    if input(f"Supprimer l'affaire {id_affaire} ? (o/N) : ").strip().lower() == 'o':
        gestion.supprimer_affaire(id_affaire)
        print("✅ Affaire supprimée !\n")
    else:
        print("❌ Annulé.\n")


def action_liens():
    # D'abord liste des affaires
    print("\n📋 LISTE DES AFFAIRES :")
    lister_affaires_court()

    id_str = input("\nID de l'affaire pour liens : ").strip()
    if id_str == "0":
        return

    try:
        id_affaire = int(id_str)
    except ValueError:
        print("❌ ID invalide.")
        return

    affaire_ref = gestion.get_affaire(id_affaire)
    if not affaire_ref:
        print("❌ Affaire introuvable.")
        return

    # Prépare les infos de référence
    lieux_ref = affaire_ref.get_lieux()
    suspects_ref = affaire_ref.get_suspects()
    armes_ref = affaire_ref.get_armes()

    ids_lieux_ref = {l.id_lieu for l in lieux_ref}
    ids_suspects_ref = {s.id_suspect for s in suspects_ref}
    ids_armes_ref = {a.id_arme for a in armes_ref}

    liens = []
    toutes = gestion.get_affaires()

    for autre in toutes:
        if autre.id_affaire == id_affaire:
            continue

        communs = []

        # Même date
        if autre.date == affaire_ref.date:
            communs.append(f"📅 Date: {affaire_ref.date}")

        # Même ville (code postal)
        if autre.code_postal and autre.code_postal == affaire_ref.code_postal:
            communs.append(f"🏙 Ville: même code postal ({affaire_ref.code_postal})")

        # Même lieu
        if autre.lieu and affaire_ref.lieu and autre.lieu.lower() == affaire_ref.lieu.lower():
            communs.append(f"📍 Lieu principal: {affaire_ref.lieu}")

        # Lieux liés communs
        lieux_autre = autre.get_lieux()
        ids_lieux_autre = {l.id_lieu for l in lieux_autre}
        lieux_communs_ids = ids_lieux_ref & ids_lieux_autre
        if lieux_communs_ids:
            noms = [l.nom for l in lieux_autre if l.id_lieu in lieux_communs_ids]
            communs.append("📍 Lieux liés: " + ", ".join(noms))

        # Suspects communs
        suspects_autre = autre.get_suspects()
        ids_suspects_autre = {s.id_suspect for s in suspects_autre}
        suspects_communs_ids = ids_suspects_ref & ids_suspects_autre
        if suspects_communs_ids:
            noms = [f"{s.prenom} {s.nom}" for s in suspects_autre if s.id_suspect in suspects_communs_ids]
            communs.append("👥 Suspects: " + ", ".join(noms))

        # Armes communes
        armes_autre = autre.get_armes()
        ids_armes_autre = {a.id_arme for a in armes_autre}
        armes_communes_ids = ids_armes_ref & ids_armes_autre
        if armes_communes_ids:
            types = [a.type for a in armes_autre if a.id_arme in armes_communes_ids]
            communs.append("🔪 Armes: " + ", ".join(types))

        if communs:
            liens.append((autre, communs))

    if not liens:
        print("❌ Aucun lien trouvé.")
    else:
        print(f"\n🔗 LIENS pour 🆔 Affaire #{affaire_ref.id_affaire} | {affaire_ref.titre}")
        print("═" * 60)
        for autre, communs in liens:
            print(f"\n🆔 Affaire liée #{autre.id_affaire}  |  {autre.titre}")
            print("─" * 60)
            print(f"📅 Date      : {autre.date}")
            print(f"🏙 Ville     : {autre.lieu or 'Non définie'} ({autre.code_postal or '----'})")
            print(f"⚖️  Statut   : {autre.statut}")
            print("🔍 Points communs :")
            for c in communs:
                print(f"   • {c}")
            print("─" * 60)
    print()



# ================================
#  BOUCLE PRINCIPALE
# ================================

def run_cli():
    afficher_banniere()

    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            action_lister()
        elif choix == "2":
            action_filtre()
        elif choix == "3":
            action_ajouter()
        elif choix == "4":
            action_modifier()
        elif choix == "5":
            action_supprimer()
        elif choix == "6":
            action_liens()
        elif choix == "0":
            print("👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide.\n")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    run_cli()
