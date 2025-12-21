"""
Ce fichier a été développé dans le cadre d’un projet étudiant.
Certaines parties du code ont été générées ou assistées par une intelligence artificielle
(ChatGPT), puis relues, comprises et adaptées par l’étudiant.

"""

import tkinter as tk

from gui.affaire_widget import AffaireWidget
from gui.liens_popup import LiensPopup
from gui.affaire_form import AffaireForm
from gui.filtre_popup import FiltrePopup
from gui.styles import COLOR_BG, COLOR_LINK
from gui.styles import POSTIT_WIDTH, POSTIT_HEIGHT


class CanvasView(tk.Canvas):
    """
    Canvas principal représentant le « mur d’enquête ».
    Il affiche les affaires sous forme de post-it et les liens entre elles.
    """

    def __init__(self, parent, gestion):
        """
        Constructeur du canvas.

        parent  : widget parent (MainWindow)
        gestion : instance de GestionEnquetes (logique métier)
        """
        super().__init__(parent, bg=COLOR_BG)

        # Référence vers la logique métier
        self.gestion = gestion

        # Dictionnaire id_affaire -> AffaireWidget
        self.widgets = {}

        # Liste des identifiants de lignes (liens entre affaires)
        self.liens = []

        # Liste des affaires filtrées (None = pas de filtre)
        self.affaires_filtrees = None

        # Texte affiché dans la sidebar pour indiquer le filtre actif
        self.filter_text = "Aucun"

        # Callback pour informer la sidebar d’un changement de filtre
        self.on_filter_changed = None

        # =====================
        # Déplacement du mur (PAN)
        # =====================
        # Clic droit + déplacement pour bouger la vue
        self.bind("<ButtonPress-3>", self.start_pan)
        self.bind("<B3-Motion>", self.do_pan)

        # Initialisation de l’affichage
        self.refresh()

        # Références vers les fenêtres popup
        self.popup_liens = None
        self.form_creation = None

    # ------------------------------------------------
    # PAN DU MUR
    # ------------------------------------------------

    def start_pan(self, event):
        """
        Marque le point de départ du déplacement du canvas.
        """
        self.scan_mark(event.x, event.y)

    def do_pan(self, event):
        """
        Déplace la vue du canvas lors du déplacement de la souris.
        """
        self.scan_dragto(event.x, event.y, gain=1)

    # ------------------------------------------------
    # ORGANISATION DU MUR
    # ------------------------------------------------

    def relayout_affaires(self):
        """
        Réorganise automatiquement les post-it sur le mur
        en les disposant en grille.
        """
        affaires = self.gestion.get_affaires()
        if not affaires:
            return

        margin_x = 40
        margin_y = 40
        spacing_x = POSTIT_WIDTH + 40
        spacing_y = POSTIT_HEIGHT + 40
        max_per_row = 4  # nombre de post-it par ligne

        for index, affaire in enumerate(affaires):
            row = index // max_per_row
            col = index % max_per_row

            x = margin_x + col * spacing_x
            y = margin_y + row * spacing_y

            # Mise à jour de la position de l’affaire
            affaire.update_position(int(x), int(y))

        self.reset_view()
        self.refresh()

    # ------------------------------------------------
    # RAFRAÎCHISSEMENT
    # ------------------------------------------------

    def refresh(self):
        """
        Rafraîchit complètement le canvas :
        - suppression des widgets existants
        - recréation des post-it
        - redessin des liens
        """
        self.delete("all")
        self.widgets.clear()
        self.liens.clear()

        # Utilise les affaires filtrées si un filtre est actif
        affaires = self.affaires_filtrees or self.gestion.get_affaires()

        for a in affaires:
            self.widgets[a.id_affaire] = AffaireWidget(self, a, self.gestion, self)

        self.dessiner_liens()

    # ------------------------------------------------
    # LIENS ENTRE AFFAIRES
    # ------------------------------------------------

    def dessiner_liens(self):
        """
        Dessine les liens entre les affaires ayant des éléments communs
        (suspects, armes, lieux).
        """
        self.liens = []

        affaires = (
            self.affaires_filtrees
            if self.affaires_filtrees is not None
            else self.gestion.get_affaires()
        )

        for a in affaires:
            for autre in affaires:
                # Évite les doublons et les auto-liens
                if a.id_affaire >= autre.id_affaire:
                    continue

                communs = self._communs(a, autre)
                if communs:
                    if a.id_affaire not in self.widgets or autre.id_affaire not in self.widgets:
                        continue

                    # Centre des deux post-it
                    x1, y1 = self.widgets[a.id_affaire].center()
                    x2, y2 = self.widgets[autre.id_affaire].center()

                    # Création de la ligne de lien
                    line = self.create_line(
                        x1, y1, x2, y2,
                        fill=COLOR_LINK,
                        width=2,
                        tags=("lien",)
                    )

                    # Place le lien sous les post-it
                    self.tag_lower(line)

                    # Clic sur le lien → popup des éléments communs
                    self.tag_bind(
                        line,
                        "<Button-1>",
                        lambda e, c=communs: self.show_liens_popup(c)
                    )

                    self.liens.append(line)

    def show_liens_popup(self, communs):
        """
        Affiche une popup listant les éléments communs entre deux affaires.
        """
        if getattr(self, "popup_liens", None) and self.popup_liens.winfo_exists():
            self.popup_liens.lift()
            self.popup_liens.focus_set()
            return

        self.popup_liens = LiensPopup(self, communs)

    def redraw_links(self):
        """
        Supprime et redessine tous les liens.
        """
        for line in self.liens:
            self.delete(line)

        self.dessiner_liens()

    # ------------------------------------------------
    # DÉTECTION DES ÉLÉMENTS COMMUNS
    # ------------------------------------------------

    def _communs(self, a1, a2):
        """
        Détecte les éléments communs entre deux affaires :
        - suspects
        - armes
        - lieux

        Retourne une liste de chaînes descriptives.
        """
        communs = []

        # -------------------------
        # SUSPECTS COMMUNS
        # -------------------------
        suspects1 = {s.id_suspect: s for s in a1.get_suspects()}
        suspects2 = {s.id_suspect: s for s in a2.get_suspects()}

        ids_communs = suspects1.keys() & suspects2.keys()
        if ids_communs:
            for sid in ids_communs:
                s = suspects1[sid]
                communs.append(f"👥 Suspect commun : {s.prenom} {s.nom}")

        # -------------------------
        # ARMES COMMUNES
        # -------------------------
        armes1 = {a.id_arme: a for a in a1.get_armes()}
        armes2 = {a.id_arme: a for a in a2.get_armes()}

        ids_communs = armes1.keys() & armes2.keys()
        if ids_communs:
            for aid in ids_communs:
                a = armes1[aid]
                label = a.type
                if a.numero_serie:
                    label += f" (n° {a.numero_serie})"
                communs.append(f"🔪 Arme commune : {label}")

        # -------------------------
        # LIEUX COMMUNS
        # -------------------------
        lieux1 = {l.id_lieu: l for l in a1.get_lieux()}
        lieux2 = {l.id_lieu: l for l in a2.get_lieux()}

        ids_communs = lieux1.keys() & lieux2.keys()
        if ids_communs:
            for lid in ids_communs:
                l = lieux1[lid]
                label = l.nom
                if l.adresse:
                    label += f" ({l.adresse})"
                communs.append(f"📍 Lieu commun : {label}")

        return communs

    # ------------------------------------------------
    # ACTIONS UTILISATEUR
    # ------------------------------------------------

    def ajouter_affaire(self):
        """
        Ouvre le formulaire de création d’une nouvelle affaire.
        """
        if self.form_creation is not None and self.form_creation.winfo_exists():
            self.form_creation.lift()
            self.form_creation.focus_set()
            return

        def _closed():
            self.form_creation = None
            self.refresh()

        self.form_creation = AffaireForm(self, self.gestion, on_close=_closed)

    def filtrer_affaires(self):
        """
        Ouvre la fenêtre de filtre des affaires.
        """
        FiltrePopup(self, self.gestion, self)

    def appliquer_filtre(self, affaires, label: str):
        """
        Applique un filtre sur les affaires affichées.
        """
        self.affaires_filtrees = affaires
        self.filter_text = label
        self.refresh()

        if self.on_filter_changed:
            self.on_filter_changed(label)

    def reset_filtre(self):
        """
        Supprime le filtre actif.
        """
        self.affaires_filtrees = None
        self.filter_text = "Aucun"
        self.refresh()

        if self.on_filter_changed:
            self.on_filter_changed("Aucun")

    def reset_view(self):
        """
        Réinitialise la position de la vue du canvas.
        """
        self.xview_moveto(0)
        self.yview_moveto(0)
