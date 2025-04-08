from Constants import LANGUAGES
from Views.LanguageWindow_View import LanguageWindow_View

class LanguageWindow_Controller:
    def __init__(self, container, model):
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
    def languageModification(self, language):
        self.language = language

        self.updateView()


    # Traitement de la sélection de la langue
    def languageSelection(self, language):
        if self.language in LANGUAGES:
            print("Langue choisie : " + self.language)
            # Sauvegarde du choix de la langue dans le .env
            self.model.setVariable("LANGUAGE", self.language)
            self.container.master.show_page("requirementsWindow_Controller")

        else:
            self.showError(self.languageChangements["FR"]["error"])


    # Affiche une erreur utilisateur et dans la console/log
    def showError (self, message):
        print("ERROR - " + message)
        self.view.updateErrorMessage(message)


    # Modifie la vue en fonction de la langue
    def updateView(self):
        self.view.updateButtonMessage(self.languageChangements[self.language]["button"])


    # Renvoie la vue de ce controlleur
    def showPage(self):
        self.view.tkraise()