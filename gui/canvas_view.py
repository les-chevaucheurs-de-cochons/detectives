import tkinter as tk
from gui.affaire_widget import AffaireWidget
from gui.liens_popup import LiensPopup
from gui.affaire_form import AffaireForm
from gui.styles import COLOR_BG, COLOR_LINK
from gui.filtre_popup import FiltrePopup


class CanvasView(tk.Canvas):
    def __init__(self, parent, gestion):
        super().__init__(parent, bg=COLOR_BG)
        self.gestion = gestion
        self.widgets = {}          # id_affaire -> AffaireWidget
        self.liens = []
        self.affaires_filtrees = None  # None = pas de filtre

        # =====================
        # Déplacement du mur (PAN)
        # =====================
        self.bind("<ButtonPress-3>", self.start_pan)  # clic droit
        self.bind("<B3-Motion>", self.do_pan)

        self.refresh()

    # ------------------------------------------------
    # PAN DU MUR
    # ------------------------------------------------

    def start_pan(self, event):
        self.scan_mark(event.x, event.y)

    def do_pan(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

    # ------------------------------------------------
    # RAFRAÎCHISSEMENT
    # ------------------------------------------------

    def refresh(self):
        self.delete("all")
        self.widgets.clear()
        self.liens.clear()

        # Affaires visibles (filtrées ou non)
        affaires = self.affaires_filtrees or self.gestion.get_affaires()

        for a in affaires:
            self.widgets[a.id_affaire] = AffaireWidget(self, a, self.gestion, self)

        self.dessiner_liens()

    # ------------------------------------------------
    # LIENS
    # ------------------------------------------------

    def dessiner_liens(self):
        self.liens = []

        affaires = (
            self.affaires_filtrees
            if self.affaires_filtrees is not None
            else self.gestion.get_affaires()
        )

        for a in affaires:
            for autre in affaires:
                if a.id_affaire >= autre.id_affaire:
                    continue

                communs = self._communs(a, autre)
                if communs:
                    # sécurité : les deux doivent être visibles
                    if a.id_affaire not in self.widgets or autre.id_affaire not in self.widgets:
                        continue

                    x1, y1 = self.widgets[a.id_affaire].center()
                    x2, y2 = self.widgets[autre.id_affaire].center()

                    line = self.create_line(
                        x1, y1, x2, y2,
                        fill=COLOR_LINK,
                        width=2,
                        tags=("lien",)
                    )

                    # 🔽 lien sous les post-it
                    self.tag_lower(line)

                    self.tag_bind(
                        line,
                        "<Button-1>",
                        lambda e, c=communs: LiensPopup(self, c)
                    )

                    self.liens.append(line)

    def redraw_links(self):
        for line in self.liens:
            self.delete(line)
        self.dessiner_liens()

    # ------------------------------------------------
    # DÉTECTION DES COMMUNS
    # ------------------------------------------------

    def _communs(self, a1, a2):
        communs = []

        if {s.id_suspect for s in a1.get_suspects()} & {s.id_suspect for s in a2.get_suspects()}:
            communs.append("Suspect commun")

        if {ar.id_arme for ar in a1.get_armes()} & {ar.id_arme for ar in a2.get_armes()}:
            communs.append("Arme commune")

        if {l.id_lieu for l in a1.get_lieux()} & {l.id_lieu for l in a2.get_lieux()}:
            communs.append("Lieu commun")

        return communs

    # ------------------------------------------------
    # ACTIONS
    # ------------------------------------------------

    def ajouter_affaire(self):
        AffaireForm(self, self.gestion, on_close=self.refresh)

    def filtrer_affaires(self):
        FiltrePopup(self, self.gestion, self)

    def appliquer_filtre(self, affaires):
        self.affaires_filtrees = affaires
        self.refresh()

    def reset_filtre(self):
        self.affaires_filtrees = None
        self.refresh()
