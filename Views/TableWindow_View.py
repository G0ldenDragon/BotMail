from tkinter import ttk
import tkinter as tk

MODERN_FONT = ("Segoe UI", 12)
COL_WIDTH = 50  # Largeur en caractères

class TableauInteractif(ttk.Frame):
    def __init__(self, parent, headers, boutons_a_cote=None, controller=None):
        super().__init__(parent)
        self.headers = headers
        self.n_colonnes = len(headers)
        if boutons_a_cote is None:
            boutons_a_cote = ["None"] * self.n_colonnes
        self.boutons_a_cote = boutons_a_cote
        self.controller = controller
        self.rows = []
        self.row_counter = 0

        # En-têtes avec largeur fixe
        for col, text in enumerate(headers):
            ttk.Label(self, text=text, font=(MODERN_FONT[0], 12, "bold"), width=COL_WIDTH, anchor="w").grid(
                row=0, column=col, padx=2, pady=2, sticky="nsew"
            )
            # Largeur minimale en pixels (approximativement 8px/char pour Consolas 11)
            self.grid_columnconfigure(col, minsize=COL_WIDTH * 8, weight=1)
        ttk.Label(self, text="").grid(row=0, column=self.n_colonnes)  # Pour la colonne du bouton de suppression

        # Champs d'ajout
        self.add_entries = [
            ttk.Entry(self, font=MODERN_FONT, width=COL_WIDTH) for _ in range(self.n_colonnes)
        ]
        self.add_buttons = []
        for i in range(self.n_colonnes):
            if self.boutons_a_cote[i] != "None":
                btn = ttk.Button(
                    self,
                    text="🔍",
                    width=2,
                    command=lambda: parent.master.master.button_file_selector(self.boutons_a_cote[i - 1])
                )
            else:
                btn = None
            self.add_buttons.append(btn)
        self.add_btn = ttk.Button(self, text="➕", command=self.add_row_from_entry, style="Add.TButton")

        self.refresh_table()

    def add_row_from_entry(self):
        values = [entry.get().strip() or f"Valeur {self.row_counter+1} col {i+1}" for i, entry in enumerate(self.add_entries)]
        self.add_row(*values)
        for entry in self.add_entries:
            entry.delete(0, tk.END)

    def add_row(self, *values):
        self.row_counter += 1
        values = list(values)
        while len(values) < self.n_colonnes:
            values.append(f"Valeur {self.row_counter} col {len(values)+1}")
        labels = [
            ttk.Label(self, text=val, font=MODERN_FONT, width=COL_WIDTH, anchor="w")
            for val in values
        ]
        delete_btn = ttk.Button(
            self, text="❌", command=lambda r=len(self.rows): self.delete_row(r), style="Del.TButton"
        )
        self.rows.append((labels, delete_btn))
        self.refresh_table()

    def delete_row(self, idx):
        for widget in self.rows[idx][0]:
            widget.grid_forget()
            widget.destroy()
        self.rows[idx][1].grid_forget()
        self.rows[idx][1].destroy()
        del self.rows[idx]
        self.refresh_table()

    def refresh_table(self):
        for i, (labels, delete_btn) in enumerate(self.rows, start=1):
            for col, label in enumerate(labels):
                label.grid(row=i, column=col, padx=2, pady=2, sticky="nsew")
            delete_btn.config(command=lambda r=i-1: self.delete_row(r))
            delete_btn.grid(row=i, column=self.n_colonnes, padx=2, pady=2, sticky="nsew")

        add_row = len(self.rows) + 1
        for w in self.add_entries + [btn for btn in self.add_buttons if btn] + [self.add_btn]:
            if w:
                w.grid_forget()
        for col, entry in enumerate(self.add_entries):
            entry.grid(row=add_row, column=col, sticky="ew", padx=(2, 0), pady=2)
            if self.boutons_a_cote[col] and self.add_buttons[col]:
                self.add_buttons[col].grid(row=add_row, column=col, sticky="e", padx=(0, 2), pady=2)
        self.add_btn.grid(row=add_row, column=self.n_colonnes, padx=2, pady=2, sticky="nsew")