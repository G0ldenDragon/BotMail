import os
import pandas as pd
import ntpath
from Constants import COLUMNS
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# ---------------------------------------

FILE_SHEET_RESULT_PATH = os.getenv("FILE_SHEET_RESULT_PATH")

# ---------------------------------------

def nomFichierDuChemin(chemin):
    chemin, fichier = ntpath.split(chemin)
    return fichier or ntpath.basename(chemin)

# ---------------------------------------
# Choix de l'utilisateur
def confirmationUtilisateur(userConfirmation: dict[str, dict[str, list[str]]]):
    userInput = ""
    messageInput = userConfirmation[os.getenv("LANGUAGE")]["messageInput"]

    for index, choix in enumerate(userConfirmation[os.getenv("LANGUAGE")]["confirmation"]):
        messageInput += f'{index+1}) {choix}\n'

    messageInput += '-> '

    while userInput not in userConfirmation[os.getenv("LANGUAGE")]["confirmation"]:
        userInput = input(messageInput)

    print("")
    return userInput

# ---------------------
# Ajout dans le fichier CSV Résultat
def resultatCSV(resultMessage, dataSerializer):
    try:
        newLine = pd.DataFrame([[resultMessage, dataSerializer.recipientEmail, dataSerializer.recipientName, dataSerializer.recipientAddress, dataSerializer.recipientPhone]], columns = COLUMNS)
        newLine.to_csv(FILE_SHEET_RESULT_PATH, mode='a', header=False, index=False, sep=';')

    except Exception as e:
        MessagePrinter({
            "FR" : "ERREUR : Une erreur durant l'enregistrement des résultats s'est produite : \n" + str(e),
            "EN" : "ERROR : An error occurred during the saving of the results.\n" + str(e)
        })
        exit()

# ---------------------
# Raise une exception de la langue utilisée.
def ExceptionRaiser(errorMessage: dict[str, str]):
    raise Exception(errorMessage[os.getenv("LANGUAGE")])

# ----------------------
# Affiche un message de la langue utilisée.
def MessagePrinter(message: dict[str, str]):
    print(message[os.getenv("LANGUAGE")])