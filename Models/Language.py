# Models/Language.py

import json
from pathlib import Path


from Models.EnvironmentVariable import *


LANG_FOLDER_PATH = Path(__file__).parent / "../lang"
DEFAULT_LANGUAGE = "EN"


class Language():
    """
    Gère la langue à afficher en fonction des fichiers de langues.
    Sélectionner une langue à partir de ses deux premières lettres (Par exemple : EN ; FR), définit le fichier à utiliser.

    Attributes:
        translation (dict): Contient les informations contenues dans le fichier JSON utilisé.

    Methods:
        load_language_file: Récupère les information JSON et les retourne.
        update_selected_language: Met à jour la langue et translation à partir de la variable d'environnement LANGUAGE.
        get_translation: Permet l'obtention des informations contenues dans une variable de translation.
    """
    def __init__(self):
        language = get_variable("LANGUAGE") if get_variable("LANGUAGE") else DEFAULT_LANGUAGE

        language_file = (LANG_FOLDER_PATH / f"{language}.json").resolve()
        self.translation = self.load_language_file(language_file)


    def load_language_file(self, language_file: str) -> dict:
        """
        Récupère les informations d'un des fichiers de langue.

        Args:
            language_file (str): Nom du fichier de langue.

        Returns:
            dict: L'ensemble des informations/variables contenues dans le fichier de langue JSON.
        """
        try:
            with open(language_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as e:
            raise Exception("Le fichier de langue demandé n'a pas été trouvé.")
        except:
            raise IOError("DEBUG : Une erreur avec le fichier de langue est survenue.")


    def update_selected_language(self) -> None:
        """
        Met à jour la langue sélectionnée à partir de la variable d'environnement "LANGUAGE".
        """
        selected_language = get_variable("LANGUAGE")
        language_file = (LANG_FOLDER_PATH / f"{selected_language}.json").resolve()
        self.translation = self.load_language_file(language_file)


    def get_translation(self, screen_name: str, variable: str) -> any:
        """
        Récupère l'information contenue dans un variable du fichier de langue JSON.

        Args:
            screen_name (str): Nom destinée au script / screen.
            variable (str): Nom de la variable souhaitée au sein du script.

        Returns:
            any: Valeur contenue dans la variable.
        """
        return self.translation[screen_name][variable]
