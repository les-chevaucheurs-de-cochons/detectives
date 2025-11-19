from database import init_db, insert, get_all


def main():
    print("🔎 Initialisation de la base de données...")
    init_db()

    print("\n📌 Exemple : création d'une affaire")

    nouvelle_affaire = {
        "titre": "Vol au musée",
        "date": "2025-01-01",
        "lieu": "Bruxelles",
        "statut": "en cours",
        "description": "Un objet précieux a été dérobé."
    }

    id_affaire = insert("Affaire", nouvelle_affaire)
    print(f"✅ Affaire insérée avec l'ID : {id_affaire}")

    print("\n📋 Liste des affaires enregistrées :")
    affaires = get_all("Affaire")
    for a in affaires:
        print(a)


if __name__ == "__main__":
    main()
