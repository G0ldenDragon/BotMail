import Constants
from Views.LanguageWindow_View import LanguageWindow_View

class LanguageWindow_Controller:
    def __init__(self, container, model):
        self.container = container      # Référence au container principale (BotMailGUI)
        self.model = model  # Associe le modèle au contrôleur
        self.view = LanguageWindow_View(container, self)    # Associe la vue au contrôleur (peut être utilisé plus tard)

        # Add the view to its parent using a layout manager
        self.view.grid(row=0, column=0, sticky="nsew")  # Use grid for consistent layout

        self.language = None


    # Traitement de la modification de la langue
    def languageModification(self, language):
        self.language = language

        self.updateView()


    # Traitement de la sélection de la langue
    def languageSelection(self, language):
        print("Langue choisie : " + self.language)
        # Sauvegarde du choix de la langue dans le .env
        # self.model



    # Affiche une erreur utilisateur et dans la console/log
    def showError (self, message):
        print("ERROR - " + message)
        self.view.updateErrorMessage(message)


    # Modifie la vue en fonction de la langue
    def updateView(self):
        languageChangements = {
            "FR" : {
                "button" : "Choisir cette langue",
                "error" : "Veuillez choisir une langue."
            },
            "EN" : {
                "button" : "Choose this language",
                "error" : "Please choose a language."
            }
        }

        if self.language in Constants.LANGUAGES:
            self.view.updateButtonMessage(languageChangements[self.language]["button"])
        else:
            self.showError(languageChangements["FR"]["error"])


    # Renvoie la vue de ce controlleur
    def showPage(self):
        self.view.tkraise()