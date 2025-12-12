import tkinter as tk
from tkinter import ttk

from gui.help_window import HelpWindow
from gui.canvas_board import CanvasBoard
from gui.generic_create_window import GenericCreateWindow
from gui.link_window import LinkWindow


class MainWindow(tk.Tk):
    def __init__(self, gestion):
        super().__init__()

        self.title("🕵️ Gestion des Enquêtes - GUI")
        self.geometry("1200x700")
        self.minsize(900, 600)

        self.gestion = gestion  # Instance GestionEnquetes()

        # --------------------------
        # MENU
        # --------------------------
        menubar = tk.Menu(self)
        menu_fichier = tk.Menu(menubar, tearoff=0)
        menu_fichier.add_command(label="Quitter", command=self.quit)

        menubar.add_cascade(label="Fichier", menu=menu_fichier)
        self.config(menu=menubar)

        # --------------------------
        # PANNEAU LATÉRAL
        # --------------------------
        sidebar = ttk.Frame(self, width=250, padding=10)
        sidebar.pack(side="left", fill="y")

        # ----- BOUTONS CRÉATION -----
        ttk.Button(sidebar, text="➕ Nouvelle affaire",
                   command=lambda: self.open_create("Affaire")
                   ).pack(fill="x", pady=5)

        ttk.Button(sidebar, text="➕ Nouveau suspect",
                   command=lambda: self.open_create("Suspect")
                   ).pack(fill="x", pady=5)

        ttk.Button(sidebar, text="➕ Nouvelle preuve",
                   command=lambda: self.open_create("Preuve")
                   ).pack(fill="x", pady=5)

        ttk.Button(sidebar, text="➕ Nouvelle arme",
                   command=lambda: self.open_create("Arme")
                   ).pack(fill="x", pady=5)

        ttk.Button(sidebar, text="➕ Nouveau lieu",
                   command=lambda: self.open_create("Lieu")
                   ).pack(fill="x", pady=5)

        # ----- LIENS -----
        ttk.Button(sidebar, text="🔗 Créer un lien",
                   command=self.open_link_window
                   ).pack(fill="x", pady=5)

        ttk.Button(sidebar, text="Actualiser",
                   command=self.refresh_board
                   ).pack(fill="x", pady=5)

        ttk.Button(sidebar, text="❓ Aide",
                   command=self.open_help_window
                   ).pack(fill="x", pady=5)




        # --------------------------
        # ZONE PRINCIPALE : CANVAS
        # --------------------------
        self.board = CanvasBoard(self)
        self.board.pack(side="right", fill="both", expand=True)

        self.refresh_board()

    # =====================================================
    #   Mise à jour de l'affichage
    # =====================================================
    def refresh_board(self):
        self.board.display_all()

    # =====================================================
    #   FENÊTRES CRÉATION
    # =====================================================
    def open_create(self, entity_type):
        """
        DOIT respecter la signature :
        GenericCreateWindow(parent, entity_type, gestion, refresh_callback)
        """
        GenericCreateWindow(
            parent=self,
            entity_type=entity_type,
            gestion=self.gestion,
            refresh_callback=self.refresh_board
        )

    # =====================================================
    #   LIENS
    # =====================================================
    def open_link_window(self):
        LinkWindow(self, self.gestion, self.refresh_board)

    def open_help_window(self):
        HelpWindow(self)


