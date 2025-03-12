import os
from docx import Document
import locale
import time
import subprocess
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

from UserInterface import resultatCSV, MessagePrinter

# ---------------------------------------

# !!!!!!! Le nom du destinataire doit être remplacée par "XXN" !!!!!!!!!!!!!
# !!!!!!! L'adresse du destinataire doit être remplacée par "XXA" !!!!!!!!!!!!!
# !!!!!!! Le numéro de téléphone du destinataire doit être remplacée par "XXT" !!!!!!!!!!!!!
MOTIVATION_LETTER_PATH = os.getenv("MOTIVATION_LETTER_PATH")
MOTIVATION_LETTER_PATH_FINAL = os.getenv("MOTIVATION_LETTER_PATH_FINAL")
MOTIVATION_LETTER_PATH_PDF = os.getenv("MOTIVATION_LETTER_PATH_PDF")
LIBRE_OFFICE_PATH = os.getenv("LIBRE_OFFICE_PATH")

# ---------------------------------------

# Modificateur du document
def documentModificator(dataSerializer):
    try:
        motivationLetter = Document(MOTIVATION_LETTER_PATH)

        for paragraph in motivationLetter.paragraphs:
            # Remplacement de l'Email du destinataire
            if "XXE" in paragraph.text and dataSerializer.recipientEmail != "":
                paragraph.text = paragraph.text.replace("XXE", dataSerializer.recipientEmail)

            # Remplacement du Nom du destinataire
            if "XXN" in paragraph.text and dataSerializer.recipientName != "":
                paragraph.text = paragraph.text.replace("XXN", dataSerializer.recipientName)

            # Remplacement de l'Adresse du destinataire
            if "XXA" in paragraph.text and dataSerializer.recipientAddress != "":
                paragraph.text = paragraph.text.replace("XXA", dataSerializer.recipientAddress)

            # Remplacement du numéro de Téléphone du destinataire
            if "XXT" in paragraph.text and dataSerializer.recipientPhone != "":
                paragraph.text = paragraph.text.replace("XXT", dataSerializer.recipientPhone)

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
        MessagePrinter({
            "FR" : "ERREUR : Une erreur durant la modification du document " + MOTIVATION_LETTER_PATH + " s'est produite : \n" + str(e),
            "EN" : "ERROR : An error occurred during the modification of the following document : " + MOTIVATION_LETTER_PATH + "\n" + str(e)
        })
        resultatCSV("! Modification Lettre de Motivation !", dataSerializer)
        exit()


def documentConvertor(dataSerializer):
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
        MessagePrinter({
            "FR" : "ERREUR : Une erreur durant la conversion du document " + MOTIVATION_LETTER_PATH_FINAL + " s'est produite : \n" + str(e),
            "EN" : "ERROR : An error occurred during the conversion of the following document : " + MOTIVATION_LETTER_PATH_FINAL + "\n" + str(e)
        })
        resultatCSV("! Conversion en PDF !", dataSerializer)
        exit()