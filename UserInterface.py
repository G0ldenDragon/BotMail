import os
import pandas as pd
import ntpath
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
def resultatCSV(resultat, dataSerializer):
    try:
        newLine = pd.DataFrame([[resultat, dataSerializer.emailEntreprise, dataSerializer.nomEntreprise, dataSerializer.adresseEntreprise, dataSerializer.telephoneEntreprise]], columns=['XXP', 'XXE', 'XXN', 'XXA', 'XXT'])
        newLine.to_csv(CSV_RESULT_FILE_PATH, mode='a', header=False, index=False, sep=';')

    except Exception as e:
        print("ERREUR : Une erreur durant l'enregistrement des résultats s'est produite : \n", e)
        exit()

# ---------------------
# Raise une exception de la langue utilisée.
def ExceptionRaiser(errorMessage: dict):
    raise Exception(errorMessage[os.getenv("LANGUAGE")])