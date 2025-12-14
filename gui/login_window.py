import tkinter as tk
from tkinter import messagebox

from backend.auth import has_agent, create_agent, authenticate


class LoginWindow(tk.Toplevel):
    def init(self, parent, on_success):
        super().init(parent)
        self.on_success = on_success

        self.title("Connexion")
        self.geometry("300x200")
        self.resizable(False, False)
        self.grab_set()

        tk.Label(self, text="Identifiant").pack(pady=(10, 0))
        self.var_user = tk.StringVar()
        tk.Entry(self, textvariable=self.var_user).pack()

        tk.Label(self, text="Mot de passe").pack(pady=(10, 0))
        self.var_pass = tk.StringVar()
        tk.Entry(self, textvariable=self.var_pass, show="*").pack()

        tk.Button(self, text="Connexion", command=self.login).pack(pady=10)

        if not has_agent():
            messagebox.showinfo(
                "Initialisation",
                "Aucun utilisateur trouvé.\nCréation du compte administrateur."
            )

    # ------------------------------------------------

    def login(self):
        user = self.var_user.get().strip()
        pwd = self.var_pass.get().strip()

        if not user or not pwd:
            return messagebox.showerror("Erreur", "Champs obligatoires")

        if not has_agent():
            create_agent(user, pwd)
            messagebox.showinfo("Succès", "Compte administrateur créé.")
            self.on_success()
            self.destroy()
            return

        agent_id = authenticate(user, pwd)
        if agent_id:
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")