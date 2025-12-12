import tkinter as tk
from tkinter import ttk, messagebox

from backend.affaire import Affaire
from backend.suspect import Suspect
from backend.preuves import Preuve
from backend.arme import Arme
from backend.lieu import Lieu

ENTITY_TYPES = {
    "Affaire": Affaire,
    "Suspect": Suspect,
    "Preuve": Preuve,
    "Arme": Arme,
    "Lieu": Lieu,
}

# ------------------------------------------------------------
# FOREIGN KEYS REQUISES PAR ENTITÉ
# ------------------------------------------------------------
REQUIRED_FK = {
    "Preuve": ["id_affaire", "id_suspect"],
    "Arme": ["id_affaire"],
    "Lieu": ["id_affaire"],
    "Affaire": [],
    "Suspect": [],
}


class GenericCreateWindow(tk.Toplevel):

    def __init__(self, parent, entity_type, gestion, refresh_callback=None):
        super().__init__(parent)

        self.entity_type = entity_type
        self.entity_class = ENTITY_TYPES[entity_type]
        self.gestion = gestion
        self.refresh_callback = refresh_callback

        self.title(f"Créer {entity_type}")
        self.geometry("420x480")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"Nouvelle {entity_type}",
                  font=("Arial", 15, "bold")).pack(pady=10)

        self.inputs = {}
        form = ttk.Frame(frame)
        form.pack(fill="x")

        # ------------------------------------------------------------------
        # Récupération des champs autorisés (pas id_, pas pos_x/pos_y)
        # ------------------------------------------------------------------
        fields = self._get_editable_fields()

        # Ajout des FK requises
        fields.extend(REQUIRED_FK[self.entity_type])

        row = 0
        for attr in fields:

            ttk.Label(form, text=f"{attr} :").grid(row=row, column=0, sticky="w")

            # ----- Foreign key -> Combo -----
            if attr.startswith("id_"):
                related_class = ENTITY_TYPES[attr.replace("id_", "").capitalize()]
                objects = related_class.all()

                labels = [
                    f"{o.id} — {getattr(o, 'titre', getattr(o, 'nom', ''))}"
                    for o in objects
                ]

                combo = ttk.Combobox(form, values=labels, state="readonly")
                combo.grid(row=row, column=1, sticky="ew")
                self.inputs[attr] = combo

            # ----- Champ métier simple -----
            else:
                var = tk.StringVar()
                entry = ttk.Entry(form, textvariable=var)
                entry.grid(row=row, column=1, sticky="ew")
                self.inputs[attr] = var

            row += 1

        form.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Créer", command=self.submit).pack(pady=10)
        ttk.Button(frame, text="Annuler", command=self.destroy).pack()

    # ----------------------------------------------------------
    #  Liste des champs métier à afficher (sans id_, sans pos_x/y)
    # ----------------------------------------------------------
    def _get_editable_fields(self):
        instance = self._build_empty_instance()
        primary_key = self._primary_key_name()

        fields = []

        for attr in instance.__dict__.keys():

            # Skip primary key
            if attr == primary_key:
                continue

            # Skip technical fields
            if attr in ("pos_x", "pos_y"):
                continue

            # Skip foreign keys (elles seront ajoutées via REQUIRED_FK)
            if attr.startswith("id_"):
                continue

            fields.append(attr)

        return fields

    def _primary_key_name(self):
        for name in self.entity_class.__dataclass_fields__.keys():
            if name.startswith("id_"):
                return name
        return None

    def _build_empty_instance(self):
        try:
            return self.entity_class(
                *([None] * len(self.entity_class.__dataclass_fields__))
            )
        except:
            return self.entity_class.__new__(self.entity_class)

    # ----------------------------------------------------------
    def submit(self):
        try:
            kwargs = {}

            for attr, widget in self.inputs.items():

                # Foreign key / combobox
                if attr.startswith("id_") and isinstance(widget, ttk.Combobox):
                    sel = widget.get()
                    kwargs[attr] = int(sel.split(" — ")[0]) if sel else None
                    continue

                value = widget.get().strip()
                if value.isdigit():
                    value = int(value)

                kwargs[attr] = value

            # Création réelle
            self.entity_class.create(**kwargs)

            if self.refresh_callback:
                self.refresh_callback()

            messagebox.showinfo("Succès", f"{self.entity_type} créée !")
            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de créer {self.entity_type} :\n{e}"
            )
