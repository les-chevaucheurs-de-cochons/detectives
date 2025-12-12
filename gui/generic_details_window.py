import tkinter as tk
from tkinter import ttk, messagebox


class GenericDetailsWindow(tk.Toplevel):

    def __init__(self, parent, entity, entity_type, gestion, refresh_callback=None):
        super().__init__(parent)

        self.entity = entity
        self.entity_type = entity_type
        self.gestion = gestion        # <-- fonctionne maintenant
        self.refresh_callback = refresh_callback

        self.title(f"{entity_type} #{entity.id}")
        self.geometry("420x540")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"{entity_type} – édition",
                  font=("Arial", 14, "bold")).pack(pady=10)

        # ======================================================
        # FORMULAIRE AUTOMATIQUE
        # ======================================================
        self.inputs = {}
        form = ttk.Frame(frame)
        form.pack(fill="x", pady=10)

        for i, (attr, value) in enumerate(self.inspect_entity(entity)):
            ttk.Label(form, text=f"{attr} :").grid(row=i, column=0, sticky="w")
            var = tk.StringVar(value=str(value) if value is not None else "")
            entry = ttk.Entry(form, textvariable=var)
            entry.grid(row=i, column=1, sticky="ew")
            self.inputs[attr] = var

        form.columnconfigure(1, weight=1)

        # ======================================================
        # BOUTONS D'ACTION
        # ======================================================
        ttk.Button(frame, text="Enregistrer",
                   command=self.save).pack(pady=10)

        ttk.Button(frame, text="🗑 Supprimer",
                   command=self.delete_entity).pack(pady=5)

        ttk.Button(frame, text="Fermer",
                   command=self.destroy).pack(pady=10)

    # ----------------------------------------------------------
    def inspect_entity(self, entity):
        """ Retourne les champs éditables automatiquement. """
        ignore = {
            "id", "id_affaire", "id_suspect", "id_preuve",
            "id_arme", "id_lieu", "pos_x", "pos_y", "uid"
        }
        return [
            (attr, value)
            for attr, value in entity.__dict__.items()
            if attr not in ignore
        ]

    # ----------------------------------------------------------
    def save(self):
        """ Sauvegarde automatique des modifications """
        try:
            for attr, var in self.inputs.items():
                val = var.get()
                if val.isdigit():
                    val = int(val)
                setattr(self.entity, attr, val)

            if hasattr(self.entity, "update"):
                self.entity.update(**self.entity.__dict__)

            if self.refresh_callback:
                self.refresh_callback()

            messagebox.showinfo("OK", "Modifications enregistrées.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erreur", f"{e}")

    # ----------------------------------------------------------
    def delete_entity(self):
        """ Suppression dynamique via GestionEnquetes """
        if not messagebox.askyesno("Supprimer ?",
                                   f"Supprimer {self.entity_type} #{self.entity.id} ?"):
            return

        method = f"supprimer_{self.entity_type.lower()}"

        if hasattr(self.gestion, method):
            getattr(self.gestion, method)(self.entity.id)
        else:
            messagebox.showerror("Erreur",
                                 f"GestionEnquetes n’a pas la méthode {method}()")
            return

        if self.refresh_callback:
            self.refresh_callback()

        messagebox.showinfo("Supprimé",
                            f"{self.entity_type} #{self.entity.id} supprimé.")
        self.destroy()
