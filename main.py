import random
from database import init_db, insert, get_all
from backend.gestion_enquete import GestionEnquetes
from gui.main_window import MainWindow


if __name__ == "__main__":
    print("🔎 Initialisation de la base de données...")
    init_db()

    gestion = GestionEnquetes()

    gui = MainWindow(gestion)
    gui.mainloop()
