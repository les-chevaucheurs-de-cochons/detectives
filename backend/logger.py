import logging
import os
import sys


def get_log_path():
    """
    Retourne un chemin de log compatible exe / script
    """
    base_dir = (
        os.path.dirname(sys.executable)
        if getattr(sys, "frozen", False)
        else os.path.dirname(os.path.abspath(__file__))
    )
    log_dir = os.path.join(base_dir, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "app.log")


def setup_logger():
    log_path = get_log_path()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()  # console (CLI)
        ],
    )

    logging.info("=== Application démarrée ===")


def get_logger():
    return logging.getLogger("detectives")