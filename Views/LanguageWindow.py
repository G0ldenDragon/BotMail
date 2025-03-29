import tkinter as tk
from tkinter import ttk

from Constants import LANGUAGES

class LanguageWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Le contrôleur est maintenant correctement passé

        # Variable pour stocker la langue sélectionnée
        self.selected_value = tk.StringVar(value="FR")

        # Création du menu déroulant (Combobox)
        self.dropdown = ttk.Combobox(
            self,
            textvariable=self.selected_value,
            values=LANGUAGES
        )
        self.dropdown.state(["readonly"])  # Empêche l'utilisateur de taper directement
        self.dropdown.pack(padx=20, pady=10)

        # Bouton pour afficher la sélection et aller à la Page 2
        self.button = ttk.Button(
            self,
            text="Confirmer",
            command=self.on_language_selected  # Lier à une méthode locale
        )
        self.button.pack(pady=10)

    def on_language_selected(self):
        """Appelle le contrôleur pour gérer la langue et redirige vers Page 2"""
        selected_language = self.selected_value.get()

        # Appelle le contrôleur pour traiter la langue sélectionnée et rediriger l'utilisateur
        if hasattr(self.controller, "languageSetter"):
            self.controller.languageSetter(selected_language)
