"""

Ce fichier a été commenté par une intelligence artificielle (ChatGpt)

"""

# Librairie standard pour interfaces graphiques en Python
import tkinter as tk

# Boîtes de dialogue (erreurs, infos)
from tkinter import messagebox

# Fonctions d'authentification backend
from backend.auth import has_agent, create_agent, authenticate

# Logger pour tracer les actions GUI
from backend.logger import get_logger

# Initialisation du logger
log = get_logger()


# Fenêtre de connexion (popup)
class LoginWindow(tk.Toplevel):

    def __init__(self, parent, on_success):
        # Initialise une fenêtre fille liée à la fenêtre principale
        super().__init__(parent)

        # Callback appelé après connexion réussie
        self.on_success = on_success

        # Configuration de la fenêtre
        self.title("Connexion")
        self.geometry("300x200")
        self.resizable(False, False)

        # Empêche l'interaction avec la fenêtre principale
        self.grab_set()

        # ======================
        # Champs de saisie
        # ======================

        # Label + champ identifiant
        tk.Label(self, text="Identifiant").pack(pady=(10, 0))
        self.var_user = tk.StringVar()
        tk.Entry(self, textvariable=self.var_user).pack()

        # Label + champ mot de passe (masqué)
        tk.Label(self, text="Mot de passe").pack(pady=(10, 0))
        self.var_pass = tk.StringVar()
        tk.Entry(self, textvariable=self.var_pass, show="*").pack()

        # Bouton de connexion
        tk.Button(self, text="Connexion", command=self.login).pack(pady=10)

        # ======================
        # Initialisation admin
        # ======================

        # Si aucun agent n'existe, on force la création d'un admin
        if not has_agent():
            log.warning(
                "Aucun agent détecté – création du compte administrateur requise"
            )
            messagebox.showinfo(
                "Initialisation",
                "Aucun utilisateur trouvé.\n"
                "Veuillez créer le compte administrateur."
            )

        # Gestion de la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        log.info("Fenêtre de login affichée")

    # ------------------------------------------------
    # Tentative de connexion
    # ------------------------------------------------

    def login(self):
        # Récupération et nettoyage des champs
        user = self.var_user.get().strip()
        pwd = self.var_pass.get().strip()

        # Vérification des champs obligatoires
        if not user or not pwd:
            return messagebox.showerror(
                "Erreur", "Champs obligatoires"
            )

        # ----- Création admin si aucun agent -----
        if not has_agent():
            # Création du premier compte administrateur
            create_agent(user, pwd)
            log.info(f"Compte administrateur créé via GUI : {user}")

            messagebox.showinfo(
                "Succès", "Compte administrateur créé."
            )

            # Connexion automatique après création
            self._success()
            return

        # ----- Authentification classique -----
        agent_id = authenticate(user, pwd)

        # Connexion réussie
        if agent_id:
            log.info(f"Connexion GUI réussie : {user}")
            self._success()
        else:
            # Connexion échouée
            log.warning(f"Échec connexion GUI : {user}")
            messagebox.showerror(
                "Erreur", "Identifiants incorrects"
            )

    # ------------------------------------------------
    # Connexion réussie
    # ------------------------------------------------

    def _success(self):
        # Ferme la fenêtre de login
        self.destroy()

        # Appelle la fonction de succès (ouvre le GUI principal)
        self.on_success()

    # ------------------------------------------------
    # Fermeture forcée de l'application
    # ------------------------------------------------

    def quit_app(self):
        log.warning(
            "Fermeture de l'application depuis la fenêtre de login"
        )

        # Ferme complètement l'application
        self.master.destroy()
