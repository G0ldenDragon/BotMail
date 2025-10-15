# Controllers/LanguageWindow_Controller.py

from Models.EnvironmentVariable import *
from Views.LanguageWindow_View import LanguageWindow_View


from Constants import LANGUAGES


class LanguageWindow_Controller:
    def __init__(self, model, screen_name: str):
        self.model = model
        self.screen_name = screen_name
        self.view = LanguageWindow_View(self, name=screen_name, size_hint=(1, 1))

        self.language = None



    # Traitement de la modification de la langue
    def language_modification(self, language):
        # Sauvegarde du choix de la langue dans le .env
        set_variable("LANGUAGE", language)
        # Charge le bon fichier de langue 
        self.model["language"].update_selected_language()

        self.update_view()



    # Traitement de la sélection de la langue
    def language_selection(self):
        if get_variable("LANGUAGE") in LANGUAGES:            

            # Passage à l'écran principal
            self.view.show_page("main")

        else:
            self.show_error(self.get_translation("error"))



    # Modifie la vue en fonction de la langue
    def update_view(self):
        self.view.update_button_message(self.get_translation("button"))



    # Affiche une erreur utilisateur et dans la console/log
    def show_error(self, message):
        print("ERROR - " + message)
        self.view.update_error_message(message)



    # Fonction pour l'utilisation de la traduction sur la vue
    def get_translation(self, variable: str):
        return self.model["language"].get_translation(self.screen_name, variable)
