import tkinter as tk
from tkinter import ttk, messagebox

from backend.affaire import Affaire
from backend.suspect import Suspect
from backend.preuves import Preuve
from backend.arme import Arme
from backend.lieu import Lieu

# Mapping entité ↔ classe backend
ENTITY_TYPES = {
    "Affaire": Affaire,
    "Suspect": Suspect,
    "Preuve": Preuve,
    "Arme": Arme,
    "Lieu": Lieu,
}


class GenericCreateWindow(tk.Toplevel):
    """
    Fenêtre générique de création d’entités :
    Affaire, Suspect, Preuve, Arme, Lieu
    """

    def __init__(self, parent, entity_type, gestion, refresh_callback=None):
        super().__init__(parent)

        self.entity_type = entity_type               # string
        self.entity_class = ENTITY_TYPES[entity_type]  # backend class
        self.gestion = gestion
        self.refresh_callback = refresh_callback

        self.title(f"Créer {entity_type}")
        self.geometry("420x500")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"Nouvelle {entity_type}", font=("Arial", 14, "bold")).pack(pady=10)

        # 🧩 On inspecte la classe pour générer automatiquement les champs
        self.inputs = {}
        form = ttk.Frame(frame)
        form.pack(fill="x")

        fake_instance = self._build_empty_instance()

        row = 0
        for attr, value in self._editable_fields(fake_instance):
            ttk.Label(form, text=attr + " :").grid(row=row, column=0, sticky="w")

            var = tk.StringVar()
            entry = ttk.Entry(form, textvariable=var)
            entry.grid(row=row, column=1, sticky="ew")

            self.inputs[attr] = var
            row += 1

        form.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Créer", command=self.submit).pack(pady=15)
        ttk.Button(frame, text="Annuler", command=self.destroy).pack()

    # ------------------------------------------------------------
    def _build_empty_instance(self):
        """Crée une instance vide pour introspection."""
        try:
            return self.entity_class(*([None] * len(self.entity_class.__dataclass_fields__)))
        except:
            return self.entity_class.__new__(self.entity_class)

    def _editable_fields(self, instance):
        ignore = {"id", "id_affaire", "id_suspect", "id_preuve", "id_arme",
                  "id_lieu", "pos_x", "pos_y"}

        fields = []
        for attr in instance.__dict__.keys():
            if attr not in ignore:
                fields.append((attr, None))
        return fields

    # ------------------------------------------------------------
    def submit(self):
        try:
            kwargs = {}

            for attr, var in self.inputs.items():
                value = var.get().strip()

                # conversion en int si possible
                if value.isdigit():
                    value = int(value)

                kwargs[attr] = value

            # ⚡ Unification backend : Appelle create()
            new_entity = self.entity_class.create(**kwargs)

            if self.refresh_callback:
                self.refresh_callback()

            messagebox.showinfo("Succès", f"{self.entity_type} créée !")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer {self.entity_type} :\n{e}")
