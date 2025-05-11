from tkinter import ttk

from Constants import LANGUAGES
from Views.LanguageWindow_View import LanguageWindow_View

class LanguageWindow_Controller(ttk.Frame):
    def __init__(self, container, model):
        super().__init__(container)
        self.container = container
        self.model = model
        self.view = LanguageWindow_View(container, self)

        # Add the view to its parent using a layout manager
        self.view.grid(row=0, column=0, sticky="nsew")

        self.language = None
        self.languageChangements = {
            "FR" : {
                "button" : "Choisir cette langue",
                "error" : "Veuillez choisir une langue."
            },
            "EN" : {
                "button" : "Choose this language",
                "error" : "Please choose a language."
            }
        }


    # Traitement de la modification de la langue
    def language_modification(self, language):
        self.language = language

        self.update_view()


    # Traitement de la sélection de la langue
    def language_selection(self, language):
        if self.language in LANGUAGES:
            print("Langue choisie : " + self.language)
            # Sauvegarde du choix de la langue dans le .env
            self.model["environmentVariable_Model"].set_variable("LANGUAGE", self.language)

            # Passage à l'écran 
            self.container.master.show_page("mainWindow_Controller")

        else:
            self.show_error(self.languageChangements["FR"]["error"])


    # Affiche une erreur utilisateur et dans la console/log
    def show_error(self, message):
        print("ERROR - " + message)
        self.view.update_error_message(message)


    # Modifie la vue en fonction de la langue
    def update_view(self):
        self.view.update_button_message(self.languageChangements[self.language]["button"])


    # Renvoie la vue de ce controlleur
    def show_page(self):
        self.view.tkraise()