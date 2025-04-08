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
    # def languageModification(self, language):
    #     self.language = language
    #
    #     self.updateView()
    #
    #
    # # Traitement de la sélection de la langue
    # def languageSelection(self, language):
    #     print("Langue choisie : " + self.language)
    #     # Sauvegarde du choix de la langue dans le .env
    #     self.model.setVariable("LANGUAGE", self.language)


    # Affiche une erreur utilisateur et dans la console/log
    def showError (self, message):
        print("ERROR - " + message)
        # self.view.updateErrorMessage(message)


    # # Modifie la vue en fonction de la langue
    # def updateView(self):
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
    #         self.view.updateButtonMessage(languageChangements[self.language]["button"])
    #     else:
    #         self.showError(languageChangements["FR"]["error"])


    # Renvoie la vue de ce controlleur
    def showPage(self):
        self.view.tkraise()