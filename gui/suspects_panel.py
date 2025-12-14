import tkinter as tk
from tkinter import simpledialog, messagebox


class SuspectsPanel(tk.Frame):
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
        for s in self.affaire.get_suspects():
            self.listbox.insert(tk.END, f"{s.prenom} {s.nom}")

    def _selected(self):
        idx = self.listbox.curselection()
        if not idx:
            return None
        return self.affaire.get_suspects()[idx[0]]

    # -----------------------------
    # ACTIONS
    # -----------------------------

    def add_new(self):
        prenom = simpledialog.askstring("Suspect", "Prénom :")
        nom = simpledialog.askstring("Suspect", "Nom :")
        if not prenom or not nom:
            return

        s = self.gestion.creer_suspect(nom, prenom)
        self.gestion.lier_suspect_affaire(self.affaire.id_affaire, s.id_suspect)
        self.refresh()

    def link_existing(self):
        suspects = self.gestion.get_suspects()
        if not suspects:
            return messagebox.showinfo("Info", "Aucun suspect existant.")

        popup = tk.Toplevel(self)
        popup.title("Lier un suspect existant")
        popup.geometry("300x350")
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Sélectionnez un suspect :").pack(pady=5)

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True, padx=10)

        for s in suspects:
            listbox.insert(tk.END, f"{s.prenom} {s.nom}")

        def valider():
            idx = listbox.curselection()
            if not idx:
                return messagebox.showwarning("Attention", "Aucun suspect sélectionné.")

            s = suspects[idx[0]]
            self.gestion.lier_suspect_affaire(self.affaire.id_affaire, s.id_suspect)
            popup.destroy()
            self.refresh()

        btns = tk.Frame(popup)
        btns.pack(pady=5)

        tk.Button(btns, text="Valider", command=valider).pack(side="left", padx=5)
        tk.Button(btns, text="Annuler", command=popup.destroy).pack(side="left", padx=5)


    def edit(self):
        s = self._selected()
        if not s:
            return

        prenom = simpledialog.askstring("Modifier", "Prénom :", initialvalue=s.prenom)
        nom = simpledialog.askstring("Modifier", "Nom :", initialvalue=s.nom)

        if prenom and nom:
            self.gestion.maj_suspect(
                s.id_suspect,
                {"prenom": prenom, "nom": nom}
            )
            self.refresh()

    def remove(self):
        s = self._selected()
        if not s:
            return

        if messagebox.askyesno(
                "Confirmation",
                f"Retirer {s.prenom} {s.nom} de cette affaire ?"
        ):
            self.gestion.del_suspect_affaire(self.affaire.id_affaire, s.id_suspect)
            self.refresh()
