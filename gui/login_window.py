import tkinter as tk
from tkinter import messagebox

from backend.auth import has_agent, create_agent, authenticate
from backend.logger import get_logger

log = get_logger()


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)

        self.on_success = on_success

        self.title("Connexion")
        self.geometry("300x200")
        self.resizable(False, False)
        self.grab_set()  # bloque la fenêtre principale

        # ======================
        # Champs
        # ======================
        tk.Label(self, text="Identifiant").pack(pady=(10, 0))
        self.var_user = tk.StringVar()
        tk.Entry(self, textvariable=self.var_user).pack()

        tk.Label(self, text="Mot de passe").pack(pady=(10, 0))
        self.var_pass = tk.StringVar()
        tk.Entry(self, textvariable=self.var_pass, show="*").pack()

        tk.Button(self, text="Connexion", command=self.login).pack(pady=10)

        # ======================
        # Initialisation admin
        # ======================
        if not has_agent():
            log.warning("Aucun agent détecté – création du compte administrateur requise")
            messagebox.showinfo(
                "Initialisation",
                "Aucun utilisateur trouvé.\n"
                "Veuillez créer le compte administrateur."
            )

        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        log.info("Fenêtre de login affichée")

    # ------------------------------------------------

    def login(self):
        user = self.var_user.get().strip()
        pwd = self.var_pass.get().strip()

        if not user or not pwd:
            return messagebox.showerror("Erreur", "Champs obligatoires")

        # ----- Création admin si aucun agent -----
        if not has_agent():
            create_agent(user, pwd)
            log.info(f"Compte administrateur créé via GUI : {user}")
            messagebox.showinfo("Succès", "Compte administrateur créé.")
            self._success()
            return

        # ----- Authentification classique -----
        agent_id = authenticate(user, pwd)
        if agent_id:
            log.info(f"Connexion GUI réussie : {user}")
            self._success()
        else:
            log.warning(f"Échec connexion GUI : {user}")
            messagebox.showerror("Erreur", "Identifiants incorrects")

    # ------------------------------------------------

    def _success(self):
        self.destroy()
        self.on_success()

    def quit_app(self):
        log.warning("Fermeture de l'application depuis la fenêtre de login")
        self.master.destroy()
