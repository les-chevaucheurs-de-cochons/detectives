# gui/link_window.py
import tkinter as tk
from tkinter import ttk, messagebox


class LinkWindow(tk.Toplevel):
    def __init__(self, parent, gestion, refresh_callback=None):
        super().__init__(parent)

        self.gestion = gestion
        self.refresh_callback = refresh_callback

        self.title("Créer un lien entre deux entités")
        self.geometry("450x360")
        self.resizable(False, False)

        # --------------------------
        # CHARGER TOUTES LES ENTITÉS
        # --------------------------
        from backend.affaire import Affaire
        from backend.suspect import Suspect
        from backend.preuves import Preuve
        from backend.arme import Arme
        from backend.lieu import Lieu

        self.entities = []

        for a in Affaire.all(): self.entities.append((a, "Affaire"))
        for s in Suspect.all(): self.entities.append((s, "Suspect"))
        for p in Preuve.all(): self.entities.append((p, "Preuve"))
        for ar in Arme.all(): self.entities.append((ar, "Arme"))
        for l in Lieu.all(): self.entities.append((l, "Lieu"))

        # --------------------------
        # UI
        # --------------------------
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Créer un lien entre deux entités",
                  font=("Arial", 14, "bold")).pack(pady=10)

        form = ttk.Frame(frame)
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Entité 1 :").grid(row=0, column=0, sticky="w")
        self.combo_1 = ttk.Combobox(form, values=self._labels(), state="readonly")
        self.combo_1.grid(row=0, column=1, sticky="ew")

        ttk.Label(form, text="Entité 2 :").grid(row=1, column=0, sticky="w")
        self.combo_2 = ttk.Combobox(form, values=self._labels(), state="readonly")
        self.combo_2.grid(row=1, column=1, sticky="ew")

        ttk.Label(form, text="Type de lien :").grid(row=2, column=0, sticky="w")
        self.combo_type = ttk.Combobox(
            form,
            values=["lié", "suspect", "arme", "preuve", "lieu"],
            state="readonly"
        )
        self.combo_type.grid(row=2, column=1, sticky="ew")

        form.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Créer le lien", command=self.submit).pack(pady=15)

    def _labels(self):
        labels = []
        for obj, t in self.entities:
            txt = getattr(obj, "titre", getattr(obj, "nom", ""))
            labels.append(f"{t} {obj.uid} — {txt}")
        return labels

    def submit(self):
        sel1 = self.combo_1.current()
        sel2 = self.combo_2.current()
        type_lien = self.combo_type.get().strip()

        if sel1 < 0 or sel2 < 0:
            return messagebox.showerror("Erreur", "Choisissez deux entités.")
        if sel1 == sel2:
            return messagebox.showerror("Erreur", "Impossible de lier un élément avec lui-même.")
        if not type_lien:
            return messagebox.showerror("Erreur", "Choisissez un type de lien.")

        entity1, type1 = self.entities[sel1]
        entity2, type2 = self.entities[sel2]

        # ID UNIQUE : A1, S3, P6, R10, L4
        uid1 = entity1.uid
        uid2 = entity2.uid

        try:
            self.gestion.creer_relation(type_lien, uid1, uid2,
                                        description=f"Lien '{type_lien}' : {uid1} ↔ {uid2}")

            if self.refresh_callback:
                self.refresh_callback()

            messagebox.showinfo("Succès", "Lien créé.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))
