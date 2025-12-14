from database import get_connection
import getpass

from backend.logger import get_logger

log = get_logger()


def has_agent():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Agent")
    count = cur.fetchone()[0]
    conn.close()

    log.info(f"Vérification agents existants : {count} trouvé(s)")
    return count > 0


def create_agent(identifiant, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Agent (identifiant, password) VALUES (?, ?)",
        (identifiant, password)
    )
    conn.commit()
    conn.close()

    log.info(f"Création d'un agent : identifiant='{identifiant}'")


def authenticate(identifiant, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_agent FROM Agent WHERE identifiant=? AND password=?",
        (identifiant, password)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        log.info(f"Connexion réussie : identifiant='{identifiant}'")
        return row[0]

    log.warning(f"Échec de connexion : identifiant='{identifiant}'")
    return None


def creer_admin_si_absent():
    """
    Crée un compte admin par défaut si aucun agent n'existe.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Agent")
    count = cur.fetchone()[0]

    if count == 0:
        log.warning("Aucun agent trouvé, création d'un compte administrateur")

        print("🔐 Aucun utilisateur trouvé.")
        print("➡️ Création d'un compte administrateur.")

        identifiant = input("Identifiant admin : ")
        password = getpass.getpass("Mot de passe : ")

        cur.execute(
            "INSERT INTO Agent (identifiant, password) VALUES (?, ?)",
            (identifiant, password)
        )
        conn.commit()

        log.info(f"Compte administrateur créé : identifiant='{identifiant}'")
        print("✅ Compte administrateur créé.\n")

    conn.close()


def login():
    """
    Demande une authentification utilisateur.
    """
    conn = get_connection()
    cur = conn.cursor()

    print("🔐 Connexion requise\n")
    log.info("Tentative de connexion utilisateur (CLI)")

    for tentative in range(1, 4):
        identifiant = input("Identifiant : ")
        password = getpass.getpass("Mot de passe : ")

        cur.execute(
            "SELECT id_agent FROM Agent WHERE identifiant = ? AND password = ?",
            (identifiant, password)
        )

        row = cur.fetchone()
        if row:
            conn.close()
            log.info(
                f"Connexion réussie (CLI) : identifiant='{identifiant}' "
                f"(tentative {tentative})"
            )
            print("✅ Connexion réussie.\n")
            return row[0]

        log.warning(
            f"Échec connexion (CLI) : identifiant='{identifiant}' "
            f"(tentative {tentative})"
        )
        print("❌ Identifiant ou mot de passe incorrect.\n")

    conn.close()
    log.error("Blocage après 3 tentatives de connexion (CLI)")
    raise SystemExit("⛔ Trop de tentatives. Fermeture.")