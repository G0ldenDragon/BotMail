from Constants import CORRECT_FILE_SHEET_EXTENSIONS
from Views.MainWindow_View import MainWindow_View

class MainWindow_Controller:
    def __init__(self, container, model):
        self.container = container
        self.model = model
        self.view = MainWindow_View(container, self)

        # Add the view to its parent using a layout manager
        self.view.grid(row=0, column=0, sticky="nsew")


    # Obtention des différents format de tableur possible
    def get_available_file_sheet_extensions(self):
        available_extensions = []
        for extension in CORRECT_FILE_SHEET_EXTENSIONS:
            available_extensions.append((
                self.model["Utilities_Model"].language_selector({
                        "FR" : "Fichier",
                        "EN" : "File"
                    }) + " " + extension.replace(".", "").upper(),
                "*" + extension
            ))
        return available_extensions


    # Traitement de la modification de la langue
    def file_sheet_selector(self, path):
        self.model["environmentVariable_Model"].set_variable("FILE_SHEET_PATH", path)
        print(path)
        # self.path_var.set(path)
        # self.display_content(path)


    # Traitement de la sélection de la langue
    def language_selection(self, language):
        print("Langue choisie : " + self.language)
        # Sauvegarde du choix de la langue dans le .env
        self.model.set_variable("LANGUAGE", self.language)


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
