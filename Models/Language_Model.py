# Models/Language_Model.py

import json
from pathlib import Path


from Models.EnvironmentVariable_Model import *


LANG_FOLDER_PATH = Path(__file__).parent / "../lang"
DEFAULT_LANGUAGE = "FR"


class Language():
    """
    Gère la langue d'affichage de l'application en fonction des fichiers de langues.

    Args:
        key (str): Nom de la variable d'environnement.
        value (str): Nouvelle valeur de la variable d'environnement.
        env_file (str): Chemin d'accès vers le fichier .env.
    """
    def __init__(self):
        language_file = (LANG_FOLDER_PATH / f"{DEFAULT_LANGUAGE}.json").resolve()
        self.translation = self.load_language_file(language_file)


    def load_language_file(self, language_file) -> dict:
        try:
            with open(language_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as e:
            raise Exception("Le fichier de langue demandé n'a pas été trouvé.")
        except:
            raise IOError("DEBUG : Une erreur avec le fichier de langue est survenue.")


    def update_selected_language(self) -> None:
        selected_language = get_variable("LANGUAGE")
        language_file = (LANG_FOLDER_PATH / f"{selected_language}.json").resolve()
        self.translation = self.load_language_file(language_file)


    def get_translation(self, screen_name: str, variable: str):
        return self.translation[screen_name][variable]
