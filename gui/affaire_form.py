import tkinter as tk
from tkinter import ttk, messagebox
import re

from gui.suspects_panel import SuspectsPanel
from gui.armes_panel import ArmesPanel
from gui.lieux_panel import LieuxPanel


DATE_REGEX = r"^\d{2}-\d{2}-\d{4}$"


class AffaireForm(tk.Toplevel):
    def __init__(self, parent, gestion, affaire=None, on_close=None):
        super().__init__(parent)
        self.gestion = gestion
        self.affaire = affaire
        self.on_close = on_close

        self.title("🗂️ Affaire")
        self.geometry("420x620")
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

        self._label_entry(form, "Code postal *", self.var_cp)
        self._label_entry(form, "Ville *", self.var_ville)

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
        # ONGLETs (toujours visibles)
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

    # ------------------------------------------------

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

    # ------------------------------------------------

    def _label_entry(self, parent, label, var):
        tk.Label(parent, text=label).pack(anchor="w")
        tk.Entry(parent, textvariable=var).pack(fill="x", pady=3)

    # ------------------------------------------------

    def save(self):
        if not self.var_titre.get().strip():
            return messagebox.showerror("Erreur", "Titre obligatoire")

        if not re.match(DATE_REGEX, self.var_date.get()):
            return messagebox.showerror("Erreur", "Date invalide (JJ-MM-AAAA)")

        if not self.var_cp.get().strip() or not self.var_ville.get().strip():
            return messagebox.showerror("Erreur", "Ville obligatoire")

        # Ville
        if not self.gestion.get_ville(self.var_cp.get()):
            self.gestion.creer_ville(self.var_cp.get(), self.var_ville.get())

        if self.affaire:
            # MODIFICATION
            self.gestion.maj_affaire(self.affaire.id_affaire, {
                "titre": self.var_titre.get(),
                "date": self.var_date.get(),
                "lieu": self.var_ville.get(),
                "code_postal": self.var_cp.get(),
                "statut": self.var_statut.get(),
                "description": self.var_desc.get() or None
            })
        else:
            # CRÉATION
            self.affaire = self.gestion.creer_affaire(
                self.var_titre.get(),
                self.var_date.get(),
                self.var_ville.get(),
                self.var_cp.get(),
                self.var_statut.get(),
                self.var_desc.get() or None
            )

            messagebox.showinfo(
                "Affaire créée",
                f"Affaire #{self.affaire.id_affaire} créée.\nVous pouvez maintenant gérer suspects, armes et lieux."
            )

            self._activer_tabs()

        if self.on_close:
            self.on_close()

    # ------------------------------------------------

    def delete(self):
        if messagebox.askyesno("Confirmer", "Supprimer cette affaire ?"):
            self.gestion.supprimer_affaire(self.affaire.id_affaire)
            self.close()

    # ------------------------------------------------

    def close(self):
        if self.on_close:
            self.on_close()
        self.destroy()
