"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Permet de se connecter à la base de données
from database import get_connection

# Sert à masquer le mot de passe lors de la saisie
import getpass

# Logger pour garder une trace des actions (connexion, erreurs, etc.)
from backend.logger import get_logger

# Initialisation du logger
log = get_logger()


# Vérifie s’il existe au moins un agent dans la base
def has_agent():
    # Connexion à la base
    conn = get_connection()
    cur = conn.cursor()

    # Compte le nombre d’agents
    cur.execute("SELECT COUNT(*) FROM Agent")
    count = cur.fetchone()[0]

    # Fermeture de la connexion
    conn.close()

    # Log informatif
    log.info(f"Vérification agents existants : {count} trouvé(s)")

    # Retourne True s’il existe au moins un agent
    return count > 0


# Crée un nouvel agent (identifiant + mot de passe)
def create_agent(identifiant, password):
    conn = get_connection()
    cur = conn.cursor()

    # Insertion de l’agent dans la table Agent
    cur.execute(
        "INSERT INTO Agent (identifiant, password) VALUES (?, ?)",
        (identifiant, password)
    )

    # Validation de l’insertion
    conn.commit()
    conn.close()

    # Log de création
    log.info(f"Création d'un agent : identifiant='{identifiant}'")


# Authentifie un agent (utilisé hors CLI)
def authenticate(identifiant, password):
    conn = get_connection()
    cur = conn.cursor()

    # Recherche de l’agent correspondant
    cur.execute(
        "SELECT id_agent FROM Agent WHERE identifiant=? AND password=?",
        (identifiant, password)
    )

    row = cur.fetchone()
    conn.close()

    # Si l’agent existe → succès
    if row:
        log.info(f"Connexion réussie : identifiant='{identifiant}'")
        return row[0]

    # Sinon → échec
    log.warning(f"Échec de connexion : identifiant='{identifiant}'")
    return None


# Crée automatiquement un compte admin si aucun agent n’existe
def creer_admin_si_absent():
    """
    Crée un compte admin par défaut si aucun agent n'existe.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Vérifie s’il existe déjà un agent
    cur.execute("SELECT COUNT(*) FROM Agent")
    count = cur.fetchone()[0]

    # Si aucun agent → création admin
    if count == 0:
        log.warning("Aucun agent trouvé, création d'un compte administrateur")

        print("🔐 Aucun utilisateur trouvé.")
        print("➡️ Création d'un compte administrateur.")

        # Saisie sécurisée des identifiants
        identifiant = input("Identifiant admin : ")
        password = getpass.getpass("Mot de passe : ")

        # Insertion de l’admin
        cur.execute(
            "INSERT INTO Agent (identifiant, password) VALUES (?, ?)",
            (identifiant, password)
        )
        conn.commit()

        log.info(f"Compte administrateur créé : identifiant='{identifiant}'")
        print("✅ Compte administrateur créé.\n")

    # Fermeture connexion DB
    conn.close()


# Procédure de connexion en ligne de commande (CLI)
def login():
    """
    Demande une authentification utilisateur.
    """
    conn = get_connection()
    cur = conn.cursor()

    print("🔐 Connexion requise\n")
    log.info("Tentative de connexion utilisateur (CLI)")

    # Autorise maximum 3 tentatives
    for tentative in range(1, 4):
        identifiant = input("Identifiant : ")
        password = getpass.getpass("Mot de passe : ")

        # Vérification des identifiants
        cur.execute(
            "SELECT id_agent FROM Agent WHERE identifiant = ? AND password = ?",
            (identifiant, password)
        )

        row = cur.fetchone()

        # Connexion réussie
        if row:
            conn.close()
            log.info(
                f"Connexion réussie (CLI) : identifiant='{identifiant}' "
                f"(tentative {tentative})"
            )
            print("✅ Connexion réussie.\n")
            return row[0]

        # Connexion échouée
        log.warning(
            f"Échec connexion (CLI) : identifiant='{identifiant}' "
            f"(tentative {tentative})"
        )
        print("❌ Identifiant ou mot de passe incorrect.\n")

    # Après 3 échecs → arrêt du programme
    conn.close()
    log.error("Blocage après 3 tentatives de connexion (CLI)")
    raise SystemExit("⛔ Trop de tentatives. Fermeture.")
