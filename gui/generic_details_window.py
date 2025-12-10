import tkinter as tk
from tkinter import ttk, messagebox


class GenericDetailsWindow(tk.Toplevel):
    """
    Fenêtre d’édition générique pour :
    - Affaire
    - Suspect
    - Preuve
    - Arme
    - Lieu

    Elle inspecte automatiquement l’objet (entity)
    et génère les champs dynamiquement.
    """

    def __init__(self, parent, entity, entity_type, refresh_callback=None):
        super().__init__(parent)

        self.entity = entity
        self.entity_type = entity_type
        self.refresh_callback = refresh_callback

        self.title(f"{entity_type} #{entity.id}")
        self.geometry("420x500")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"{entity_type} – édition", font=("Arial", 14, "bold")).pack(pady=10)

        # -------------------------
        # Champs dynamiques
        # -------------------------
        self.inputs = {}
        form = ttk.Frame(frame)
        form.pack(fill="x", pady=10)

        for i, (attr, value) in enumerate(self.inspect_entity(entity)):
            ttk.Label(form, text=attr + " :").grid(row=i, column=0, sticky="w")
            var = tk.StringVar(value=str(value) if value is not None else "")
            entry = ttk.Entry(form, textvariable=var)
            entry.grid(row=i, column=1, sticky="ew")
            self.inputs[attr] = var

        form.columnconfigure(1, weight=1)

        # -------------------------
        # Boutons
        # -------------------------
        ttk.Button(frame, text="Enregistrer", command=self.save).pack(pady=10)
        ttk.Button(frame, text="Fermer", command=self.destroy).pack()

    # --------------------------------------------------------------------
    def inspect_entity(self, entity):
        """
        Retourne les champs éditables automatiquement.
        On ignore les IDs et positions.
        """
        ignore = {"id", "id_affaire", "id_suspect", "id_preuve", "id_arme", "id_lieu",
                  "pos_x", "pos_y"}

        fields = []
        for attr, value in entity.__dict__.items():
            if attr in ignore:
                continue
            fields.append((attr, value))
        return fields

    # --------------------------------------------------------------------
    def save(self):
        """ Mets à jour l'objet automatiquement. """
        try:
            for attr, var in self.inputs.items():
                new_val = var.get()

                # Convertir en int lorsque approprié
                if new_val.isdigit():
                    new_val = int(new_val)

                setattr(self.entity, attr, new_val)

            # Sauvegarde si classe possède .update() ou .save()
            if hasattr(self.entity, "update"):
                self.entity.update(**self.entity.__dict__)
            elif hasattr(self.entity, "save"):
                self.entity.save()

            if self.refresh_callback:
                self.refresh_callback()

            messagebox.showinfo("Succès", "Modifications enregistrées.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder :\n{e}")
