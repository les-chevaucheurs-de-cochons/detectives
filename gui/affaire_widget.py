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
        self.form_window = None

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

        # 2) Créer le texte
        self.text = canvas.create_text(
            x + 10,
            y + 10,
            anchor="nw",
            width=POSTIT_WIDTH - 20,
            font=("Segoe UI", 10),
            text=self._build_text(),
            tags=("postit",)
        )


        bbox = canvas.bbox(self.text)
        if bbox:
            tx1, ty1, tx2, ty2 = bbox
            text_width = tx2 - tx1
            text_height = ty2 - ty1


            new_width = max(POSTIT_WIDTH, text_width + 20)
            new_height = max(POSTIT_HEIGHT, text_height + 20)

            canvas.coords(
                self.rect,
                x, y,
                x + new_width,
                y + new_height
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


        self.parent.redraw_links()

    def on_release(self, event):

        x1, y1, _, _ = self.canvas.coords(self.rect)

        # Sauvegarde en base
        self.affaire.update_position(int(x1), int(y1))

    def on_double_click(self, event):

        if self.form_window is not None and self.form_window.winfo_exists():
            self.form_window.lift()
            self.form_window.focus_set()
            return

        self.form_window = AffaireForm(
            self.canvas,
            self.gestion,
            self.affaire,
            on_close=self._on_form_close
        )

    def _on_form_close(self):

        self.form_window = None
        self.parent.refresh()


    # ------------------------------------------------

    def center(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        return (x1 + x2) // 2, (y1 + y2) // 2

    def _build_text(self):

        suspects = self.affaire.get_suspects()
        armes = self.affaire.get_armes()
        lieux = self.affaire.get_lieux()

        statut = self.affaire.statut.upper()
        date = self.affaire.date
        ville = self.affaire.lieu
        cp = self.affaire.code_postal or "—"

        # Détail suspects
        if suspects:
            suspects_lines = [f"   - {s.prenom} {s.nom}" for s in suspects]
            suspects_block = "👥 Suspects:\n" + "\n".join(suspects_lines)
        else:
            suspects_block = "👥 Suspects: aucun"

        # Détail armes
        if armes:
            armes_lines = []
            for a in armes:
                label = a.type
                if a.numero_serie:
                    label += f" (n° {a.numero_serie})"
                armes_lines.append(f"   - {label}")
            armes_block = "🔪 Armes:\n" + "\n".join(armes_lines)
        else:
            armes_block = "🔪 Armes: aucune"

        # Détail lieux
        if lieux:
            lieux_lines = []
            for l in lieux:
                label = l.nom
                if l.adresse:
                    label += f" ({l.adresse})"
                lieux_lines.append(f"   - {label}")
            lieux_block = "📍 Lieux:\n" + "\n".join(lieux_lines)
        else:
            lieux_block = "📍 Lieux: aucun"

        return (
            f"🗂️ {self.affaire.titre}\n"
            f"📅 {date}\n"
            f"📍 {ville} ({cp})\n"
            f"\n"
            f"{suspects_block}\n"
            f"\n"
            f"{armes_block}\n"
            f"\n"
            f"{lieux_block}\n"
            f"\n"
            f"⬤ {statut}"
        )
