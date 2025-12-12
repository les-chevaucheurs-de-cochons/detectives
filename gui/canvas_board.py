# gui/canvas_board.py
import tkinter as tk
from tkinter import messagebox
from gui.postit_widget import DraggablePostit

RELATION_COLORS = {
    "suspect": "red",
    "arme": "orange",
    "preuve": "pink",
    "lieu": "yellow",
    "lié": "white",
    "default": "cyan",
}


class CanvasBoard(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e", highlightthickness=0)

        self.postits = []
        self.lines = []

        # ===========================
        # ZOOM & PAN VARIABLES
        # ===========================
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.bind("<ButtonPress-2>", self.start_pan)   # clic milieu
        self.bind("<B2-Motion>", self.do_pan)

        # Zoom molette
        self.bind("<MouseWheel>", self.zoom)
        self.bind("<Control-MouseWheel>", self.zoom)   # bonus ctrl+molette

    # ============================================================
    # CANVAS RESET
    # ============================================================
    def clear(self):
        for i in self.find_all():
            self.delete(i)
        self.postits.clear()
        self.lines.clear()

    # ============================================================
    # AFFICHAGE ENTITÉS
    # ============================================================
    def display_all(self):
        self.clear()

        from backend.affaire import Affaire
        from backend.suspect import Suspect
        from backend.preuves import Preuve
        from backend.arme import Arme
        from backend.lieu import Lieu

        ENTITIES = [
            (Affaire.all(), "Affaire"),
            (Suspect.all(), "Suspect"),
            (Preuve.all(), "Preuve"),
            (Arme.all(), "Arme"),
            (Lieu.all(), "Lieu"),
        ]

        for entity_list, t in ENTITIES:
            for obj in entity_list:
                self.create_postit(obj, t)

        self.draw_links()

    # ============================================================
    # CREATION POST-IT
    # ============================================================
    def create_postit(self, entity, entity_type):

        postit = DraggablePostit(
            canvas=self,
            entity=entity,
            entity_type=entity_type,
            refresh_callback=self.master.refresh_board,
        )

        postit.uid = entity.uid

        x = getattr(entity, "pos_x", 60)
        y = getattr(entity, "pos_y", 60)

        # position transformée avec zoom/pan
        x = (x * self.scale_factor) + self.offset_x
        y = (y * self.scale_factor) + self.offset_y

        postit.window_id = self.create_window(x, y, window=postit, anchor="nw")
        self.postits.append(postit)

    # ============================================================
    # DESSIN DES LIENS
    # ============================================================
    def draw_links(self):
        for line in self.lines:
            self.delete(line)
        self.lines.clear()

        relations = self.master.gestion.get_relations()

        for rel in relations:
            id_relation, type_rel, uid1, uid2, desc = rel

            p1 = next((p for p in self.postits if p.uid == uid1), None)
            p2 = next((p for p in self.postits if p.uid == uid2), None)

            if not p1 or not p2:
                continue

            x1, y1 = self.coords(p1.window_id)
            x2, y2 = self.coords(p2.window_id)

            x1 += p1.winfo_width() / 2
            y1 += p1.winfo_height() / 2
            x2 += p2.winfo_width() / 2
            y2 += p2.winfo_height() / 2

            color = RELATION_COLORS.get(type_rel, "cyan")

            line = self.create_line(
                x1, y1, x2, y2,
                fill=color, width=3,
                tags=("relation", f"rel_{id_relation}"),
            )

            self.lines.append(line)

            self.tag_bind(line, "<Button-1>",
                          lambda e, rel_id=id_relation: self.delete_relation(rel_id))

    # ============================================================
    # SUPPRESSION LIEN
    # ============================================================
    def delete_relation(self, rel_id):
        if messagebox.askyesno("Supprimer ?", "Supprimer ce lien ?"):
            self.master.gestion.supprimer_relation(rel_id)
            self.master.refresh_board()

    # ============================================================
    # PANNING (déplacement)
    # ============================================================
    def start_pan(self, event):
        self.scan_mark(event.x, event.y)

    def do_pan(self, event):
        self.scan_dragto(event.x, event.y, gain=1)
        self.draw_links()

    # ============================================================
    # ZOOM (molette)
    # ============================================================
    def zoom(self, event):
        zoom_factor = 1.1 if event.delta > 0 else 0.9

        self.scale_factor *= zoom_factor

        # zoom centré sur la souris
        self.scale("all", event.x, event.y, zoom_factor, zoom_factor)

        # recalcul offset
        self.offset_x = self.canvasx(0)
        self.offset_y = self.canvasy(0)

        self.draw_links()
