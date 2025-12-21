"""

Ce fichier a été développé dans le cadre d’un projet étudiant.
Certaines parties du code ont été générées ou assistées par une intelligence artificielle
(ChatGPT), puis relues, comprises et adaptées par l’étudiant.

"""

import tkinter as tk
from tkinter import simpledialog, messagebox


class SuspectsPanel(tk.Frame):
    """
    Panneau graphique permettant de gérer les suspects liés à une affaire.
    Ce panneau est intégré dans l’interface graphique principale (GUI).
    """

    def __init__(self, parent, gestion, affaire):
        """
        Constructeur du panneau des suspects.

        parent  : widget parent (Notebook / Frame)
        gestion : instance de GestionEnquetes (logique métier)
        affaire : affaire actuellement sélectionnée
        """
        super().__init__(parent)

        # Références vers la logique métier et l'affaire courante
        self.gestion = gestion
        self.affaire = affaire

        # Listbox affichant les suspects liés à l'affaire
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame contenant les boutons d’action
        btns = tk.Frame(self)
        btns.pack(fill="x")

        # Bouton pour créer un nouveau suspect
        tk.Button(btns, text="➕ Nouveau", command=self.add_new).pack(side="left", padx=2)

        # Bouton pour lier un suspect existant
        tk.Button(btns, text="🔗 Lier existant", command=self.link_existing).pack(side="left", padx=2)

        # Bouton pour modifier un suspect existant
        tk.Button(btns, text="✏️ Éditer", command=self.edit).pack(side="left", padx=2)

        # Bouton pour retirer le lien entre un suspect et l’affaire
        tk.Button(btns, text="❌ Retirer", command=self.remove).pack(side="left", padx=2)

        # Chargement initial de la liste
        self.refresh()

    # -----------------------------
    # MÉTHODES UTILITAIRES
    # -----------------------------

    def refresh(self):
        """
        Met à jour la liste des suspects affichés.
        Les suspects sont récupérés depuis l’objet affaire.
        """
        self.listbox.delete(0, tk.END)

        for s in self.affaire.get_suspects():
            # Affichage sous la forme "Prénom Nom"
            self.listbox.insert(tk.END, f"{s.prenom} {s.nom}")

    def _selected(self):
        """
        Retourne le suspect actuellement sélectionné dans la liste.
        Si aucun suspect n’est sélectionné, retourne None.
        """
        idx = self.listbox.curselection()
        if not idx:
            return None

        return self.affaire.get_suspects()[idx[0]]

    # -----------------------------
    # ACTIONS UTILISATEUR
    # -----------------------------

    def add_new(self):
        """
        Crée un nouveau suspect et le lie immédiatement à l’affaire.
        """
        prenom = simpledialog.askstring("Suspect", "Prénom :")
        nom = simpledialog.askstring("Suspect", "Nom :")

        # Vérification des champs obligatoires
        if not prenom or not nom:
            return

        # Création du suspect via la couche métier
        s = self.gestion.creer_suspect(nom, prenom)

        # Liaison du suspect avec l’affaire
        self.gestion.lier_suspect_affaire(self.affaire.id_affaire, s.id_suspect)

        self.refresh()

    def link_existing(self):
        """
        Permet de lier un suspect existant à l’affaire courante.
        """
        suspects = self.gestion.get_suspects()
        if not suspects:
            return messagebox.showinfo("Info", "Aucun suspect existant.")

        # Fenêtre popup pour la sélection
        popup = tk.Toplevel(self)
        popup.title("Lier un suspect existant")
        popup.geometry("300x350")
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Sélectionnez un suspect :").pack(pady=5)

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True, padx=10)

        # Remplissage de la liste des suspects disponibles
        for s in suspects:
            listbox.insert(tk.END, f"{s.prenom} {s.nom}")

        def valider():
            """
            Valide la sélection et lie le suspect à l’affaire.
            """
            idx = listbox.curselection()
            if not idx:
                return messagebox.showwarning("Attention", "Aucun suspect sélectionné.")

            s = suspects[idx[0]]
            self.gestion.lier_suspect_affaire(self.affaire.id_affaire, s.id_suspect)

            popup.destroy()
            self.refresh()

        # Boutons de validation / annulation
        btns = tk.Frame(popup)
        btns.pack(pady=5)

        tk.Button(btns, text="Valider", command=valider).pack(side="left", padx=5)
        tk.Button(btns, text="Annuler", command=popup.destroy).pack(side="left", padx=5)

    def edit(self):
        """
        Modifie les informations du suspect sélectionné.
        """
        s = self._selected()
        if not s:
            return

        prenom = simpledialog.askstring("Modifier", "Prénom :", initialvalue=s.prenom)
        nom = simpledialog.askstring("Modifier", "Nom :", initialvalue=s.nom)

        if prenom and nom:
            # Mise à jour via la couche métier
            self.gestion.maj_suspect(
                s.id_suspect,
                {"prenom": prenom, "nom": nom}
            )
            self.refresh()

    def remove(self):
        """
        Retire le lien entre le suspect sélectionné et l’affaire.
        """
        s = self._selected()
        if not s:
            return

        if messagebox.askyesno(
                "Confirmation",
                f"Retirer {s.prenom} {s.nom} de cette affaire ?"
        ):
            self.gestion.del_suspect_affaire(self.affaire.id_affaire, s.id_suspect)
            self.refresh()
