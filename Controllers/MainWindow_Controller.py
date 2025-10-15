# Controllers/MainWindow_Controller.py

from Views.MainWindow_View import MainWindow_View


from Constants import CORRECT_SHEET_FILE_EXTENSIONS, CORRECT_DOCUMENT_FILE_EXTENSIONS


class MainWindow_Controller:
    def __init__(self, model, screen_name: str):
        self.model = model
        self.screen_name = screen_name
        self.view = MainWindow_View(self, name=screen_name)


    # Obtention des différents format de tableur possible
    def get_available_file_extensions(self, fileType):
        return [
            self.get_translation("document_file") if fileType == "document" else self.get_translation("sheet_file"),
            "".join(f"*{ext} " for ext in (
                CORRECT_DOCUMENT_FILE_EXTENSIONS if fileType == "document"
                else CORRECT_SHEET_FILE_EXTENSIONS
            ))
        ]


    # Traitement de la modification de la langue
    def file_sheet_selector(self, path):
        self.model["environmentVariable_Model"].set_variable("FILE_SHEET_PATH", path)


    # Traitement de la sélection de la langue
    def language_selection(self, language):
        print("Langue choisie : " + self.language)
        # Sauvegarde du choix de la langue dans le .env
        self.model.set_variable("LANGUAGE", self.language)


    # Affiche une erreur utilisateur et dans la console/log
    def show_error(self, message):
        print("ERROR - " + message)
        # self.view.update_error_message(message)


    # Renvoie la vue de ce controlleur
    def show_page(self):
        self.container.clear_widgets()
        self.container.add_widget(self.view)


    # Fonction pour l'utilisation de la traduction sur la vue
    def get_translation(self, variable: str):
        return self.model["language"].get_translation(self.screen_name, variable)
