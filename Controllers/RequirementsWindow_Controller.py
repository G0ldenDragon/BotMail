from Constants import LANGUAGES
from Views.RequirementsWindow_View import RequirementsWindow_View

class RequirementsWindow_Controller:
    def __init__(self, container, model):
        self.container = container
        self.model = model
        self.view = RequirementsWindow_View(container, self)

        # Add the view to its parent using a layout manager
        self.view.grid(row=0, column=0, sticky="nsew")


    # # Traitement de la modification de la langue
    # def language_modification(self, language):
    #     self.language = language
    #
    #     self.update_view()
    #
    #
    # # Traitement de la sélection de la langue
    # def language_selection(self, language):
    #     print("Langue choisie : " + self.language)
    #     # Sauvegarde du choix de la langue dans le .env
    #     self.model.set_variable("LANGUAGE", self.language)


    # Affiche une erreur utilisateur et dans la console/log
    def show_error(self, message):
        print("ERROR - " + message)
        # self.view.update_error_message(message)


    # # Modifie la vue en fonction de la langue
    # def update_view(self):
    #     languageChangements = {
    #         "FR" : {
    #             "button" : "Choisir cette langue",
    #             "error" : "Veuillez choisir une langue."
    #         },
    #         "EN" : {
    #             "button" : "Choose this language",
    #             "error" : "Please choose a language."
    #         }
    #     }
    #
    #     if self.language in LANGUAGES:
    #         self.view.update_button_message(languageChangements[self.language]["button"])
    #     else:
    #         self.show_error(languageChangements["FR"]["error"])


    # Renvoie la vue de ce controlleur
    def show_page(self):
        self.view.tkraise()