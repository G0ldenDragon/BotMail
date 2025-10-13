# BotMail.py

import os
import pandas as pd
from validate_email import validate_email


from DataSerializer import DataSerializer
from DocumentModificator import document_modificator, document_convertor
from Utilities import user_confirmation, csv_result, file_name, exception_raiser, message_printer
import EmailSender
from Models.EnvironmentVariable_Model import load_env, get_variable, set_variable
load_env()
from Models.Language_Model import Language


from Constants import COLUMNS
# Chemin d'accès vers le fichier CSV
FILE_SHEET_PATH = get_variable("FILE_SHEET_PATH")
FILE_SHEET_RESULT_PATH = get_variable("FILE_SHEET_RESULT_PATH")
TERMINAL_BOTMAIL = "terminal_botmail"


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
                language_Model.get_translation(TERMINAL_BOTMAIL, "message_input_overwrite").replace(";;;", file_name(FILE_SHEET_RESULT_PATH)),
                language_Model.get_translation(TERMINAL_BOTMAIL, "confirmation_overwrite")
            )

            if userInput == 1:
                message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "shut_down"))
                exit()

            if userInput == 0:
                resultFile = pd.DataFrame(columns = COLUMNS)
                resultFile.to_csv(FILE_SHEET_RESULT_PATH, index=False, sep=';')
    except PermissionError as e:
        exception_raiser(language_Model.get_translation(TERMINAL_BOTMAIL, "exception_csv_opening"))

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
                message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "recipient_name").replace(";;;", data_serializer.recipientName))

                # -------------------------------------------
                # Modification Docx

                # Modification du Docx en fonction des noms des destinataires
                message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "modification"))
                
                document_modificator(data_serializer)
                message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "modified"))

                # -------------------------------------------
                # Création PDF

                # Conversion du Docx en PDF
                message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "conversion"))
                document_convertor(data_serializer)
                message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "converted"))

                # -------------------------------------------
                # Envoie des mails

                # Si le choix précédent est "Oui pour Tout", on ne pose pas la question
                if userInput != 1:

                    # Si un email a déjà été envoyé à ce destinataire
                    if data_serializer.previousSend == "Envoyé !":
                        userInput = user_confirmation(
                            language_Model.get_translation(TERMINAL_BOTMAIL, "message_input_already_sent").replace(";;;", file_name(FILE_SHEET_RESULT_PATH)),
                            language_Model.get_translation(TERMINAL_BOTMAIL, "confirmation_already_sent")
                        )

                    else:
                        userInput = user_confirmation(
                            language_Model.get_translation(TERMINAL_BOTMAIL, "message_input_send_confirmation").replace(";;;", data_serializer.recipientName),
                            language_Model.get_translation(TERMINAL_BOTMAIL, "confirmation_send_confirmation")
                        )

                # Si Stop : Arrêt du programme
                if userInput == 3:
                    message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "shut_down"))
                    exit()

                # Si Non : Destinataire suivant
                if userInput == 2:
                    message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "next_recipient"))

                # Si Oui : Envoie d'un mail
                if userInput == 0 or userInput == 1:
                    EmailSender.send(data_serializer)

            else:
                csv_result("! Email Invalide !", data_serializer)
                exception_raiser(language_Model.get_translation(
                    TERMINAL_BOTMAIL, "exception_invalid_email"
                    ).replace(
                        ";;;", data_serializer.recipientEmail
                    ).replace(
                        "///", data_serializer.recipientName
                    )
                )

        message_printer(language_Model.get_translation(TERMINAL_BOTMAIL, "script_end"))

    except FileNotFoundError as e:
        exception_raiser(language_Model.get_translation(TERMINAL_BOTMAIL, "exception_csv_path").replace(";;;", data_serializer.fileExtension))

    except Exception as e:
        exception_raiser(language_Model.get_translation(TERMINAL_BOTMAIL, "exception_csv_general").replace(";;;", data_serializer.fileExtension) + str(e))
