import tkinter as tk
from tkinter import messagebox

from gui.sidebar import Sidebar
from gui.canvas_view import CanvasView


class MainWindow(tk.Tk):

    @property
    def titre(self) -> str:
        return self._titre

    @titre.setter
    def titre(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Le titre doit être une chaine non vide")

        self._titre = value
        self.title(value)


    @property
    def icon(self) -> str | None:
        return self._icon_path

    @icon.setter
    def icon(self, value: str):
        assert isinstance(value, str) and value.strip(), "le chemin de l'icone doit être une chaîne non vide"

        self._icon_path = value

        try:
            self.iconbitmap(value)
        except Exception:
            pass
        assert self._icon_path == value, "l'icone n'a pas été correctement définie"



    def __init__(self, gestion):
        super().__init__()
        self.gestion = gestion

        self._titre = None
        self.titre = "Mur d'enquête"

        self.geometry("1200x700")
        self.configure(bg="#ddd")

        self._icon_path = None
        self.icon = "icon.ico"




        self.sidebar = Sidebar(self)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Canvas (mur d'enquête)
        self.canvas_view = CanvasView(self, gestion)
        self.canvas_view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas_view.on_filter_changed = self.sidebar.set_filter_text

        # Menu en haut
        self._create_menu()

        # Actions sidebar
        self.sidebar.set_actions(
            on_add=self.canvas_view.ajouter_affaire,
            on_filter=self.canvas_view.filtrer_affaires,
            on_center=self.canvas_view.reset_view,
            on_reset_layout=self.canvas_view.relayout_affaires,
            on_help=self._help
        )


    # ------------------------------------------------

    def _create_menu(self):
        menubar = tk.Menu(self)

        self.menu_label = [
            "Nouvelle affaire",
            "Filtrer les affaires",
            "Réinitialiser le filtre",
            "Quitter"
        ]


        # ===== Menu Affaire =====
        menu_affaire = tk.Menu(menubar, tearoff=0)
        menu_affaire.add_command(
            label=self.menu_label[0],
            command=self.canvas_view.ajouter_affaire
        )
        menu_affaire.add_command(
            label=self.menu_label[1],
            command=self.canvas_view.filtrer_affaires
        )
        menu_affaire.add_command(
            label=self.menu_label[2],
            command=self.canvas_view.reset_filtre
        )
        menu_affaire.add_command(
            label=self.menu_label[3],
            command=self.quit
        )

        menubar.add_cascade(label="Affaire", menu=menu_affaire)

        # ===== Menu Aide =====
        menu_aide = tk.Menu(menubar, tearoff=0)
        menu_aide.add_command(
            label="📖 Aide / Utilisation",
            command=self._help
        )
        menu_aide.add_separator()
        menu_aide.add_command(
            label="À propos",
            command=self._about
        )
        menubar.add_cascade(label="Aide", menu=menu_aide)

        self.config(menu=menubar)

    # ------------------------------------------------

    def _about(self):
        messagebox.showinfo(
            "À propos",
            "Logiciel de gestion d’enquêtes criminelles\n"
            "Projet Python – GUI + CLI\n\n"
            "Développé en Python avec Tkinter et SQLite."
        )

    # ------------------------------------------------

    def _help(self):
        messagebox.showinfo(
            "Aide – Utilisation de l'application",
            "🧱 Mur d'enquête\n"
            "• Clic droit + glisser : déplacer le mur\n\n"

            "📌 Post-it (affaires)\n"
            "• Clic gauche + glisser : déplacer une affaire\n"
            "• Double-clic : modifier l'affaire\n\n"

            "➕ Gestion des affaires\n"
            "• Menu Affaire → Nouvelle affaire\n"
            "• Sidebar ou menu pour filtrer les affaires\n\n"

            "🔗 Liens entre affaires\n"
            "• Les lignes indiquent des éléments communs\n"
            "• Cliquer sur une ligne affiche les liens\n\n"

            "💾 Sauvegarde\n"
            "• Les modifications sont enregistrées automatiquement\n"
        )
