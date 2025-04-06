from Views.LanguageWindow_View import LanguageWindow_View

class LanguageWindow_Controller:
    def __init__(self, container, model):
        self.container = container      # Référence au container principale (BotMailGUI)
        self.model = model  # Associe le modèle au contrôleur
        self.view = LanguageWindow_View(container, self)    # Associe la vue au contrôleur (peut être utilisé plus tard)

        # Add the view to its parent using a layout manager
        self.view.grid(row=0, column=0, sticky="nsew")  # Use grid for consistent layout

        self.language = None


    # Traitement de la modification
    def languageModification(self, language):
        self.language = language

        # # Redirige vers PageExample2 après avoir traité la langue
        # self.container.show_page("PageExample2")


    def showError (self, message):
        self.view.errorLabel.configure(text=message)


    def updateView(self):
        languageChangements = {
            "FR" : {
                "button" : "Choisir cette langue.",
                "error" : "Vous devez choisir une langue."
            },
            "EN" : {
                "button" : "Choose this language.",
                "error" : "You need to choose a language."
            }
        }

        if self.language is not None:
            self.view.button.configure(text=languageChangements[self.language]["button"])
        else:
            self.showError(languageChangements["FR"]["button"])


    def showPage(self):
        self.view.tkraise()