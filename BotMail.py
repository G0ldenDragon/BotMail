# BotMail.py

import os
import pandas as pd
from validate_email import validate_email


from TerminalUtils import user_confirmation, file_name
from DataSerializer import DataSerializer
from DocumentModificator import document_modificator, document_convertor
from EmailSender import *
from Models.EnvironmentVariable_Model import load_env, get_variable
load_env()
from Models.Language_Model import Language


from Constants import COLUMNS
# Chemin d'accès vers le fichier CSV
FILE_SHEET_PATH = get_variable("FILE_SHEET_PATH")
FILE_SHEET_RESULT_PATH = get_variable("FILE_SHEET_RESULT_PATH")
SCRIPT_NAME = "terminal_botmail"


if __name__ == '__main__':
    # Extraction et sérialisation des données
    data_serializer = DataSerializer()
    language_Model = Language()

    try:
        # Créer ou demande l'écrasement du fichier CSV résultant
        if not(os.path.exists(FILE_SHEET_RESULT_PATH)):
            # Créer le fichier de résultat avec les entêtes
            resultFile = pd.DataFrame(columns = COLUMNS)
            resultFile.to_csv(FILE_SHEET_RESULT_PATH, index=False, sep=';')

        else:
            userInput = user_confirmation(
                language_Model.get_translation(SCRIPT_NAME, "message_input_overwrite").replace(";;;", file_name(FILE_SHEET_RESULT_PATH)),
                language_Model.get_translation(SCRIPT_NAME, "confirmation_overwrite")
            )

            if userInput == 1:
                print(language_Model.get_translation(SCRIPT_NAME, "shut_down"))
                exit()

            if userInput == 0:
                resultFile = pd.DataFrame(columns = COLUMNS)
                resultFile.to_csv(FILE_SHEET_RESULT_PATH, index=False, sep=';')
    except PermissionError as e:
        raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_csv_opening"))

    userInput = ""

    try:
        # Lecture des données sérialisée pour traitement
        for i in range(0, data_serializer.get_length()):

            # Définition du choix utilisateur
            if userInput != 1:
                userInput = ""

            # Définition de toutes les valeurs à partir de la ligne actuelle du fichier CSV.
            data_serializer.set_current_line(i)

            # Vérification de l'existence et de la validité de l'email
            if validate_email(data_serializer.recipientEmail):

                # Impression du destinataire à qui va être envoyé le mail.
                print(language_Model.get_translation(SCRIPT_NAME, "recipient_name").replace(";;;", data_serializer.recipientName))

                # -------------------------------------------
                # Modification Docx

                # Modification du Docx en fonction des noms des destinataires
                print(language_Model.get_translation(SCRIPT_NAME, "modification"))
                
                document_modificator(data_serializer)
                print(language_Model.get_translation(SCRIPT_NAME, "modified"))

                # -------------------------------------------
                # Création PDF

                # Conversion du Docx en PDF
                print(language_Model.get_translation(SCRIPT_NAME, "conversion"))
                document_convertor(data_serializer)
                print(language_Model.get_translation(SCRIPT_NAME, "converted"))

                # -------------------------------------------
                # Envoie des mails

                # Si le choix précédent est "Oui pour Tout", on ne pose pas la question
                if userInput != 1:

                    # Si un email a déjà été envoyé à ce destinataire
                    if data_serializer.previousSend == language_Model.get_translation("email_sender", "email_sent"):
                        userInput = user_confirmation(
                            language_Model.get_translation(SCRIPT_NAME, "message_input_already_sent").replace(";;;", file_name(FILE_SHEET_RESULT_PATH)),
                            language_Model.get_translation(SCRIPT_NAME, "confirmation_already_sent")
                        )

                    else:
                        userInput = user_confirmation(
                            language_Model.get_translation(SCRIPT_NAME, "message_input_send_confirmation").replace(";;;", data_serializer.recipientName),
                            language_Model.get_translation(SCRIPT_NAME, "confirmation_send_confirmation")
                        )

                # Si Stop : Arrêt du programme
                if userInput == 3:
                    print(language_Model.get_translation(SCRIPT_NAME, "shut_down"))
                    exit()

                # Si Non : Destinataire suivant
                if userInput == 2:
                    print(language_Model.get_translation(SCRIPT_NAME, "next_recipient"))

                # Si Oui : Envoie d'un mail
                if userInput == 0 or userInput == 1:
                    send(data_serializer)

            else:
                data_serializer.csv_result(language_Model.get_translation(SCRIPT_NAME, "result_invalid_email"))
                raise Exception(language_Model.get_translation(
                    SCRIPT_NAME, "exception_invalid_email"
                    ).replace(
                        ";;;", data_serializer.recipientEmail
                    ).replace(
                        "///", data_serializer.recipientName
                    )
                )

        print(language_Model.get_translation(SCRIPT_NAME, "script_end"))

    except FileNotFoundError as e:
        raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_csv_path").replace(";;;", data_serializer.fileExtension))

    except Exception as e:
        raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_csv_general").replace(";;;", data_serializer.fileExtension) + str(e))
