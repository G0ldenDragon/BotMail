import tkinter as tk
from tkinter import ttk

from Constants import LANGUAGES

class LanguageWindow_View(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selectedLanguage = tk.StringVar()

        # Création du menu déroulant (Combobox)
        self.dropdown = ttk.Combobox(
            self,
            textvariable=self.selectedLanguage,
            values=LANGUAGES,
            state="readonly"
        )
        self.dropdown.set("Please, select your language.")
        self.dropdown.pack(padx=20, pady=10)
        self.dropdown.bind("<<ComboboxSelected>>", self.languageSelection)

        # Bouton avec commande liée
        self.button = ttk.Button(
            self,
            text="Confirmer",
            command=self.languageFinalChoice
        )
        self.button.pack(pady=10)


    def languageSelection(self, event=None):
        """Fonction appelée lors de la sélection dans la combobox"""
        print("Sélection changée : ", self.selectedLanguage.get())
        # Vous pouvez ajouter ici un traitement immédiat si nécessaire

    def languageFinalChoice(self):
        """Gère la confirmation de la sélection"""
        if self.selectedLanguage.get():
            print("Confirmation :", self.selectedLanguage.get())
            self.controller.languageSetter(self.selectedLanguage.get())
        else:
            print("Veuillez sélectionner une langue")