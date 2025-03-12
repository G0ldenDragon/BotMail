import os
import pandas as pd
from validate_email import validate_email
from Constants import COLUMNS
from dotenv import load_dotenv, set_key
load_dotenv(dotenv_path=".env")
# A RETENIR POUR LA CONFIGURATION DE LA LANGUE
# set_key(".env", "LANGUAGE", "EN")

from DataSerializer import DataSerializer
from DocumentModificator import documentModificator, documentConvertor
from UserInterface import confirmationUtilisateur, resultatCSV, nomFichierDuChemin, ExceptionRaiser, MessagePrinter
import EmailSender

# ---------------------------------------

# Chemin d'accès vers le fichier CSV
FILE_SHEET_PATH = os.getenv("FILE_SHEET_PATH")
FILE_SHEET_RESULT_PATH = os.getenv("FILE_SHEET_RESULT_PATH")

# ---------------------------------------

# Lecture CSV
if __name__ == '__main__':

    # Extraction et sérialisation des données
    dataSerializer = DataSerializer()

    try:
        # Créer ou demande l'écrasement du fichier CSV résultant
        if not(os.path.exists (FILE_SHEET_PATH)):
            # Créer le fichier de résultat avec les entêtes
            resultFile = pd.DataFrame(columns = COLUMNS)
            resultFile.to_csv(FILE_SHEET_RESULT_PATH, index=False, sep=';')

        else:
            userConfirm = {
                "FR" : {
                    "messageInput" : "Le fichier --" + nomFichierDuChemin(FILE_SHEET_RESULT_PATH) + "-- va être écrasé, voulez-vous continuer ?\n",
                    "confirmation" : ["Oui", "Non"]
                },
                "EN" : {
                    "messageInput" : "The following file --" + nomFichierDuChemin(FILE_SHEET_RESULT_PATH) + "-- will be overwritten, Do you want to continue ?\n",
                    "confirmation" : ["Yes", "No"]
                }
            }

            userInput = confirmationUtilisateur(userConfirm)

            if userInput == userConfirm[os.getenv("LANGUAGE")]["confirmation"][1]:
                MessagePrinter({
                    "FR" : "Arrêt...",
                    "EN" : "Shutting down..."
                })
                exit()

            if userInput == userConfirm[os.getenv("LANGUAGE")]["confirmation"][0]:
                resultFile = pd.DataFrame(columns = COLUMNS)
                resultFile.to_csv(FILE_SHEET_RESULT_PATH, index=False, sep=';')
    except PermissionError as e:
        ExceptionRaiser({
            "FR" : "Le fichier donné en argument est ouvert dans un autre programme, impossible de l'ouvrir.",
            "EN" : "The file provided as an argument is open in another program, it cannot be accessed."
        })

    userInput = ""
    userConfirm = {
        "FR" : {
            "messageInput" : "",
            "confirmation" : ["Oui", "Oui pour Tout", "Non", "Stop"]
        },
        "EN" : {
            "messageInput" : "",
            "confirmation" : ["Yes", "Yes for All", "No", "Stop"]
        }
    }
    try:
        # Lecture des données sérialisée pour traitement
        for i in range(0, dataSerializer.getLength()):

            # Définition du choix utilisateur
            if userInput != userConfirm[os.getenv("LANGUAGE")]["confirmation"][1]:
                userInput = ""

            # Définition de toutes les valeurs à partir de la ligne actuelle du fichier CSV.
            dataSerializer.setCurrentLine(i)

            # Vérification de l'existence et de la validité de l'email
            if validate_email(dataSerializer.recipientEmail):

                # Impression du destinataire à qui va être envoyé le mail.
                MessagePrinter({
                    "FR" : "Destinataire : ---" + dataSerializer.recipientName + "---",
                    "EN" : "Recipient : ---" + dataSerializer.recipientName + "---"
                })

                # -------------------------------------------
                # Modification Docx

                # Modification du Docx en fonction des noms des destinataires
                MessagePrinter({
                    "FR" : "Modification...",
                    "EN" : "Modification..."
                })
                documentModificator(dataSerializer)
                MessagePrinter({
                    "FR" : "Modifié !",
                    "EN" : "Modified !"
                })

                # -------------------------------------------
                # Création PDF

                # Conversion du Docx en PDF
                MessagePrinter({
                    "FR" : "Conversion en PDF...",
                    "EN" : "Converting to PDF..."
                })
                documentConvertor(dataSerializer)
                MessagePrinter({
                    "FR" : "Converti !",
                    "EN" : "Converted !"
                })

                # -------------------------------------------
                # Envoie des mails

                # Si le choix précédent est "Oui pour Tout", on ne pose pas la question
                if userInput != userConfirm[os.getenv("LANGUAGE")]["confirmation"][1]:

                    # Si un email a déjà été envoyé à ce destinataire
                    if dataSerializer.previousSend == "Envoyé !":
                        userConfirm = {
                            "FR" : {
                                "messageInput" : "Un mail à déjà été envoyé à --" + dataSerializer.recipientName + "--, voulez-vous en renvoyer un ? (N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n",
                                "confirmation" : ["Oui", "Oui pour Tout", "Non", "Stop"]
                            },
                            "EN" : {
                                "messageInput" : "A mail has already been sent to --" + nomFichierDuChemin(FILE_SHEET_RESULT_PATH) + "-- would you like to send another one ? (Don't forget to verify the PDF of the motivation letter generated.)\n",
                                "confirmation" : ["Yes", "Yes for All", "No", "Stop"]
                            }
                        }
                        userInput = confirmationUtilisateur(userConfirm)

                    else:
                        userConfirm = {
                            "FR" : {
                                "messageInput" : "\nVoulez-vous envoyer ce mail à --" + dataSerializer.recipientName + "-- ? (N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n",
                                "confirmation" : ["Oui", "Oui pour Tout", "Non", "Stop"]
                            },
                            "EN" : {
                                "messageInput" : "\nWould you like to send this mail to --" + dataSerializer.recipientName + "-- ? (Don't forget to verify the PDF of the motivation letter generated.)\n",
                                "confirmation" : ["Yes", "Yes for All", "No", "Stop"]
                            }
                        }
                        userInput = confirmationUtilisateur(userConfirm)

                # Si Stop : Arrêt du programme
                if userInput == userConfirm[os.getenv("LANGUAGE")]["confirmation"][3]:
                    MessagePrinter({
                        "FR" : "Arrêt...",
                        "EN" : "Shutting down..."
                    })
                    exit()

                # Si Non : Destinataire suivant
                if userInput == userConfirm[os.getenv("LANGUAGE")]["confirmation"][2]:
                    MessagePrinter({
                        "FR" : "Prochain destinataire...\n",
                        "EN" : "Next recipient...\n"
                    })

                # Si Oui : Envoie d'un mail
                if userInput == userConfirm[os.getenv("LANGUAGE")]["confirmation"][0] or userInput == userConfirm[os.getenv("LANGUAGE")]["confirmation"][1]:
                    EmailSender.send(dataSerializer)

            else:
                MessagePrinter({
                    "FR" : "ERREUR : L'email --" + dataSerializer.recipientEmail + "-- de --" + dataSerializer.recipientName + "-- n'est pas valide.\n",
                    "EN" : "ERROR : The following email --" + dataSerializer.recipientEmail + "-- of --" + dataSerializer.recipientName + "-- isn't valid.\n"
                })
                resultatCSV("! Email Invalide !", dataSerializer)

        MessagePrinter({
            "FR" : "Plus aucun destinataire, arrêt...",
            "EN" : "No more recipients, shut down..."
        })

    except FileNotFoundError as e:
        MessagePrinter({
            "FR" : "ERREUR : Le fichier CSV n'est pas trouvé à partir de ce chemin d'accès.",
            "EN" : "ERROR : The Sheet file isn't find with the path given."
        })

    except Exception as e:
        MessagePrinter({
            "FR" : "ERREUR : Le fichier CSV est bien trouvé mais rencontre un problème : \n" + str(e),
            "EN" : "ERROR : The Sheet file is found but has the following error : \n" + str(e)
        })