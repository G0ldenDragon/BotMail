import os
import pandas as pd
from pathlib import Path
from Constants import COLUMNS
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# ---------------------------------------

FILE_SHEET_RESULT_PATH = os.getenv("FILE_SHEET_RESULT_PATH")

# ---------------------------------------

def fileName(chemin):
    return Path(chemin).name

# ---------------------------------------
# Choix de l'utilisateur
def confirmationUtilisateur(userConfirmation: dict[str, dict[str, list[str]]]) -> int:
    userInput = ""
    messageInput = userConfirmation[os.getenv("LANGUAGE")]["messageInput"]

    for index, choix in enumerate(userConfirmation[os.getenv("LANGUAGE")]["confirmation"]):
        messageInput += f'{index+1}) {choix}\n'

    messageInput += '-> '

    while True:
        userInput = input(messageInput)
        print("")
        if userInput in userConfirmation[os.getenv("LANGUAGE")]["confirmation"]:
            index = userConfirmation[os.getenv("LANGUAGE")]["confirmation"].index(userInput)
            return index

# ---------------------
# Ajout dans le fichier CSV Résultat
def resultatCSV(resultMessage, dataSerializer):
    try:
        newLine = pd.DataFrame([[resultMessage, dataSerializer.recipientEmail, dataSerializer.recipientName, dataSerializer.recipientAddress, dataSerializer.recipientPhone]], columns = COLUMNS)
        newLine.to_csv(FILE_SHEET_RESULT_PATH, mode='a', header=False, index=False, sep=';')

    except PermissionError as e:
        if resultMessage == "Envoyé !":
            ExceptionRaiser({
                "FR" : "ATTENTION ! Le mail a bien été envoyé mais l'état 'envoyé' n'a pas pu être inscrit dans la feuille de calcul car elle est ouvert dans un autre programme, veillez à ne pas remettre cette adresse mail lors d'une prochaine utilisation : " + dataSerializer.recipientEmail,
                "EN" : "WARNING! The email has been sent successfully, but the 'sent' status could not be recorded in the spreadsheet because it is open in another program. Please make sure not to reuse this email address in future use : " + dataSerializer.recipientEmail
            })

        else:
            ExceptionRaiser({
                "FR" : "La feuille de calcul de résultat donné est ouvert dans un autre programme, impossible de l'ouvrir.",
                "EN" : "The result sheet file provided is open in another program, it cannot be accessed."
            })

    except Exception as e:
        ExceptionRaiser({
            "FR" : "Une erreur durant l'enregistrement des résultats s'est produite : \n" + str(e),
            "EN" : "An error occurred during the saving of the results.\n" + str(e)
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