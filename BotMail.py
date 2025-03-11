import os
from csv import DictReader, DictWriter, writer as csv_writer

import pandas as pd
from validate_email import validate_email
from dotenv import load_dotenv, set_key
load_dotenv(dotenv_path=".env")
# A RETENIR POUR LA CONFIGURATION DE LA LANGUE
# set_key(".env", "LANGUAGE", "EN")

from DataSerializer import DataSerializer
from DocumentModificator import documentModificator, documentConvertor
from UserInterface import confirmationUtilisateur, resultatCSV, nomFichierDuChemin, ExceptionRaiser
import EmailSender

# ---------------------------------------

# Chemin d'accès vers le fichier CSV
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
CSV_RESULT_FILE_PATH = os.getenv("CSV_RESULT_FILE_PATH")

# ---------------------------------------

# Lecture CSV
if __name__ == '__main__':

    # Extraction et sérialisation des données
    dataSerializer = DataSerializer()

    try:
        # Créer ou demande l'écrasement du fichier CSV résultant
        if not(os.path.exists (CSV_FILE_PATH)):
            # Créer le fichier de résultat avec les entêtes
            resultFile = pd.DataFrame(columns=['XXP', 'XXE', 'XXN', 'XXA', 'XXT'])
            resultFile.to_csv(CSV_RESULT_FILE_PATH, index=False, sep=';')

        else:
            userInput = confirmationUtilisateur(
                "Le fichier --" + nomFichierDuChemin(CSV_RESULT_FILE_PATH) + "-- va être écrasé, voulez-vous continuer ?\n",
                ["Oui", "Non"]
            )

            if userInput == "Non":
                print("Arrêt...")
                exit()

            if userInput == "Oui":
                resultFile = pd.DataFrame(columns=['XXP', 'XXE', 'XXN', 'XXA', 'XXT'])
                resultFile.to_csv(CSV_RESULT_FILE_PATH, index=False, sep=';')
    except PermissionError as e:
        ExceptionRaiser({
            "FR" : "Le fichier donné en argument est ouvert dans un autre programme, impossible de l'ouvrir.",
            "EN" : "The file provided as an argument is open in another program, it cannot be accessed."
        })

    userInput = ""
    try:
        # Lecture des données sérialisée pour traitement
        for i in range(0, dataSerializer.getLength()):

            # Définition du choix utilisateur
            if userInput != "Oui pour Tout":
                userInput = ""

            # Définition de toutes les valeurs à partir de la ligne actuelle du fichier CSV.
            dataSerializer.setCurrentLine(i)

            # Vérification de l'existence et de la validité de l'email
            if validate_email(dataSerializer.emailEntreprise):

                # Impression de l'entreprise à qui va être envoyé le mail.
                print("Destinataire : ---" + dataSerializer.nomEntreprise + "---")

                # -------------------------------------------
                # Modification Docx

                # Modification du Docx en fonction des noms des entreprises
                print("Modification...")
                documentModificator(dataSerializer)
                print("Modifié !")

                # -------------------------------------------
                # Création PDF

                # Conversion du Docx en PDF
                print("Conversion en PDF...")
                documentConvertor(dataSerializer)
                print("Converti !")

                # -------------------------------------------
                # Envoie des mails

                # Si le choix précédent est "Oui pour Tout", on ne pose pas la question
                if userInput != "Oui pour Tout":

                    # Si un email a déjà été envoyé à ce destinataire
                    if dataSerializer.envoiePrecedent == "Envoyé !":
                        userInput = confirmationUtilisateur(
                            "Un mail à déjà été envoyé à --" + dataSerializer.nomEntreprise + "--, voulez-vous en renvoyer un ? (N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n",
                            ["Oui", "Oui pour Tout", "Non", "Stop"]
                        )

                    else:
                        userInput = confirmationUtilisateur(
                            "\nVoulez-vous envoyer ce mail à --" + dataSerializer.nomEntreprise + "-- ? (N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n",
                            ["Oui", "Oui pour Tout", "Non", "Stop"]
                        )

                # Si Stop : Arrêt du programme
                if userInput == "Stop":
                    print("Arrêt...")
                    exit()

                # Si Non : Entreprise suivante
                if userInput == "Non":
                    print("Entreprise suivante...\n")

                # Si Oui : Envoie d'un mail
                if userInput == "Oui" or userInput == "Oui pour Tout":
                    EmailSender.send(dataSerializer)

            else:
                print("ERREUR : L'email --" + dataSerializer.emailEntreprise + "-- de --" + dataSerializer.nomEntreprise + "-- n'est pas valide.\n")
                resultatCSV("! Email Invalide !", dataSerializer)

        print("Plus aucun destinataire, arrêt...")

    except FileNotFoundError as e:
        print("ERREUR : Le fichier CSV n'est pas trouvé à partir de ce chemin d'accès.")

    except Exception as e:
        print("ERREUR : Le fichier CSV est bien trouvé mais rencontre un problème : \n", e)