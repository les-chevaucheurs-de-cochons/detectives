import tkinter as tk
from tkinter import ttk
from gui.generic_details_window import GenericDetailsWindow


class DraggablePostit(ttk.Frame):
    def __init__(self, canvas, entity, entity_type, refresh_callback=None):
        """
        canvas : Canvas Tkinter
        entity : instance des classes backend
        entity_type : string ("Affaire", "Suspect", "Preuve", "Arme", "Lieu")
        """
        super().__init__(canvas, padding=20, style=f"{entity_type}.TFrame")

        self.canvas = canvas
        self.entity = entity
        self.entity_type = entity_type
        self.refresh_callback = refresh_callback
        self.window_id = None

        # -----------------------------------------------------------
        # Texte visible sur le post-it
        # -----------------------------------------------------------
        ttk.Label(self, text=f"{entity_type} #{entity.id}", font=("Arial", 10, "bold")).pack()

        # Dynamique : affiche les champs les plus pertinents
        for attr in ("titre", "nom", "type", "description"):
            if hasattr(entity, attr):
                val = getattr(entity, attr)
                if val:
                    ttk.Label(self, text=str(val)[:30]).pack()

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
    # DÉTAILS AUTOMATIQUES
    # -----------------------------------------------------------
    def open_details(self, event):
        GenericDetailsWindow(
            parent=self,
            entity=self.entity,
            entity_type=self.entity_type,
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
