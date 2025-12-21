"""
Ce fichier a été développé dans le cadre d’un projet étudiant.
Certaines parties du code ont été générées ou assistées par une intelligence artificielle
(ChatGPT), puis relues, comprises et adaptées par l’étudiant.

"""

import tkinter as tk


class LiensPopup(tk.Toplevel):
    """
    Fenêtre popup affichant les éléments communs entre plusieurs affaires.
    Elle est utilisée lorsque l’utilisateur clique sur un lien dans le mur d’enquête.
    """

    def __init__(self, parent, communs):
        """
        Constructeur de la fenêtre popup.

        parent  : fenêtre parente (MainWindow)
        communs : liste de chaînes représentant les éléments communs
                  (suspects, armes, lieux, etc.)
        """
        super().__init__(parent)

        # Titre de la fenêtre
        self.title("🔗 Liens communs")

        # Affichage de chaque élément commun sous forme de liste
        for c in communs:
            tk.Label(
                self,
                text="• " + c
            ).pack(anchor="w", padx=10)

        # Configuration de la fenêtre comme popup modale
        self.transient(parent)   # liée à la fenêtre parente
        self.grab_set()          # bloque les interactions avec la fenêtre principale
        self.focus_set()         # donne le focus à la popup
        self.lift()              # place la popup au premier plan
