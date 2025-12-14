import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#bbb", width=180)
        self.pack_propagate(False)

        tk.Label(self, text="Menu", bg="#bbb", font=("Arial", 12, "bold")).pack(pady=10)

        self.btn_add = tk.Button(self, text="➕ Nouvelle affaire")
        self.btn_add.pack(fill="x", padx=10, pady=5)

        self.btn_filter = tk.Button(self, text="🔍 Filtrer")
        self.btn_filter.pack(fill="x", padx=10, pady=5)

        tk.Frame(self, height=2, bg="#999").pack(fill="x", pady=10)

        self.btn_help = tk.Button(self, text="📖 Aide")
        self.btn_help.pack(fill="x", padx=10, pady=5)

    # ------------------------------------------------

    def set_actions(self, on_add=None, on_filter=None, on_help=None):
        if on_add:
            self.btn_add.config(command=on_add)
        if on_filter:
            self.btn_filter.config(command=on_filter)
        if on_help:
            self.btn_help.config(command=on_help)
