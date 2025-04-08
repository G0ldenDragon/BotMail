import tkinter as tk
from tkinter import ttk

from Constants import LANGUAGES

class RequirementsWindow_View(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selectedLanguage = tk.StringVar()

        # Permet l'affichage d'un message d'erreur
        self.errorLabel = tk.Label(self, text="", fg="red")
        self.errorLabel.pack()

        # Bouton avec commande liée
        self.button = ttk.Button(
            self,
            text="TEST",
            command=self.buttonLanguageSelection
        )
        self.button.pack(pady=10)


    # Fonction appelée lors de la modification dans la combobox
    def dropdownLanguageModification(self, event=None):
        self.controller.languageModification(self.selectedLanguage.get())


    # Fonction appelé lors du clique sur le bouton
    def buttonLanguageSelection(self):
        self.controller.languageSelection(self.selectedLanguage.get())


    # Permet l'affichage d'un message d'erreur
    def updateErrorMessage(self, message):
        self.errorLabel.config(text=message)


    # Permet la modification du message du button
    def updateButtonMessage(self, message):
        self.button.config(text=message)