import os
from dotenv import load_dotenv, set_key

class EnvironmentVariable_Model:
    def __init__(self, env_file=".env"):
        self.env_file = env_file
        load_dotenv(self.env_file)


    # Récupération de la valeur d'une variable d'environnement
    def getVariable(self, key):
        return os.getenv(key)


    # Met à jour une variable d'environnement
    def setVariable(self, key, value):
        set_key(self.env_file, key, value)
        print(f"Variable '{key}' définie avec succès.")


    # Supprime une variable d'environnement
    def deleteVariable(self, key):
        with open(self.env_file, "r") as file:
            lines = file.readlines()

        with open(self.env_file, "w") as file:
            for line in lines:
                if not line.startswith(f"{key}="):
                    file.write(line)
        print(f"Variable '{key}' supprimée avec succès.")


    # Liste toutes les variables d'environnement
    def listVariables(self):
        for key, value in os.environ.items():
            print(f"{key}={value}")