from backend.logger import setup_logger, get_logger
from database import init_db
from backend.auth import creer_admin_si_absent, login
from cli.affaires_cli import run_cli

setup_logger()
log = get_logger()

if __name__ == "__main__":
    init_db()
    log.info("Base de données initialisée (CLI)")

    creer_admin_si_absent()
    agent_id = login()
    log.info(f"Agent connecté (id={agent_id})")

    run_cli()
