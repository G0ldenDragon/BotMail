# DocumentModificator.py

import os
from docx import Document
import locale
import time
import subprocess


from Utilities import csv_result, message_printer, exception_raiser
from Models.EnvironmentVariable_Model import load_env, get_variable, set_variable
load_env()
from Models.Language_Model import Language


# !!!!!!! Le nom du destinataire doit être remplacée par "XXN" !!!!!!!!!!!!!
# !!!!!!! L'adresse du destinataire doit être remplacée par "XXA" !!!!!!!!!!!!!
# !!!!!!! Le numéro de téléphone du destinataire doit être remplacée par "XXT" !!!!!!!!!!!!!
MOTIVATION_LETTER_PATH = get_variable("MOTIVATION_LETTER_PATH")
MOTIVATION_LETTER_PATH_FINAL = get_variable("MOTIVATION_LETTER_PATH_FINAL")
MOTIVATION_LETTER_PATH_PDF = get_variable("MOTIVATION_LETTER_PATH_PDF")
LIBRE_OFFICE_PATH = get_variable("LIBRE_OFFICE_PATH")
DOCUMENT_MODIFICATOR = "document_modificator"


# Modificateur du document
def document_modificator(data_serializer):
    try:
        motivationLetter = Document(MOTIVATION_LETTER_PATH)

        for paragraph in motivationLetter.paragraphs:
            # Remplacement de l'Email du destinataire
            if "XXE" in paragraph.text and data_serializer.recipientEmail != "":
                paragraph.text = paragraph.text.replace("XXE", data_serializer.recipientEmail)

            # Remplacement du Nom du destinataire
            if "XXN" in paragraph.text and data_serializer.recipientName != "":
                paragraph.text = paragraph.text.replace("XXN", data_serializer.recipientName)

            # Remplacement de l'Adresse du destinataire
            if "XXA" in paragraph.text and data_serializer.recipientAddress != "":
                paragraph.text = paragraph.text.replace("XXA", data_serializer.recipientAddress)

            # Remplacement du numéro de Téléphone du destinataire
            if "XXT" in paragraph.text and data_serializer.recipientPhone != "":
                paragraph.text = paragraph.text.replace("XXT", data_serializer.recipientPhone)

            # Remplacement de la Date
            if "XXD" in paragraph.text:
                # Problème de thread-safe.
                locale.setlocale(locale.LC_ALL, '')
                # Obtention de la traduction de la date dans la langue actuelle de l'ordinateur.
                currentDate = time.localtime()
                # Traduction de la date
                translatedCurrentDate = time.strftime("%d %B %Y", currentDate)
                paragraph.text = paragraph.text.replace("XXD", translatedCurrentDate.title())

        motivationLetter.save(MOTIVATION_LETTER_PATH_FINAL)

    except Exception as e:
        language_Model = Language()
        csv_result("! Modification Lettre de Motivation !", data_serializer)
        exception_raiser(language_Model.get_translation(DOCUMENT_MODIFICATOR, "exception_document_modification_general").replace(";;;", MOTIVATION_LETTER_PATH) + str(e))


def document_convertor(data_serializer):
    try:
        subprocess.run(
            [
                LIBRE_OFFICE_PATH,
                "--headless",
                "--convert-to",
                "pdf",
                MOTIVATION_LETTER_PATH_FINAL,
                "--outdir",
                os.path.dirname(MOTIVATION_LETTER_PATH_PDF)
            ])

    except Exception as e:
        language_Model = Language()
        csv_result("! Conversion en PDF !", data_serializer)
        exception_raiser(language_Model.get_translation(DOCUMENT_MODIFICATOR, "exception_document_conversion_general").replace(";;;", MOTIVATION_LETTER_PATH_FINAL) + str(e))
