import tkinter as tk
from gui.affaire_form import AffaireForm
from gui.styles import POSTIT_WIDTH, POSTIT_HEIGHT, COLOR_EN_COURS, COLOR_CLASSEE


class AffaireWidget:
    def __init__(self, canvas, affaire, gestion, parent):
        self.canvas = canvas
        self.affaire = affaire
        self.gestion = gestion
        self.parent = parent

        self.start_x = 0
        self.start_y = 0

        color = COLOR_EN_COURS if affaire.statut == "en cours" else COLOR_CLASSEE

        x = affaire.pos_x
        y = affaire.pos_y

        self.rect = canvas.create_rectangle(
            x, y,
            x + POSTIT_WIDTH,
            y + POSTIT_HEIGHT,
            fill=color,
            outline="black",
            tags=("postit",)
        )

        self.text = canvas.create_text(
            x + 10,
            y + 10,
            anchor="nw",
            width=POSTIT_WIDTH - 20,
            font=("Segoe UI", 10),
            text=self._build_text(),
            tags=("postit",)
        )



        # =====================
        # EVENTS
        # =====================
        for item in (self.rect, self.text):
            canvas.tag_bind(item, "<ButtonPress-1>", self.on_press)
            canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
            canvas.tag_bind(item, "<ButtonRelease-1>", self.on_release)
            canvas.tag_bind(item, "<Double-Button-1>", self.on_double_click)

    # ------------------------------------------------

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.text, dx, dy)

        self.start_x = event.x
        self.start_y = event.y

        # Redessiner les liens en temps réel
        self.parent.redraw_links()

    def on_release(self, event):
        # Nouvelle position = coin supérieur gauche du rectangle
        x1, y1, _, _ = self.canvas.coords(self.rect)

        # Sauvegarde en base
        self.affaire.update_position(int(x1), int(y1))

    def on_double_click(self, event):
        AffaireForm(
            self.canvas,
            self.gestion,
            self.affaire,
            on_close=self.parent.refresh
        )

    # ------------------------------------------------

    def center(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        return (x1 + x2) // 2, (y1 + y2) // 2

    def _build_text(self):
        nb_suspects = len(self.affaire.get_suspects())
        nb_armes = len(self.affaire.get_armes())
        nb_lieux = len(self.affaire.get_lieux())

        statut = self.affaire.statut.upper()
        date = self.affaire.date
        ville = self.affaire.lieu
        cp = self.affaire.code_postal or "—"

        return (
            f"🗂️ {self.affaire.titre}\n"
            f"📅 {date}\n"
            f"📍 {ville} ({cp})\n"
            f"\n"
            f"👥 {nb_suspects} suspect(s)\n"
            f"🔪 {nb_armes} arme(s)\n"
            f"📍 {nb_lieux} lieu(x)\n"
            f"\n"
            f"⬤ {statut}"
        )

