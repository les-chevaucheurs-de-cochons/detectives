from backend import GestionEnquetes
from database import init_db
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
    """Affiche la liste des affaires (version courte pour actions)"""
    affaires = gestion.get_affaires()
    if not affaires:
        print("❌ Aucune affaire trouvée.")
        return []
    print(f"\n📋 {len(affaires)} affaire(s) :")
    for a in affaires:
        print(f"[{a.id_affaire}] {a.titre} | {a.date} | {a.lieu}")
    return affaires


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

    print(f"\n📋 {len(affaires)} affaire(s) trouvée(s):")
    for a in affaires:
        desc = a.description or "Aucune"
        print(f"[{a.id_affaire}] {a.titre} | {a.date} | {a.lieu} | {a.statut}")
        print(f"    {desc}")
    print()


def action_filtre():
    # D'abord liste des affaires
    lister_affaires_court()

    print("\n🔍 FILTRES DISPONIBLES:")
    print("1. Affaires en cours")
    print("2. Affaires classées")
    print("3. Rechercher un mot (titre/lieu)")
    print("4. Entre deux dates")
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
        affaires = [a for a in affaires if texte in a.titre.lower() or texte in a.lieu.lower()]
    elif choix == "4":
        dmin = saisie_date("Date minimum (JJ-MM-AAAA)")
        dmax = saisie_date("Date maximum (JJ-MM-AAAA)")
        affaires = [a for a in affaires if dmin <= a.date <= dmax]
    else:
        print("❌ Choix invalide.")
        return

    if not affaires:
        print("❌ Aucun résultat.")
    else:
        print(f"\n📋 {len(affaires)} résultat(s):")
        for a in affaires:
            print(f"[{a.id_affaire}] {a.titre} ({a.date}, {a.lieu})")
    print()


def action_ajouter():
    print("\n➕ Création d'une nouvelle affaire")

    titre = saisie_obligatoire("Titre : ")
    date = saisie_date("Date (JJ-MM-AAAA) : ")
    lieu = saisie_obligatoire("Lieu : ")
    statut = saisie_statut()  # ← NOUVEAU : 1/0
    description = input("Description (Entrée pour aucune) : ").strip() or None

    affaire = gestion.creer_affaire(titre, date, lieu, statut, description)
    print(f"✅ Affaire créée ! ID: {affaire.id_affaire}\n")


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

    print(f"\n✏️ MODIFICATION [{affaire.id_affaire}] {affaire.titre}")
    print("Entrée = garder la valeur actuelle\n")

    titre = saisie_libre_ou_defaut("Titre", affaire.titre)
    date = saisie_date("Date (JJ-MM-AAAA)", affaire.date)
    lieu = saisie_libre_ou_defaut("Lieu", affaire.lieu)
    statut = saisie_statut() if input(f"Statut [{affaire.statut}] (1/0 ou Entrée) : ").strip() else affaire.statut
    description = saisie_libre_ou_defaut("Description", affaire.description or "")

    data = {
        "titre": titre,
        "date": date,
        "lieu": lieu,
        "statut": statut,
        "description": description if description else None
    }

    gestion.maj_affaire(id_affaire, data)
    print("✅ Affaire modifiée !\n")


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

    id_str = input("\nID de l'affaire pour liens (0 pour retour) : ").strip()
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

    # Liens simples (date + lieu)
    liens = []
    toutes = gestion.get_affaires()

    for autre in toutes:
        if autre.id_affaire == id_affaire:
            continue

        communs = []

        # Même date
        if autre.date == affaire_ref.date:
            communs.append(f"date: {affaire_ref.date}")

        # Même lieu
        if autre.lieu.lower() == affaire_ref.lieu.lower():
            communs.append(f"lieu: {affaire_ref.lieu}")

        if communs:
            liens.append((autre, communs))

    if not liens:
        print("❌ Aucun lien trouvé.")
    else:
        print(f"\n🔗 LIENS pour [{affaire_ref.id_affaire}] {affaire_ref.titre}:")
        for autre, communs in liens:
            print(f"- [{autre.id_affaire}] {autre.titre}: {', '.join(communs)}")
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
