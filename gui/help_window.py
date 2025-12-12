import tkinter as tk
from tkinter import ttk


class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Aide — Utilisation de l'application")
        self.geometry("520x650")
        self.resizable(True, True)

        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="📘 Aide de l'application",
                          font=("Arial", 16, "bold"))
        title.pack(pady=10)

        text = tk.Text(frame, wrap="word", font=("Arial", 11),
                       bg="#f0f0f0", relief="flat")
        text.pack(fill="both", expand=True)

        help_text = """
============================================
🟨 1. Déplacement des Post-it
============================================
• Cliquez avec le bouton droit sur un post-it.
• Déplacez la souris pour le bouger.
• Relâchez le bouton pour sauvegarder automatiquement
  la nouvelle position.

La position est immédiatement enregistrée dans la base.

============================================
🟦 2. Ouvrir / Modifier un élément
============================================
• Cliquez avec le bouton gauche sur un post-it.
• Une fenêtre de détails s'ouvre automatiquement.
• Vous pouvez modifier les champs.
• Cliquez sur Sauvegarder pour enregistrer.

La base de données se met à jour immédiatement.

============================================
🟪 3. Créer une nouvelle entité
============================================
Dans le menu de gauche, cliquez sur :
• "➕ Nouvelle affaire"
• "➕ Nouveau suspect"
• "➕ Nouvelle arme"
• "➕ Nouvelle preuve"
• "➕ Nouveau lieu"

Une fenêtre de création apparaîtra avec les champs appropriés.

============================================
🟥 4. Créer un lien entre deux entités
============================================
1. Cliquez sur "🔗 Créer un lien" dans le menu.
2. Choisissez :
   - Entité 1
   - Entité 2
   - Type de lien (ex : suspect, lieu, preuve…)
3. Cliquez sur "Créer le lien".

Un trait coloré apparaîtra sur la carte.

============================================
⬜ 5. Supprimer un lien
============================================
• Cliquez sur n’importe quel trait (liaison).
• Une confirmation apparaîtra.
• Validez pour supprimer.

============================================
🟧 6. Zoom et déplacement global (Canvas)
============================================
• 🔍 Zoom avant = molette vers le haut.
• 🔎 Zoom arrière = molette vers le bas.
• ✋ Déplacement global = clique MIDDLE (scroll) + bouger.

(This feature must be enabled in your canvas code.)

============================================
🟩 7. Rafraîchir l'affichage
============================================
• Cliquez sur le bouton "Actualiser" dans le menu.
• Tous les post-it et les liens seront redessinés.

============================================
💾 8. Les données sont-elles sauvegardées ?
============================================
Oui ! Toute modification (déplacement, édition, création,
suppression de lien…) est enregistrée directement dans la
base SQLite.

============================================
""".strip()

        text.insert("1.0", help_text)
        text.config(state="disabled")

