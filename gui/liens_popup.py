import tkinter as tk

class LiensPopup(tk.Toplevel):
    def __init__(self, parent, communs):
        super().__init__(parent)
        self.title("🔗 Liens communs")

        for c in communs:
            tk.Label(self, text="• " + c).pack(anchor="w", padx=10)

        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.lift()
