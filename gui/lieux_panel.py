import tkinter as tk
from tkinter import simpledialog, messagebox


class LieuxPanel(tk.Frame):
    def __init__(self, parent, gestion, affaire):
        super().__init__(parent)
        self.gestion = gestion
        self.affaire = affaire

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)

        btns = tk.Frame(self)
        btns.pack(fill="x")

        tk.Button(btns, text="➕ Nouveau", command=self.add_new).pack(side="left", padx=2)
        tk.Button(btns, text="🔗 Lier existant", command=self.link_existing).pack(side="left", padx=2)
        tk.Button(btns, text="✏️ Éditer", command=self.edit).pack(side="left", padx=2)
        tk.Button(btns, text="❌ Retirer", command=self.remove).pack(side="left", padx=2)

        self.refresh()

    # -----------------------------

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for l in self.affaire.get_lieux():
            label = l.nom
            if l.adresse:
                label += f" ({l.adresse})"
            self.listbox.insert(tk.END, label)

    def _selected(self):
        idx = self.listbox.curselection()
        if not idx:
            return None
        return self.affaire.get_lieux()[idx[0]]

    # -----------------------------

    def add_new(self):
        nom = simpledialog.askstring("Lieu", "Nom :")
        adresse = simpledialog.askstring("Lieu", "Adresse (optionnelle) :")
        if not nom:
            return

        l = self.gestion.creer_lieu(nom, adresse, type=None, id_affaire=self.affaire.id_affaire)
        self.gestion.lier_lieu_affaire(self.affaire.id_affaire, l.id_lieu)
        self.refresh()

    def link_existing(self):
        lieux = self.gestion.get_lieux()
        if not lieux:
            return messagebox.showinfo("Info", "Aucun lieu existant.")

        popup = tk.Toplevel(self)
        popup.title("Lier un lieu existant")
        popup.geometry("350x350")
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Sélectionnez un lieu :").pack(pady=5)

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True, padx=10)

        for l in lieux:
            label = l.nom
            if l.adresse:
                label += f" ({l.adresse})"
            listbox.insert(tk.END, label)

        def valider():
            idx = listbox.curselection()
            if not idx:
                return messagebox.showwarning("Attention", "Aucun lieu sélectionné.")

            lieu = lieux[idx[0]]
            self.gestion.lier_lieu_affaire(self.affaire.id_affaire, lieu.id_lieu)
            popup.destroy()
            self.refresh()

        btns = tk.Frame(popup)
        btns.pack(pady=5)

        tk.Button(btns, text="Valider", command=valider).pack(side="left", padx=5)
        tk.Button(btns, text="Annuler", command=popup.destroy).pack(side="left", padx=5)


    def edit(self):
        l = self._selected()
        if not l:
            return

        nom = simpledialog.askstring("Modifier", "Nom :", initialvalue=l.nom)
        adresse = simpledialog.askstring("Modifier", "Adresse :", initialvalue=l.adresse)

        self.gestion.maj_lieu(
            l.id_lieu,
            {"nom": nom, "adresse": adresse}
        )
        self.refresh()

    def remove(self):
        l = self._selected()
        if not l:
            return

        if messagebox.askyesno("Confirmation", f"Retirer le lieu « {l.nom} » ?"):
            self.gestion.del_lieu_affaire(self.affaire.id_affaire, l.id_lieu)
            self.refresh()
