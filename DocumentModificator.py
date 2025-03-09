import os
from docx import Document
import locale
import time
import subprocess
from dotenv import load_dotenv
load_dotenv()

from UserInterface import resultatCSV

# Chemin vers le dossier où est stockée la plupart des fichiers
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")

# !!!!!!! Le nom de l'entreprise doit être remplacée par "XXN" !!!!!!!!!!!!!
# !!!!!!! L'adresse de l'entreprise doit être remplacée par "XXA" !!!!!!!!!!!!!
# !!!!!!! Le numéro de téléphone de l'entreprise doit être remplacée par "XXT" !!!!!!!!!!!!!
LETTRE_MOTIVATION = DOCUMENTS_PATH + os.getenv("LETTRE_MOTIVATION")
LETTRE_MOTIVATION_FINALE = DOCUMENTS_PATH + os.getenv("LETTRE_MOTIVATION_FINALE")
LETTRE_MOTIVATION_PDF = DOCUMENTS_PATH + os.getenv("LETTRE_MOTIVATION_PDF")
LIBRE_OFFICE_PATH = os.getenv("LIBRE_OFFICE_PATH")


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
            motivationLetter = Document(LETTRE_MOTIVATION)
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

            motivationLetter.save(LETTRE_MOTIVATION_FINALE)

        except Exception as e:
            print("ERREUR : Une erreur durant la modification du document " + LETTRE_MOTIVATION + " s'est produite : \n", e)
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
                    LETTRE_MOTIVATION_FINALE,
                    "--outdir",
                    os.path.dirname(LETTRE_MOTIVATION_PDF)
                ])

        except Exception as e:
            print("ERREUR : Une erreur durant la conversion du document " + LETTRE_MOTIVATION_FINALE + " s'est produite : \n", e)
            resultatCSV("! Conversion en PDF !", self.ligne)
            exit()