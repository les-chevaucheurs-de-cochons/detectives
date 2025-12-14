import tkinter as tk
from tkinter import simpledialog, messagebox


class FiltrePopup(tk.Toplevel):
    def __init__(self, parent, gestion, canvas_view):
        super().__init__(parent)
        self.gestion = gestion
        self.canvas_view = canvas_view

        self.title("🔍 Filtrer les affaires")
        self.geometry("300x350")
        self.resizable(False, False)
        self.grab_set()

        tk.Button(self, text="🟡 Affaires en cours", command=self.filtre_en_cours).pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="⚪ Affaires classées", command=self.filtre_classees).pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="🔎 Recherche texte", command=self.filtre_texte).pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="👥 Par suspect", command=self.filtre_suspect).pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="🔪 Par arme", command=self.filtre_arme).pack(fill="x", pady=5, padx=10)

        tk.Label(self, text="").pack()
        tk.Button(self, text="♻️ Réinitialiser", command=self.reset).pack(fill="x", pady=5, padx=10)

    # ------------------------

    def filtre_en_cours(self):
        affaires = [a for a in self.gestion.get_affaires() if a.statut == "en cours"]
        self.canvas_view.appliquer_filtre(affaires)
        self.destroy()

    def filtre_classees(self):
        affaires = [a for a in self.gestion.get_affaires() if a.statut == "classée"]
        self.canvas_view.appliquer_filtre(affaires)
        self.destroy()

    def filtre_texte(self):
        texte = simpledialog.askstring("Recherche", "Mot à chercher :")
        if not texte:
            return

        texte = texte.lower()
        resultats = []

        for a in self.gestion.get_affaires():
            champs = [a.titre.lower(), (a.lieu or "").lower()]
            if any(texte in c for c in champs):
                resultats.append(a)

        self.canvas_view.appliquer_filtre(resultats)
        self.destroy()

    def filtre_suspect(self):
        suspects = self.gestion.get_suspects()
        if not suspects:
            return messagebox.showinfo("Info", "Aucun suspect.")

        popup = simpledialog.askinteger("Suspect", "ID du suspect :")
        if popup is None:
            return

        resultats = []
        for a in self.gestion.get_affaires():
            if popup in {s.id_suspect for s in a.get_suspects()}:
                resultats.append(a)

        self.canvas_view.appliquer_filtre(resultats)
        self.destroy()

    def filtre_arme(self):
        armes = self.gestion.get_armes()
        if not armes:
            return messagebox.showinfo("Info", "Aucune arme.")

        popup = simpledialog.askinteger("Arme", "ID de l’arme :")
        if popup is None:
            return

        resultats = []
        for a in self.gestion.get_affaires():
            if popup in {ar.id_arme for ar in a.get_armes()}:
                resultats.append(a)

        self.canvas_view.appliquer_filtre(resultats)
        self.destroy()

    def reset(self):
        self.canvas_view.reset_filtre()
        self.destroy()
