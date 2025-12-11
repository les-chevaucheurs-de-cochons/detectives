from database import init_db
from backend import GestionEnquetes

gestion = GestionEnquetes()


def afficher_banniere():
    print("_________________________________")
    print("|    Gestionnaire des affaires   |")
    print("_________________________________")
    print()


def afficher_menu_principal():
    print("[lister]    Lister les affaires")
    print("[filtre]    Filtrer les affaires")
    print("[ajouter]   Ajouter une nouvelle affaire")
    print("[modifier]  Modifier une affaire existante")
    print("[supprimer] Supprimer une affaire")
    print("[quitter]   Quitter")
    print()


def action_lister():
    affaires = gestion.get_affaires()
    if not affaires:
        print("Aucune affaire enregistrée.")
        print()
        return

    print("📋 Affaires :")
    for a in affaires:
        # a = (id_affaire, titre, date, lieu, statut, description)
        print(f"[{a[0]}] {a[1]} – {a[2]} – {a[3]} – {a[4]} – {a[5]}")
    print()

    print("Vous pouvez :")
    print(" - taper [filtre] pour filtrer les affaires")
    print(" - taper [retour] pour revenir au menu principal")
    print()
    # boucle pour gérer le sous-choix
    while True:
        choix = input("Commande (filtre/retour) : ").strip().lower()
        if choix == "filtre":
            action_filtre()
            break
        elif choix == "retour":
            break
        else:
            print("Commande inconnue, merci de taper 'filtre' ou 'retour'.")


def action_filtre():
    while True:
        print("Filtres disponibles :")
        print("[statut1] Affaires en cours")
        print("[statut0] Affaires classées")
        print("[retour]  Revenir au menu principal")
        print()
        choix = input("Votre choix de filtre : ").strip().lower()

        if choix == "retour":
            print()
            return

        affaires = gestion.get_affaires()

        if choix == "statut1":
            affaires = [a for a in affaires if a[4] == "en cours"]
        elif choix == "statut0":
            affaires = [a for a in affaires if a[4] == "classée"]
        else:
            print("⚠️ Filtre inconnu, réessayez.")
            print()
            continue

        if not affaires:
            print("Aucune affaire trouvée pour ce filtre.")
        else:
            print("📋 Résultats du filtre :")
            for a in affaires:
                print(f"[{a[0]}] {a[1]} – {a[2]} – {a[3]} – {a[4]}")
        print()
        # Après un filtrage, on revient au sous-menu filtre
        # (boucle while continue)


def action_ajouter():
    print("Ajout d'une nouvelle affaire :")

    # Boucles pour champs obligatoires
    while True:
        titre = input("Titre : ").strip()
        if titre:
            break
        print("Le titre est obligatoire.")

    while True:
        date = input("Date (ex: 2025-01-01) : ").strip()
        if date:
            break
        print("La date est obligatoire.")

    while True:
        lieu = input("Lieu : ").strip()
        if lieu:
            break
        print("Le lieu est obligatoire.")

    while True:
        statut = input("Statut (en cours / classée / ...) : ").strip()
        if statut:
            break
        print("Le statut est obligatoire.")

    description = input("Description (optionnelle) : ").strip() or None

    id_affaire = gestion.creer_affaire(titre, date, lieu, statut, description)
    print(f"✅ Affaire créée avec l'ID : {id_affaire}")
    print()


def action_modifier():
    # Boucle pour ID valide
    while True:
        id_str = input("ID de l'affaire à modifier (ou 'retour') : ").strip().lower()
        if id_str == "retour":
            print()
            return
        try:
            id_affaire = int(id_str)
            break
        except ValueError:
            print("⚠️ Merci d'entrer un ID numérique.")

    affaire = gestion.get_affaire(id_affaire)
    if not affaire:
        print("Affaire introuvable.")
        print()
        return

    print(f"Modification de l'affaire [{affaire[0]}] {affaire[1]}")
    titre = input(f"Titre [{affaire[1]}] : ").strip() or affaire[1]
    date = input(f"Date [{affaire[2]}] : ").strip() or affaire[2]
    lieu = input(f"Lieu [{affaire[3]}] : ").strip() or affaire[3]
    statut = input(f"Statut [{affaire[4]}] : ").strip() or affaire[4]
    description = input(f"Description [{affaire[5]}] : ").strip() or affaire[5]

    data = {
        "titre": titre,
        "date": date,
        "lieu": lieu,
        "statut": statut,
        "description": description,
    }
    gestion.maj_affaire(id_affaire, data)
    print("✏️ Affaire mise à jour.")
    print()


def action_supprimer():
    while True:
        id_str = input("ID de l'affaire à supprimer (ou 'retour') : ").strip().lower()
        if id_str == "retour":
            print()
            return
        try:
            id_affaire = int(id_str)
            break
        except ValueError:
            print("⚠️ Merci d'entrer un ID numérique.")

    confirm = input(f"Confirmer la suppression de l'affaire {id_affaire} ? (o/N) : ").strip().lower()
    if confirm == "o":
        gestion.supprimer_affaire(id_affaire)
        print(f"🗑️ Affaire {id_affaire} supprimée.")
    else:
        print("Suppression annulée.")
    print()


def main():
    init_db()
    afficher_banniere()

    while True:
        afficher_menu_principal()
        choix = input("Votre choix : ").strip().lower()

        # boucle de validation simple
        if choix == "lister":
            action_lister()
        elif choix == "filtre":
            action_filtre()
        elif choix == "ajouter":
            action_ajouter()
        elif choix == "modifier":
            action_modifier()
        elif choix == "supprimer":
            action_supprimer()
        elif choix == "quitter":
            print("Au revoir.")
            break
        else:
            print("⚠️ Choix inconnu, merci de taper une commande proposée.")
            print()


if __name__ == "__main__":
    main()
