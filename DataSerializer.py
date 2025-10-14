# DataSerializer.py

import os
from pathlib import Path
import pandas as pd


from TerminalUtils import file_name
from Models.EnvironmentVariable_Model import load_env, get_variable
load_env()
from Models.Language_Model import Language


from Constants import CORRECT_SHEET_FILE_EXTENSIONS, COLUMNS
FILE_SHEET_RESULT_PATH = get_variable("FILE_SHEET_RESULT_PATH")
SCRIPT_NAME = "data_serializer"


class DataSerializer():
    def __init__(self, csvFilePath = get_variable("FILE_SHEET_PATH")):
        language_Model = Language()
        
        # Vérification du fichier, s'il est vide, il ne sert à rien de continuer.
        if os.stat(csvFilePath).st_size == 0:
            raise Exception(language_Model.get_translation(SCRIPT_NAME, "data_serializer"))

        # Obtention de l'extension
        self.fileExtension = Path(file_name(csvFilePath)).suffix
        print(self.fileExtension)

        try :
            # Si l'extension du fichier est CSV, alors traitement particulier
            if self.fileExtension == '.csv':
                self.data = pd.read_csv(csvFilePath, sep=';', header=0)
            else:
                self.ata = pd.read_excel(csvFilePath, header=0)

        except pd._config.config.OptionError or ValueError as e:
            raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_csv_wrong_format"))
        except ImportError as e:
            raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_csv_wrong_extension") + str(CORRECT_SHEET_FILE_EXTENSIONS).replace("[", "").replace("]", ""))
        except Exception as e:
            raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_csv_general"))

        self.previousSend = ""
        self.recipientEmail = ""
        self.recipientName = ""
        self.recipientAddress = ""
        self.recipientPhone = ""

    # -------------------------
    def get_length(self):
        return self.data.shape[0]

    # -------------------------

    def get_serialized__data(self):
        return self.data

    # -------------------------
    def get_line(self, number):
        return self.data.loc[number]

    # -------------------------
    def set_current_line(self, number):
        if pd.notnull(self.data.loc[number, 'XXP']):
            self.previousSend = self.data.loc[number, 'XXP']

        self.recipientEmail = self.data.loc[number, 'XXE'].lower().rstrip()

        if pd.notnull(self.data.loc[number, 'XXN']):
            self.recipientName = self.data.loc[number, 'XXN'].rstrip()

        if pd.notnull(self.data.loc[number, 'XXA']):
            self.recipientAddress = self.data.loc[number, 'XXA'].rstrip()

        if pd.notnull(self.data.loc[number, 'XXT']):
            self.recipientPhone = self.data.loc[number, 'XXT']


    # Ajout dans le fichier CSV Résultat
    def csv_result(self, resultMessage):
        language_Model = Language()

        try:
            newLine = pd.DataFrame([[resultMessage, self.recipientEmail, self.recipientName, self.recipientAddress, self.recipientPhone]], columns = COLUMNS)
            newLine.to_csv(FILE_SHEET_RESULT_PATH, mode='a', header=False, index=False, sep=';')

        except PermissionError as e:
            if resultMessage == language_Model.get_translation("email_sender", "email_sent"):
                raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_script_finished_but_sheet_opened").replace(";;;", self.recipientEmail))

            else:
                raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_sheet_opened"))

        except Exception as e:
            raise Exception(language_Model.get_translation(SCRIPT_NAME, "exception_sheet_general") + str(e))
