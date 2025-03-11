import os
from docx import Document
import locale
import time
import subprocess
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

from UserInterface import resultatCSV

# ---------------------------------------

# !!!!!!! Le nom de l'entreprise doit être remplacée par "XXN" !!!!!!!!!!!!!
# !!!!!!! L'adresse de l'entreprise doit être remplacée par "XXA" !!!!!!!!!!!!!
# !!!!!!! Le numéro de téléphone de l'entreprise doit être remplacée par "XXT" !!!!!!!!!!!!!
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
            # Remplacement de l'Email de l'entreprise
            if "XXE" in paragraph.text and dataSerializer.emailEntreprise != "":
                paragraph.text = paragraph.text.replace("XXE", dataSerializer.emailEntreprise)

            # Remplacement du Nom de l'entreprise
            if "XXN" in paragraph.text and dataSerializer.nomEntreprise != "":
                paragraph.text = paragraph.text.replace("XXN", dataSerializer.nomEntreprise)

            # Remplacement de l'Adresse de l'entreprise
            if "XXA" in paragraph.text and dataSerializer.adresseEntreprise != "":
                paragraph.text = paragraph.text.replace("XXA", dataSerializer.adresseEntreprise)

            # Remplacement du numéro de Téléphone de l'entreprise
            if "XXT" in paragraph.text and dataSerializer.telephoneEntreprise != "":
                paragraph.text = paragraph.text.replace("XXT", dataSerializer.telephoneEntreprise)

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
        print("ERREUR : Une erreur durant la modification du document " + MOTIVATION_LETTER_PATH + " s'est produite : \n", e)
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
        print("ERREUR : Une erreur durant la conversion du document " + MOTIVATION_LETTER_PATH_FINAL + " s'est produite : \n", e)
        resultatCSV("! Conversion en PDF !", dataSerializer)
        exit()