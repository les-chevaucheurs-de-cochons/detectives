"""
Ce fichier a été développé dans le cadre d’un projet étudiant.
Certaines parties du code ont été générées ou assistées par une intelligence artificielle
(ChatGPT), puis relues, comprises et adaptées par l’étudiant.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox


class ArmesPanel(tk.Frame):
    """
    Panneau graphique permettant de gérer les armes liées à une affaire.
    Ce panneau est intégré dans l’interface graphique principale (GUI).
    """

    def __init__(self, parent, gestion, affaire):
        """
        Constructeur du panneau des armes.

        parent  : widget parent (Notebook / Frame)
        gestion : instance de GestionEnquetes (logique métier)
        affaire : affaire actuellement sélectionnée
        """
        super().__init__(parent)

        # Références vers la logique métier et l'affaire courante
        self.gestion = gestion
        self.affaire = affaire

        # Listbox affichant les armes liées à l'affaire
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame contenant les boutons d’action
        btns = tk.Frame(self)
        btns.pack(fill="x")

        # Bouton pour créer une nouvelle arme
        tk.Button(btns, text="➕ Nouvelle", command=self.add_new).pack(side="left", padx=2)

        # Bouton pour lier une arme existante
        tk.Button(btns, text="🔗 Lier existante", command=self.link_existing).pack(side="left", padx=2)

        # Bouton pour modifier une arme existante
        tk.Button(btns, text="✏️ Éditer", command=self.edit).pack(side="left", padx=2)

        # Bouton pour retirer le lien entre une arme et l’affaire
        tk.Button(btns, text="❌ Retirer", command=self.remove).pack(side="left", padx=2)

        # Chargement initial de la liste
        self.refresh()

    # -----------------------------
    # MÉTHODES UTILITAIRES
    # -----------------------------

    def refresh(self):
        """
        Met à jour la liste des armes affichées.
        Les armes sont récupérées depuis l’objet affaire.
        """
        self.listbox.delete(0, tk.END)

        for a in self.affaire.get_armes():
            # Construction du label affiché
            label = a.type
            if a.numero_serie:
                label += f" (n° {a.numero_serie})"

            self.listbox.insert(tk.END, label)

    def _selected(self):
        """
        Retourne l’arme actuellement sélectionnée dans la liste.
        Si aucune arme n’est sélectionnée, retourne None.
        """
        idx = self.listbox.curselection()
        if not idx:
            return None

        return self.affaire.get_armes()[idx[0]]

    # -----------------------------
    # ACTIONS UTILISATEUR
    # -----------------------------

    def add_new(self):
        """
        Crée une nouvelle arme et la lie immédiatement à l’affaire.
        """
        type_arme = simpledialog.askstring("Arme", "Type :")
        numero = simpledialog.askstring("Arme", "Numéro de série (optionnel) :")
        description = simpledialog.askstring("Arme", "Description (optionnelle) :")

        # Si aucun type n’est fourni, on annule l’opération
        if not type_arme:
            return

        # Création de l’arme via la couche métier
        a = self.gestion.creer_arme(
            type_arme,
            description,
            numero,
            self.affaire.id_affaire
        )

        # Liaison de l’arme avec l’affaire
        self.gestion.lier_arme_affaire(self.affaire.id_affaire, a.id_arme)

        # Rafraîchissement de l’affichage
        self.refresh()

    def link_existing(self):
        """
        Permet de lier une arme existante à l’affaire courante.
        """
        armes = self.gestion.get_armes()
        if not armes:
            return messagebox.showinfo("Info", "Aucune arme existante.")

        # Fenêtre popup pour la sélection
        popup = tk.Toplevel(self)
        popup.title("Lier une arme existante")
        popup.geometry("350x350")
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Sélectionnez une arme :").pack(pady=5)

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True, padx=10)

        # Remplissage de la liste des armes disponibles
        for a in armes:
            label = a.type
            if a.numero_serie:
                label += f" (n° {a.numero_serie})"
            listbox.insert(tk.END, label)

        def valider():
            """
            Valide la sélection et lie l’arme à l’affaire.
            """
            idx = listbox.curselection()
            if not idx:
                return messagebox.showwarning("Attention", "Aucune arme sélectionnée.")

            arme = armes[idx[0]]
            self.gestion.lier_arme_affaire(self.affaire.id_affaire, arme.id_arme)

            popup.destroy()
            self.refresh()

        # Boutons de validation / annulation
        btns = tk.Frame(popup)
        btns.pack(pady=5)

        tk.Button(btns, text="Valider", command=valider).pack(side="left", padx=5)
        tk.Button(btns, text="Annuler", command=popup.destroy).pack(side="left", padx=5)

    def edit(self):
        """
        Modifie les informations de l’arme sélectionnée.
        """
        a = self._selected()
        if not a:
            return

        type_arme = simpledialog.askstring("Modifier", "Type :", initialvalue=a.type)
        numero = simpledialog.askstring("Modifier", "Numéro :", initialvalue=a.numero_serie)
        description = simpledialog.askstring("Modifier", "Description :", initialvalue=a.description)

        # Mise à jour via la couche métier
        self.gestion.maj_arme(
            a.id_arme,
            {
                "type": type_arme,
                "numero_serie": numero,
                "description": description
            }
        )

        self.refresh()

    def remove(self):
        """
        Retire le lien entre l’arme sélectionnée et l’affaire.
        """
        a = self._selected()
        if not a:
            return

        if messagebox.askyesno("Confirmation", f"Retirer l’arme « {a.type} » ?"):
            self.gestion.del_arme_affaire(self.affaire.id_affaire, a.id_arme)
            self.refresh()
