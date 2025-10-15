# Controllers/LanguageScreen_Controller.py

from Models.EnvironmentVariable import load_env, get_variable, set_variable
load_env()

from Views.LanguageScreen_View import LanguageScreen_View


from Constants import LANGUAGES


class LanguageScreen_Controller:
    def __init__(self, model, screen_name: str):
        self.model = model
        self.screen_name = screen_name
        self.view = LanguageScreen_View(self, name=screen_name, size_hint=(1, 1))



    # Traitement de la modification de la langue
    def language_modification(self, language: str) -> None:
        # Sauvegarde du choix de la langue dans le .env
        set_variable("LANGUAGE", language)
        # Charge le bon fichier de langue 
        self.model["language"].update_selected_language()

        self._update_screen_view()



    # Traitement de la sélection de la langue
    def language_selection(self) -> None:
        if get_variable("LANGUAGE") in LANGUAGES:            

            # Passage à l'écran principal
            self.view.show_page("screen_main")

        else:
            self._show_error(self.get_translation("error"))



    # Modifie la vue en fonction de la langue
    def _update_screen_view(self) -> None:
        self.view.update_button_text(self.get_translation("button"))



    # Affiche une erreur utilisateur et dans la console/log
    def _show_error(self, message: str) -> None:
        print("ERROR - " + message)
        self.view.update_error_message(message)



    # Fonction pour l'utilisation de la traduction sur la vue
    def get_translation(self, variable: str):
        return self.model["language"].get_translation(self.screen_name, variable)
