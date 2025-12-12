import tkinter as tk
from tkinter import ttk
from gui.generic_details_window import GenericDetailsWindow


class DraggablePostit(ttk.Frame):
    def __init__(self, canvas, entity, entity_type, refresh_callback=None):
        super().__init__(canvas, padding=12, style=f"{entity_type}.TFrame")

        self.canvas = canvas
        self.entity = entity
        self.entity_type = entity_type
        self.refresh_callback = refresh_callback
        self.window_id = None

        # -----------------------------------------------------------
        # TITRE
        # -----------------------------------------------------------
        ttk.Label(self, text=f"{entity_type} #{entity.id}",
                  font=("Arial", 11, "bold")).pack()

        # -----------------------------------------------------------
        # CHAMPS PERTINENTS
        # -----------------------------------------------------------
        info_lines = self._extract_display_info(entity, entity_type)

        for line in info_lines:
            ttk.Label(self, text=line, font=("Arial", 9), justify="left").pack(anchor="w")

        # -----------------------------------------------------------
        # ÉVÉNEMENTS
        # -----------------------------------------------------------
        self.bind("<Button-1>", self.open_details)
        self.bind("<ButtonPress-3>", self.start_drag)
        self.bind("<B3-Motion>", self.do_drag)
        self.bind("<ButtonRelease-3>", self.end_drag)

        self.drag_start_x = 0
        self.drag_start_y = 0

    # -----------------------------------------------------------
    # EXTRACTION AUTOMATIQUE DES INFOS
    # -----------------------------------------------------------
    def _extract_display_info(self, entity, entity_type):
        """
        Retourne une liste de lignes courtes à afficher selon le type d'entité.
        """

        # ===================== AFFAIRE =====================
        if entity_type == "Affaire":
            return [
                f"Titre : {entity.titre[:25]}",
                f"Date : {entity.date}",
                f"Statut : {entity.statut}",
            ]

        # ===================== SUSPECT =====================
        if entity_type == "Suspect":
            lines = [
                f"Nom : {entity.nom}",
                f"Prénom : {entity.prenom}",
            ]
            if hasattr(entity, "age") and entity.age:
                lines.append(f"Âge : {entity.age}")
            return lines

        # ===================== PREUVE =====================
        if entity_type == "Preuve":
            return [
                f"Type : {entity.type}",
                f"Date : {entity.date}",
                f"Lieu : {entity.lieu}",
            ]

        # ===================== ARME =====================
        if entity_type == "Arme":
            return [
                f"Type : {entity.type}",
                f"Série : {entity.numero_serie}",
            ]

        # ===================== LIEU =====================
        if entity_type == "Lieu":
            return [
                f"Nom : {entity.nom}",
                f"Type : {entity.type}",
            ]

        # ===================== DEFAULT (automatique) =====================
        lines = []
        for attr in ("nom", "titre", "type", "description"):
            if hasattr(entity, attr):
                val = getattr(entity, attr)
                if val:
                    lines.append(f"{attr.capitalize()} : {str(val)[:25]}")
        return lines

    # -----------------------------------------------------------
    # OUVRIR FENÊTRE DÉTAILS
    # -----------------------------------------------------------
    def open_details(self, event):
        GenericDetailsWindow(
            parent=self.canvas,
            entity=self.entity,
            entity_type=self.entity_type,
            gestion=self.canvas.master.gestion,
            refresh_callback=self.refresh_callback
        )


    # -----------------------------------------------------------
    # DRAG & DROP
    # -----------------------------------------------------------
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        self.canvas.move(self.window_id, dx, dy)
        self.canvas.draw_links()

    def end_drag(self, event):
        x, y = self.canvas.coords(self.window_id)

        if hasattr(self.entity, "update_position"):
            self.entity.update_position(int(x), int(y))

        print(f"💾 Position {self.entity_type} #{self.entity.id} -> {x},{y}")
        self.canvas.draw_links()
