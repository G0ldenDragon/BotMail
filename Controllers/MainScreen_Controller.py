# Controllers/MainScreen_Controller.py

from Models.EnvironmentVariable import load_env, get_variable, set_variable
load_env()

from Views.MainScreen_View import MainScreen_View


from Constants import CORRECT_SHEET_FILE_EXTENSIONS, CORRECT_DOCUMENT_FILE_EXTENSIONS


class MainScreen_Controller:
    def __init__(self, model, screen_name: str):
        self.model = model
        self.screen_name = screen_name
        self.view = MainScreen_View(self, name=screen_name)



    # Obtention des différents format de tableur possible
    def get_sorted_file_explorer(self, fileType: str) -> list:
        """
        Args :
            filetype (str) : Pouvant être : document_file ; sheet_file ; pdf_file ; generic_document_file
        """
        sorted_extensions = []

        self.filter_sheets = [
            (
                "Excel/Calc files " + ", ".join(CORRECT_SHEET_FILE_EXTENSIONS),
                ";".join(f"*{ext}" for ext in CORRECT_SHEET_FILE_EXTENSIONS)
            )
        ]


        if fileType == "document_file":
            sorted_extensions = [(
                self.get_translation("document_file") + ", ".join(CORRECT_DOCUMENT_FILE_EXTENSIONS),
                ";".join(f"*{ext}" for ext in CORRECT_DOCUMENT_FILE_EXTENSIONS)
            )]
        elif fileType == "sheet_file":
            sorted_extensions = [(
                self.get_translation("sheet_file") + ", ".join(CORRECT_SHEET_FILE_EXTENSIONS),
                ";".join(f"*{ext}" for ext in CORRECT_SHEET_FILE_EXTENSIONS)
            )]
        elif fileType == "pdf_file":
            sorted_extensions = [(
                self.get_translation("sheet_file") + ".pdf",
                "*.pdf"
            )]
        elif fileType == "generic_document_file":
            sorted_extensions = [(
                self.get_translation("sheet_file") + ", ".join(CORRECT_DOCUMENT_FILE_EXTENSIONS)  + ", .pdf",
                ";".join(f"*{ext}" for ext in CORRECT_SHEET_FILE_EXTENSIONS) + ";*.pdf"
            )]
        else:
            raise KeyError("Mauvais argument")

        return sorted_extensions



    # Traitement de la modification de la langue
    def file_sheet_selector(self, path):
        set_variable("FILE_SHEET_PATH", path)

    

    # Modifie la vue en fonction de la langue
    def _update_view(self):
        self.view.update_button_text(self.get_translation("button"))



    # Affiche une erreur utilisateur et dans la console/log
    def _show_error(self, message):
        print("ERROR - " + message)
        # self.view.update_error_message(message)



    # Fonction pour l'utilisation de la traduction sur la vue
    def get_translation(self, variable: str):
        return self.model["language"].get_translation(self.screen_name, variable)
