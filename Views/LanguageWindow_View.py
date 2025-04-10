import tkinter as tk
from tkinter import ttk

from Constants import LANGUAGES

class LanguageWindow_View(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selectedLanguage = tk.StringVar()

        # Permet l'affichage d'un message d'erreur
        self.errorLabel = tk.Label(self, text="", fg="red")
        self.errorLabel.pack()

        # Création du menu déroulant (Combobox)
        self.dropdownLanguage = ttk.Combobox(
            self,
            textvariable=self.selectedLanguage,
            values=LANGUAGES,
            state="readonly"
        )
        self.dropdownLanguage.set("Please, select your language")
        self.dropdownLanguage.pack(padx=20, pady=10)
        self.dropdownLanguage.bind("<<ComboboxSelected>>", self.dropdown_language_modification)

        # Bouton avec commande liée
        self.button = ttk.Button(
            self,
            text="Choose this language",
            command=self.button_language_selection
        )
        self.button.pack(pady=10)


    # Fonction appelée lors de la modification dans la combobox
    def dropdown_language_modification(self, event=None):
        self.controller.language_modification(self.selectedLanguage.get())


    # Fonction appelé lors du clique sur le bouton
    def button_language_selection(self):
        self.controller.language_selection(self.selectedLanguage.get())


    # Permet l'affichage d'un message d'erreur
    def update_error_message(self, message):
        self.errorLabel.config(text=message)


    # Permet la modification du message du button
    def update_button_message(self, message):
        self.button.config(text=message)