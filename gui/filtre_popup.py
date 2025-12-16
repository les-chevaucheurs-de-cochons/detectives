import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter import simpledialog



class FiltrePopup(tk.Toplevel):
    def __init__(self, parent, gestion, canvas_view):
        super().__init__(parent)
        self.gestion = gestion
        self.canvas_view = canvas_view

        self.title("🔍 Filtrer les affaires")
        self.geometry("300x360")
        self.resizable(False, False)
        self.grab_set()

        tk.Button(self, text="🟡 Affaires en cours", command=self.filtre_en_cours) \
            .pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="⚪ Affaires classées", command=self.filtre_classees) \
            .pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="🔎 Recherche texte", command=self.filtre_texte) \
            .pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="👥 Par suspect", command=self.filtre_suspect) \
            .pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="🔪 Par arme", command=self.filtre_arme) \
            .pack(fill="x", pady=5, padx=10)
        tk.Button(self, text="📅 Entre deux dates", command=self.filtre_dates) \
            .pack(fill="x", pady=5, padx=10)

        tk.Label(self, text="").pack()
        tk.Button(self, text="♻️ Réinitialiser", command=self.reset) \
            .pack(fill="x", pady=5, padx=10)

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
        from tkinter import simpledialog
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

    # ========================
    # FILTRE PAR SÉLECTION
    # ========================

    def filtre_suspect(self):
        suspects = self.gestion.get_suspects()
        if not suspects:
            return messagebox.showinfo("Info", "Aucun suspect.")

        self._select_popup(
            title="Filtrer par suspect",
            label="Choisir un suspect :",
            items=suspects,
            display=lambda s: f"{s.nom} {s.prenom}",
            matcher=lambda a, s: s.id_suspect in {x.id_suspect for x in a.get_suspects()}
        )

    def filtre_dates(self):
        dmin = simpledialog.askstring(
            "Filtrer",
            "Date minimum (JJ-MM-AAAA)\nLaisser vide pour aucune :"
        )
        if dmin == "":
            dmin = None

        dmax = simpledialog.askstring(
            "Filtrer",
            "Date maximum (JJ-MM-AAAA)\nLaisser vide pour aucune :"
        )
        if dmax == "":
            dmax = None

        # Conversion sécurisée
        try:
            date_min = datetime.strptime(dmin, "%d-%m-%Y") if dmin else None
            date_max = datetime.strptime(dmax, "%d-%m-%Y") if dmax else None
        except ValueError:
            return messagebox.showerror(
                "Erreur",
                "Date invalide.\nFormat attendu : JJ-MM-AAAA"
            )

        # Appliquer le filtre
        resultats = []
        for a in self.gestion.get_affaires():
            try:
                date_affaire = datetime.strptime(a.date, "%d-%m-%Y")
            except ValueError:
                continue  # sécurité si donnée corrompue

            if date_min and date_affaire < date_min:
                continue
            if date_max and date_affaire > date_max:
                continue

            resultats.append(a)

        self.canvas_view.appliquer_filtre(resultats)
        self.destroy()


    def filtre_arme(self):
        armes = self.gestion.get_armes()
        if not armes:
            return messagebox.showinfo("Info", "Aucune arme.")

        self._select_popup(
            title="Filtrer par arme",
            label="Choisir une arme :",
            items=armes,
            display=lambda a: a.nom if hasattr(a, "nom") else f"Arme #{a.id_arme}",
            matcher=lambda aff, ar: ar.id_arme in {x.id_arme for x in aff.get_armes()}
        )

    # ========================
    # POPUP GÉNÉRIQUE
    # ========================

    def _select_popup(self, title, label, items, display, matcher):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry("300x120")
        popup.resizable(False, False)
        popup.grab_set()

        tk.Label(popup, text=label).pack(pady=5)

        var = tk.StringVar()
        combo = ttk.Combobox(
            popup,
            textvariable=var,
            values=[display(i) for i in items],
            state="readonly"
        )
        combo.pack(fill="x", padx=10)
        combo.current(0)

        def appliquer():
            idx = combo.current()
            selected = items[idx]

            resultats = [
                a for a in self.gestion.get_affaires()
                if matcher(a, selected)
            ]

            self.canvas_view.appliquer_filtre(resultats)
            popup.destroy()
            self.destroy()

        tk.Button(popup, text="Filtrer", command=appliquer) \
            .pack(pady=10)

    # ------------------------

    def reset(self):
        self.canvas_view.reset_filtre()
        self.destroy()
