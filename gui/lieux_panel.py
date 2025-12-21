"""
Ce fichier a été développé dans le cadre d’un projet étudiant.
Certaines parties du code ont été générées ou assistées par une intelligence artificielle
(ChatGPT), puis relues, comprises et adaptées par l’étudiant.

"""

import tkinter as tk
from tkinter import simpledialog, messagebox


class LieuxPanel(tk.Frame):
    """
    Panneau graphique permettant de gérer les lieux liés à une affaire.
    Ce panneau est intégré dans l’interface graphique principale (GUI).
    """

    def __init__(self, parent, gestion, affaire):
        """
        Constructeur du panneau des lieux.

        parent  : widget parent (Notebook / Frame)
        gestion : instance de GestionEnquetes (logique métier)
        affaire : affaire actuellement sélectionnée
        """
        super().__init__(parent)

        # Références vers la logique métier et l'affaire courante
        self.gestion = gestion
        self.affaire = affaire

        # Listbox affichant les lieux liés à l'affaire
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame contenant les boutons d’action
        btns = tk.Frame(self)
        btns.pack(fill="x")

        # Bouton pour créer un nouveau lieu
        tk.Button(btns, text="➕ Nouveau", command=self.add_new).pack(side="left", padx=2)

        # Bouton pour lier un lieu déjà existant
        tk.Button(btns, text="🔗 Lier existant", command=self.link_existing).pack(side="left", padx=2)

        # Bouton pour modifier un lieu existant
        tk.Button(btns, text="✏️ Éditer", command=self.edit).pack(side="left", padx=2)

        # Bouton pour retirer le lien entre un lieu et l’affaire
        tk.Button(btns, text="❌ Retirer", command=self.remove).pack(side="left", padx=2)

        # Chargement initial de la liste
        self.refresh()

    # -----------------------------
    # MÉTHODES UTILITAIRES
    # -----------------------------

    def refresh(self):
        """
        Met à jour la liste des lieux affichés.
        Les lieux sont récupérés depuis l’objet affaire.
        """
        self.listbox.delete(0, tk.END)

        for l in self.affaire.get_lieux():
            # Construction du label affiché
            label = l.nom
            if l.adresse:
                label += f" ({l.adresse})"

            self.listbox.insert(tk.END, label)

    def _selected(self):
        """
        Retourne le lieu actuellement sélectionné dans la liste.
        Si aucun élément n’est sélectionné, retourne None.
        """
        idx = self.listbox.curselection()
        if not idx:
            return None

        return self.affaire.get_lieux()[idx[0]]

    # -----------------------------
    # ACTIONS UTILISATEUR
    # -----------------------------

    def add_new(self):
        """
        Crée un nouveau lieu et le lie immédiatement à l’affaire.
        """
        nom = simpledialog.askstring("Lieu", "Nom :")
        adresse = simpledialog.askstring("Lieu", "Adresse (optionnelle) :")

        # Si aucun nom n’est fourni, on annule l’opération
        if not nom:
            return

        # Création du lieu via la couche métier
        l = self.gestion.creer_lieu(
            nom,
            adresse,
            type=None,
            id_affaire=self.affaire.id_affaire
        )

        # Liaison du lieu avec l’affaire
        self.gestion.lier_lieu_affaire(self.affaire.id_affaire, l.id_lieu)

        # Rafraîchissement de l’affichage
        self.refresh()

    def link_existing(self):
        """
        Permet de lier un lieu existant à l’affaire courante.
        """
        lieux = self.gestion.get_lieux()
        if not lieux:
            return messagebox.showinfo("Info", "Aucun lieu existant.")

        # Fenêtre popup pour la sélection
        popup = tk.Toplevel(self)
        popup.title("Lier un lieu existant")
        popup.geometry("350x350")
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Sélectionnez un lieu :").pack(pady=5)

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True, padx=10)

        # Remplissage de la liste des lieux disponibles
        for l in lieux:
            label = l.nom
            if l.adresse:
                label += f" ({l.adresse})"
            listbox.insert(tk.END, label)

        def valider():
            """
            Valide la sélection et lie le lieu à l’affaire.
            """
            idx = listbox.curselection()
            if not idx:
                return messagebox.showwarning("Attention", "Aucun lieu sélectionné.")

            lieu = lieux[idx[0]]
            self.gestion.lier_lieu_affaire(self.affaire.id_affaire, lieu.id_lieu)

            popup.destroy()
            self.refresh()

        # Boutons de validation / annulation
        btns = tk.Frame(popup)
        btns.pack(pady=5)

        tk.Button(btns, text="Valider", command=valider).pack(side="left", padx=5)
        tk.Button(btns, text="Annuler", command=popup.destroy).pack(side="left", padx=5)

    def edit(self):
        """
        Modifie les informations du lieu sélectionné.
        """
        l = self._selected()
        if not l:
            return

        nom = simpledialog.askstring("Modifier", "Nom :", initialvalue=l.nom)
        adresse = simpledialog.askstring("Modifier", "Adresse :", initialvalue=l.adresse)

        # Mise à jour via la couche métier
        self.gestion.maj_lieu(
            l.id_lieu,
            {"nom": nom, "adresse": adresse}
        )

        self.refresh()

    def remove(self):
        """
        Retire le lien entre le lieu sélectionné et l’affaire.
        """
        l = self._selected()
        if not l:
            return

        if messagebox.askyesno("Confirmation", f"Retirer le lieu « {l.nom} » ?"):
            self.gestion.del_lieu_affaire(self.affaire.id_affaire, l.id_lieu)
            self.refresh()
