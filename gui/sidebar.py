"""

Ce fichier a été réalisé dans le cadre d’un projet étudiant.
Certaines parties du code ont été générées ou assistées par une intelligence artificielle
(ChatGPT), puis relues, comprises et adaptées par l’étudiant.

"""

import tkinter as tk


class Sidebar(tk.Frame):
    """
    Barre latérale de l'application.
    Elle contient les boutons principaux (ajout, filtre, recentrage, aide)
    ainsi qu’un affichage du filtre actuellement actif.
    """

    def __init__(self, parent):
        """
        parent : fenêtre parente (MainWindow)
        """
        # Initialisation du Frame Tkinter
        super().__init__(parent, bg="#bbb", width=180)

        # Empêche le redimensionnement automatique selon le contenu
        self.pack_propagate(False)

        # ========================
        # TITRE
        # ========================
        tk.Label(
            self,
            text="Menu",
            bg="#bbb",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # ========================
        # BOUTONS PRINCIPAUX
        # ========================

        # Bouton pour créer une nouvelle affaire
        self.btn_add = tk.Button(self, text="➕ Nouvelle affaire")
        self.btn_add.pack(fill="x", padx=10, pady=5)

        # Bouton pour ouvrir la fenêtre de filtres
        self.btn_filter = tk.Button(self, text="🔍 Filtrer")
        self.btn_filter.pack(fill="x", padx=10, pady=5)

        # Bouton pour recentrer la vue du mur d’enquête
        self.btn_center = tk.Button(self, text="🎯 Recentrer la vue")
        self.btn_center.pack(fill="x", padx=10, pady=5)

        # Bouton pour réorganiser automatiquement les post-it
        self.btn_reset_layout = tk.Button(self, text="🧩 Réorganiser le mur")
        self.btn_reset_layout.pack(fill="x", padx=10, pady=5)

        # ========================
        # SÉPARATEUR VISUEL
        # ========================
        tk.Frame(self, height=2, bg="#999").pack(fill="x", pady=10)

        # ========================
        # AFFICHAGE DU FILTRE ACTIF
        # ========================
        tk.Label(
            self,
            text="Filtre actif :",
            bg="#bbb",
            anchor="w"
        ).pack(fill="x", padx=10)

        # Label mis à jour dynamiquement selon le filtre appliqué
        self.lbl_filter = tk.Label(
            self,
            text="Aucun",
            bg="#bbb",
            anchor="w",
            justify="left"
        )
        self.lbl_filter.pack(fill="x", padx=10, pady=(0, 10))

        # ========================
        # BOUTON AIDE
        # ========================
        self.btn_help = tk.Button(self, text="📖 Aide")
        self.btn_help.pack(fill="x", padx=10, pady=5)

    # ------------------------------------------------
    # LIAISON DES ACTIONS
    # ------------------------------------------------

    def set_actions(
            self,
            on_add=None,
            on_filter=None,
            on_center=None,
            on_reset_layout=None,
            on_help=None
    ):
        """
        Associe les fonctions passées en paramètre
        aux boutons correspondants de la sidebar.

        Cette méthode permet de séparer :
        - la logique métier (CanvasView / MainWindow)
        - l’interface graphique (Sidebar)
        """
        if on_add:
            self.btn_add.config(command=on_add)
        if on_filter:
            self.btn_filter.config(command=on_filter)
        if on_center:
            self.btn_center.config(command=on_center)
        if on_reset_layout:
            self.btn_reset_layout.config(command=on_reset_layout)
        if on_help:
            self.btn_help.config(command=on_help)

    # ------------------------------------------------
    # MISE À JOUR DU FILTRE
    # ------------------------------------------------

    def set_filter_text(self, text: str):
        """
        Met à jour le texte affiché indiquant
        le filtre actuellement actif.
        """
        self.lbl_filter.config(text=text or "Aucun")
