# Utilities.py

import os
import pandas as pd
from pathlib import Path


from Models.EnvironmentVariable_Model import load_env, get_variable, set_variable
load_env()
from Models.Language_Model import Language


from Constants import COLUMNS
FILE_SHEET_RESULT_PATH = get_variable("FILE_SHEET_RESULT_PATH")
UTILITIES = "utilities"


def file_name(chemin):
    return Path(chemin).name

# ---------------------------------------
# Choix de l'utilisateur
def user_confirmation(messageInput: str, userConfirmation: list[str]) -> int:
    userInput = ""

    for index, choix in enumerate(userConfirmation):
        messageInput += f'{index+1}) {choix}\n'

    messageInput += '-> '

    while True:
        userInput = input(messageInput)
        print("")
        if userInput in userConfirmation:
            index = userConfirmation.index(userInput)
            return index

# ---------------------
# Ajout dans le fichier CSV Résultat
def csv_result(resultMessage, data_serializer):
    language_Model = Language()

    try:
        newLine = pd.DataFrame([[resultMessage, data_serializer.recipientEmail, data_serializer.recipientName, data_serializer.recipientAddress, data_serializer.recipientPhone]], columns = COLUMNS)
        newLine.to_csv(FILE_SHEET_RESULT_PATH, mode='a', header=False, index=False, sep=';')

    except PermissionError as e:
        if resultMessage == "Envoyé !":
            exception_raiser(language_Model.get_translation(UTILITIES, "script_finished_but_sheet_opened").replace(";;;", data_serializer.recipientEmail))

        else:
            exception_raiser(language_Model.get_translation(UTILITIES, "exception_sheet_opened"))

    except Exception as e:
        exception_raiser(language_Model.get_translation(UTILITIES, "exception_sheet_general") + str(e))

# ---------------------
# Raise une exception de la langue utilisée.
def exception_raiser(errorMessage: str):
    raise Exception(errorMessage)

# ----------------------
# Affiche un message de la langue utilisée.
def message_printer(message: str):
    print(message)