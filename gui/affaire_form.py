import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from gui.suspects_panel import SuspectsPanel
from gui.armes_panel import ArmesPanel
from gui.lieux_panel import LieuxPanel


class AffaireForm(tk.Toplevel):
    def __init__(self, parent, gestion, affaire=None, on_close=None):
        super().__init__(parent)
        self.gestion = gestion
        self.affaire = affaire
        self.on_close = on_close

        self.title("🗂️ Affaire")
        self.geometry("420x650")
        self.resizable(False, False)

        # =======================
        # Variables
        # =======================
        self.var_titre = tk.StringVar(value=getattr(affaire, "titre", ""))
        self.var_date = tk.StringVar(value=getattr(affaire, "date", ""))
        self.var_statut = tk.StringVar(value=getattr(affaire, "statut", "en cours"))
        self.var_desc = tk.StringVar(value=getattr(affaire, "description", ""))

        self.var_cp = tk.StringVar(value=getattr(affaire, "code_postal", ""))
        self.var_ville = tk.StringVar(value=getattr(affaire, "lieu", ""))

        # =======================
        # FORMULAIRE
        # =======================
        form = tk.Frame(self)
        form.pack(fill="x", padx=10, pady=5)

        self._label_entry(form, "Titre *", self.var_titre)
        self._label_entry(form, "Date (JJ-MM-AAAA) *", self.var_date)

        tk.Label(form, text="Statut *").pack(anchor="w")
        ttk.Combobox(
            form,
            textvariable=self.var_statut,
            values=["en cours", "classée"],
            state="readonly"
        ).pack(fill="x", pady=3)

        # =======================
        # VILLE (COMBOBOX)
        # =======================
        tk.Label(form, text="Ville *").pack(anchor="w")

        self.villes = self.gestion.get_villes()  # [(cp, nom)]
        self.ville_map = {
            f"{cp} — {nom}": (cp, nom) for cp, nom in self.villes
        }

        self.combo_ville = ttk.Combobox(
            form,
            values=list(self.ville_map.keys()) + ["➕ Créer une nouvelle ville…"],
            state="readonly"
        )
        self.combo_ville.pack(fill="x", pady=3)
        self.combo_ville.bind("<<ComboboxSelected>>", self.on_ville_select)

        # Champs CP / Ville
        self.entry_cp = self._label_entry(form, "Code postal *", self.var_cp)
        self.entry_ville = self._label_entry(form, "Nom de la ville *", self.var_ville)

        # Par défaut : non éditables
        self._set_entries_state("readonly")

        tk.Label(form, text="Description").pack(anchor="w")
        tk.Entry(form, textvariable=self.var_desc).pack(fill="x", pady=3)

        # =======================
        # BOUTONS
        # =======================
        btns = tk.Frame(self)
        btns.pack(fill="x", pady=5)

        tk.Button(btns, text="💾 Enregistrer", command=self.save).pack(side="left", padx=5)

        if affaire:
            tk.Button(btns, text="🗑 Supprimer", command=self.delete).pack(side="right", padx=5)

        # =======================
        # ONGLETs
        # =======================
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_suspects = tk.Frame(self.notebook)
        self.tab_armes = tk.Frame(self.notebook)
        self.tab_lieux = tk.Frame(self.notebook)

        self.notebook.add(self.tab_suspects, text="👥 Suspects", state="disabled")
        self.notebook.add(self.tab_armes, text="🔪 Armes", state="disabled")
        self.notebook.add(self.tab_lieux, text="📍 Lieux", state="disabled")

        if self.affaire:
            self._activer_tabs()

    # ==================================================
    # UTILITAIRES
    # ==================================================

    def _label_entry(self, parent, label, var):
        tk.Label(parent, text=label).pack(anchor="w")
        entry = tk.Entry(parent, textvariable=var)
        entry.pack(fill="x", pady=3)
        return entry

    def _set_entries_state(self, state: str):
        self.entry_cp.config(state=state)
        self.entry_ville.config(state=state)

    def _date_valide(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    # ==================================================
    # VILLE — COMBOBOX
    # ==================================================

    def on_ville_select(self, event):
        choix = self.combo_ville.get()

        if choix == "➕ Créer une nouvelle ville…":
            self.var_cp.set("")
            self.var_ville.set("")
            self._set_entries_state("normal")
            return

        cp, nom = self.ville_map[choix]
        self.var_cp.set(cp)
        self.var_ville.set(nom)
        self._set_entries_state("readonly")

    # ==================================================
    # SAUVEGARDE
    # ==================================================

    def save(self):
        if not self.var_titre.get().strip():
            return messagebox.showerror("Erreur", "Titre obligatoire")

        date_str = self.var_date.get().strip()
        if not self._date_valide(date_str):
            return messagebox.showerror(
                "Erreur",
                "Date invalide.\nFormat attendu : JJ-MM-AAAA\nExemple : 25-12-2025"
            )

        cp = self.var_cp.get().strip()
        ville = self.var_ville.get().strip()

        if not cp or not ville:
            return messagebox.showerror("Erreur", "Ville obligatoire")

        # Création de la ville si nouvelle
        if not self.gestion.get_ville(cp):
            self.gestion.creer_ville(cp, ville)

        if self.affaire:
            self.gestion.maj_affaire(
                self.affaire.id_affaire,
                {
                    "titre": self.var_titre.get(),
                    "date": date_str,
                    "lieu": ville,
                    "code_postal": cp,
                    "statut": self.var_statut.get(),
                    "description": self.var_desc.get() or None
                }
            )
        else:
            self.affaire = self.gestion.creer_affaire(
                self.var_titre.get(),
                date_str,
                ville,
                cp,
                self.var_statut.get(),
                self.var_desc.get() or None
            )

            messagebox.showinfo(
                "Affaire créée",
                f"Affaire #{self.affaire.id_affaire} créée.\n"
                "Vous pouvez maintenant gérer suspects, armes et lieux."
            )

            self._activer_tabs()

        if self.on_close:
            self.on_close()

    # ==================================================
    # ONGLETs
    # ==================================================

    def _activer_tabs(self):
        for tab in (self.tab_suspects, self.tab_armes, self.tab_lieux):
            for w in tab.winfo_children():
                w.destroy()

        SuspectsPanel(self.tab_suspects, self.gestion, self.affaire).pack(fill="both", expand=True)
        ArmesPanel(self.tab_armes, self.gestion, self.affaire).pack(fill="both", expand=True)
        LieuxPanel(self.tab_lieux, self.gestion, self.affaire).pack(fill="both", expand=True)

        self.notebook.tab(self.tab_suspects, state="normal")
        self.notebook.tab(self.tab_armes, state="normal")
        self.notebook.tab(self.tab_lieux, state="normal")

    # ==================================================
    # SUPPRESSION
    # ==================================================

    def delete(self):
        if messagebox.askyesno("Confirmer", "Supprimer cette affaire ?"):
            self.gestion.supprimer_affaire(self.affaire.id_affaire)
            self.close()

    def close(self):
        if self.on_close:
            self.on_close()
        self.destroy()
