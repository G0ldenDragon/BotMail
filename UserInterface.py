import os
import pandas as pd
import ntpath
from Constants import COLUMNS
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

# ---------------------------------------

CSV_RESULT_FILE_PATH = os.getenv("CSV_RESULT_FILE_PATH")

# ---------------------------------------

def nomFichierDuChemin(chemin):
    chemin, fichier = ntpath.split(chemin)
    return fichier or ntpath.basename(chemin)

# ---------------------------------------
# Choix de l'utilisateur
def confirmationUtilisateur(messageInput, confirmation):
    userInput = ""

    for index, choix in enumerate(confirmation):
        messageInput += f'{index+1}) {choix}\n'

    messageInput += '-> '

    while userInput not in confirmation:
        userInput = input(messageInput)

    print("")
    return userInput

# ---------------------
# Ajout dans le fichier CSV Résultat
def resultatCSV(resultMessage, dataSerializer):
    try:
        newLine = pd.DataFrame([[resultMessage, dataSerializer.emailEntreprise, dataSerializer.nomEntreprise, dataSerializer.adresseEntreprise, dataSerializer.telephoneEntreprise]], columns = COLUMNS)
        newLine.to_csv(CSV_RESULT_FILE_PATH, mode='a', header=False, index=False, sep=';')

    except Exception as e:
        MessagePrinter({
            "FR" : ("ERREUR : Une erreur durant l'enregistrement des résultats s'est produite : \n", e),
            "EN" : ("ERROR : An error occurred during the saving of the results.\n", e)
        })
        exit()

# ---------------------
# Raise une exception de la langue utilisée.
def ExceptionRaiser(errorMessage: dict):
    raise Exception(errorMessage[os.getenv("LANGUAGE")])

# ----------------------
# Affiche un message de la langue utilisée.
def MessagePrinter(message: dict):
    print(message[os.getenv("LANGUAGE")])