import argparse
from database import init_db
from backend import GestionEnquetes

# Instance centrale de gestion des enquêtes
gestion = GestionEnquetes()


def cmd_creer(args):
    id_affaire = gestion.creer_affaire(
        titre=args.titre,
        date=args.date,
        lieu=args.lieu,
        statut=args.statut,
        description=args.description,
    )
    print(f"✅ Affaire créée avec l'ID : {id_affaire}")


def cmd_lister(_args):
    affaires = gestion.get_affaires()
    if not affaires:
        print("Aucune affaire enregistrée.")
        return

    print("📋 Affaires enregistrées :")
    for a in affaires:
        # a = (id_affaire, titre, date, lieu, statut, description)
        print(f"[{a[0]}] {a[1]} – {a[2]} – {a[3]} – {a[4]} – {a[5]}")


def cmd_modifier(args):
    # On ne met à jour que les champs donnés
    data = {}
    if args.titre is not None:
        data["titre"] = args.titre
    if args.date is not None:
        data["date"] = args.date
    if args.lieu is not None:
        data["lieu"] = args.lieu
    if args.statut is not None:
        data["statut"] = args.statut
    if args.description is not None:
        data["description"] = args.description

    # Vérifie qu'il y a au moins un champ à modifier
    if not data:
        print("Aucun champ à modifier n'a été fourni.")
        return

    gestion.maj_affaire(args.id, data)
    print(f"✏️ Affaire {args.id} mise à jour.")


def cmd_supprimer(args):
    gestion.supprimer_affaire(args.id)
    print(f"🗑️ Affaire {args.id} supprimée.")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="affaire",
        description="Gestion des affaires criminelles (CLI)"
    )

    subparsers = parser.add_subparsers(dest="commande", required=True)

    # --- affaire creer ---
    p_creer = subparsers.add_parser("creer", help="Créer une nouvelle affaire")
    p_creer.add_argument("titre", help="Titre de l'affaire")
    p_creer.add_argument("date", help="Date (format libre, ex: 2025-01-01)")
    p_creer.add_argument("lieu", help="Lieu de l'affaire")
    p_creer.add_argument("statut", help="Statut de l'affaire")
    p_creer.add_argument(
        "--description",
        "-d",
        default="",
        help="Description de l'affaire"
    )
    p_creer.set_defaults(func=cmd_creer)

    # --- affaire lister ---
    p_lister = subparsers.add_parser("lister", help="Lister toutes les affaires")
    p_lister.set_defaults(func=cmd_lister)

    # --- affaire modifier ---
    p_modifier = subparsers.add_parser("modifier", help="Modifier une affaire")
    p_modifier.add_argument("id", type=int, help="ID de l'affaire à modifier")
    p_modifier.add_argument("--titre")
    p_modifier.add_argument("--date")
    p_modifier.add_argument("--lieu")
    p_modifier.add_argument("--statut")
    p_modifier.add_argument("--description")
    p_modifier.set_defaults(func=cmd_modifier)

    # --- affaire supprimer ---
    p_supprimer = subparsers.add_parser("supprimer", help="Supprimer une affaire")
    p_supprimer.add_argument("id", type=int, help="ID de l'affaire à supprimer")
    p_supprimer.set_defaults(func=cmd_supprimer)

    return parser


def main():
    # Initialise la base avant d'utiliser la gestion des enquêtes
    init_db()

    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()