import os
import pandas as pd
from dotenv import load_dotenv

from Constants import CORRECT_EXTENSIONS

load_dotenv(dotenv_path=".env")

from UserInterface import nomFichierDuChemin, ExceptionRaiser


# -------------------------

class DataSerializer:
    def __init__(self, csvFilePath = os.getenv("CSV_FILE_PATH")):
        # Vérification du fichier, s'il est vide, il ne sert à rien de continuer.
        if os.stat(csvFilePath).st_size == 0:
            ExceptionRaiser({
                "FR" : "Le fichier donné est vide.",
                "EN" : "The file given in argument is empty."
            })

        # Obtention de l'extension
        self.fileExtension = os.path.splitext(nomFichierDuChemin(csvFilePath))[1]

        try :
            # Si l'extension du fichier est CSV, alors traitement particulier
            if self.fileExtension == '.csv':
                self.data = pd.read_csv(csvFilePath, sep=';', header=0)
            else:
                self.ata = pd.read_excel(csvFilePath, header=0)

        except pd._config.config.OptionError or ValueError as e:
            ExceptionRaiser({
                "FR" : "Le fichier donné en argument n'est pas un fichier de type Excel.",
                "EN" : "The file given in argument is not an Excel file."
            })
        except ImportError as e:
            ExceptionRaiser({
                "FR" : "L'extension du fichier donné en argument n'est pas la bonne. Voici les extensions valables : " + str(CORRECT_EXTENSIONS).replace("[", "").replace("]", ""),
                "EN" : "The file extension given in argument is wrong. Here is the available extensions: " + str(CORRECT_EXTENSIONS).replace("[", "").replace("]", "")
            })
        except Exception as e:
            ExceptionRaiser({
                "FR" : "Le fichier donné en argument ne réussi pas à être ouvert. Veuillez vérifier l'état du fichier.",
                "EN" : "The file given in argument is not an Excel file. Please check the status of the file."
            })

        self.envoiePrecedent = ""
        self.emailEntreprise = ""
        self.nomEntreprise = ""
        self.adresseEntreprise = ""
        self.telephoneEntreprise = ""

    # -------------------------
    def getLength(self):
        return self.data.shape[0]

    # -------------------------

    def getSerializedData(self):
        return self.data

    # -------------------------
    def getLine (self, number):
        return self.data.loc[number]

    # -------------------------
    def setCurrentLine(self, number):
        if pd.notnull (self.data.loc[number, 'XXP']):
            self.envoiePrecedent = self.data.loc[number, 'XXP']

        self.emailEntreprise = self.data.loc[number, 'XXE'].lower().rstrip()

        if pd.notnull (self.data.loc[number, 'XXN']):
            self.nomEntreprise = self.data.loc[number, 'XXN'].rstrip()

        if pd.notnull (self.data.loc[number, 'XXA']):
            self.adresseEntreprise = self.data.loc[number, 'XXA'].rstrip()

        if pd.notnull (self.data.loc[number, 'XXT']):
            self.telephoneEntreprise = self.data.loc[number, 'XXT']