"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Module standard de gestion des logs
import logging

# Modules système pour gérer les chemins
import os
import sys


# Détermine le chemin du fichier de log
def get_log_path():
    """
    Retourne un chemin de log compatible
    avec une exécution en script ou en .exe
    """

    # Si l'application est compilée (.exe)
    base_dir = (
        os.path.dirname(sys.executable)
        if getattr(sys, "frozen", False)
        else os.path.dirname(os.path.abspath(__file__))
    )

    # Dossier logs (créé si inexistant)
    log_dir = os.path.join(base_dir, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Fichier app.log
    return os.path.join(log_dir, "app.log")


# Configure le système de logs
def setup_logger():
    log_path = get_log_path()

    logging.basicConfig(
        # Niveau minimum des logs
        level=logging.INFO,

        # Format d’affichage des logs
        format="%(asctime)s | %(levelname)s | %(message)s",

        # Format de la date
        datefmt="%d-%m-%Y %H:%M:%S",

        # Sortie vers fichier + console
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()  # affichage CLI
        ],
    )

    # Log de démarrage de l’application
    logging.info("=== Application démarrée ===")


# Retourne le logger principal de l’application
def get_logger():
    return logging.getLogger("detectives")
