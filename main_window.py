from backend.logger import setup_logger, get_logger
from database import init_db
from backend.gestion_enquete import GestionEnquetes
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
import tkinter as tk

setup_logger()
log = get_logger()

if __name__ == "__main__":
    init_db()
    log.info("Base de données initialisée (GUI)")

    root = tk.Tk()
    root.withdraw()

    def start_app():
        log.info("Ouverture de la fenêtre principale")
        root.destroy()
        app = MainWindow(GestionEnquetes())
        app.mainloop()

    LoginWindow(root, on_success=start_app)
    root.mainloop()