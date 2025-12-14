import tkinter as tk
from tkinter import simpledialog, messagebox


class ArmesPanel(tk.Frame):
    def __init__(self, parent, gestion, affaire):
        super().__init__(parent)
        self.gestion = gestion
        self.affaire = affaire

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)

        btns = tk.Frame(self)
        btns.pack(fill="x")

        tk.Button(btns, text="➕ Nouvelle", command=self.add_new).pack(side="left", padx=2)
        tk.Button(btns, text="🔗 Lier existante", command=self.link_existing).pack(side="left", padx=2)
        tk.Button(btns, text="✏️ Éditer", command=self.edit).pack(side="left", padx=2)
        tk.Button(btns, text="❌ Retirer", command=self.remove).pack(side="left", padx=2)

        self.refresh()

    # -----------------------------

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for a in self.affaire.get_armes():
            label = a.type
            if a.numero_serie:
                label += f" (n° {a.numero_serie})"
            self.listbox.insert(tk.END, label)

    def _selected(self):
        idx = self.listbox.curselection()
        if not idx:
            return None
        return self.affaire.get_armes()[idx[0]]

    # -----------------------------

    def add_new(self):
        type_arme = simpledialog.askstring("Arme", "Type :")
        numero = simpledialog.askstring("Arme", "Numéro de série (optionnel) :")
        description = simpledialog.askstring("Arme", "Description (optionnelle) :")

        if not type_arme:
            return

        a = self.gestion.creer_arme(type_arme, description, numero, self.affaire.id_affaire)
        self.gestion.lier_arme_affaire(self.affaire.id_affaire, a.id_arme)
        self.refresh()

    def link_existing(self):
        armes = self.gestion.get_armes()
        if not armes:
            return messagebox.showinfo("Info", "Aucune arme existante.")

        popup = tk.Toplevel(self)
        popup.title("Lier une arme existante")
        popup.geometry("350x350")
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text="Sélectionnez une arme :").pack(pady=5)

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True, padx=10)

        for a in armes:
            label = a.type
            if a.numero_serie:
                label += f" (n° {a.numero_serie})"
            listbox.insert(tk.END, label)

        def valider():
            idx = listbox.curselection()
            if not idx:
                return messagebox.showwarning("Attention", "Aucune arme sélectionnée.")

            arme = armes[idx[0]]
            self.gestion.lier_arme_affaire(self.affaire.id_affaire, arme.id_arme)
            popup.destroy()
            self.refresh()

        btns = tk.Frame(popup)
        btns.pack(pady=5)

        tk.Button(btns, text="Valider", command=valider).pack(side="left", padx=5)
        tk.Button(btns, text="Annuler", command=popup.destroy).pack(side="left", padx=5)


    def edit(self):
        a = self._selected()
        if not a:
            return

        type_arme = simpledialog.askstring("Modifier", "Type :", initialvalue=a.type)
        numero = simpledialog.askstring("Modifier", "Numéro :", initialvalue=a.numero_serie)
        description = simpledialog.askstring("Modifier", "Description :", initialvalue=a.description)

        self.gestion.maj_arme(
            a.id_arme,
            {"type": type_arme, "numero_serie": numero, "description": description}
        )
        self.refresh()

    def remove(self):
        a = self._selected()
        if not a:
            return

        if messagebox.askyesno("Confirmation", f"Retirer l’arme « {a.type} » ?"):
            self.gestion.del_arme_affaire(self.affaire.id_affaire, a.id_arme)
            self.refresh()
