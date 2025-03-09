import os
from docx import Document
import locale
import time
import subprocess
from dotenv import load_dotenv
load_dotenv()

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

class DocumentModificator:
    def __init__(self, ligne):
        self.ligne = ligne
        self.envoiePrecedent = ligne.get("envoiePrecedent")
        self.nomEntreprise = ligne.get("nomEntreprise").rstrip()
        self.emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
        self.adresseEntreprise = ligne.get("adresseEntreprise")
        self.telephoneEntreprise = ligne.get("telephoneEntreprise")


    def documentModificator(self):
        try:
            motivationLetter = Document(MOTIVATION_LETTER_PATH)
            for paragraph in motivationLetter.paragraphs:
                # Remplacement du Nom de l'entreprise
                if "XXN" in paragraph.text and self.nomEntreprise != "":
                    paragraph.text = paragraph.text.replace("XXN", self.nomEntreprise)

                # Remplacement de l'Email de l'entreprise
                if "XXE" in paragraph.text and self.emailEntreprise != "":
                    paragraph.text = paragraph.text.replace("XXE", self.emailEntreprise)

                # Remplacement de l'Adresse de l'entreprise
                if "XXA" in paragraph.text and self.adresseEntreprise != "":
                    paragraph.text = paragraph.text.replace("XXA", self.adresseEntreprise)

                # Remplacement du numéro de Téléphone de l'entreprise
                if "XXT" in paragraph.text and self.telephoneEntreprise != "":
                    paragraph.text = paragraph.text.replace("XXT", self.telephoneEntreprise)

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
            resultatCSV("! Modification Lettre de Motivation !", self.ligne)
            exit()


    def documentConvertor(self):
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
            resultatCSV("! Conversion en PDF !", self.ligne)
            exit()