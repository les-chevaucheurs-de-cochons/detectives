from database import init_db
from backend.gestion_enquete import GestionEnquetes
from gui.main_window import MainWindow

if __name__ == "__main__":
    init_db()
    gestion = GestionEnquetes()
    gui = MainWindow(gestion)
    gui.mainloop()
