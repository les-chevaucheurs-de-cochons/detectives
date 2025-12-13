from database import init_db
from backend.gestion_enquete import GestionEnquetes
from gui.main_window import MainWindow
from cli.affaires_cli import run_cli

if __name__ == "__main__":
    print("🔎 Initialisation de la base de données...")
    init_db()

    print("1 = Mode CLI (terminal)")
    print("2 = Mode GUI (interface graphique)")
    mode = input("Votre choix (1/2) : ").strip()

    if mode == "1":
        # Lancement du CLI
        run_cli()
    else:
        # Lancement de la GUI
        gestion = GestionEnquetes()
        gui = MainWindow(gestion)
        gui.mainloop()
