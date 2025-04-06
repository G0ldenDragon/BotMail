import os
from dotenv import load_dotenv, set_key

class EnvironmentVariable_Model:
    def __init__(self, env_file=".env"):
        """
        Initialise le gestionnaire d'environnement avec un fichier .env.
        """
        self.env_file = env_file
        load_dotenv(self.env_file)

    def get_variable(self, key):
        """
        Récupère la valeur d'une variable d'environnement.
        """
        return os.getenv(key)

    def set_variable(self, key, value):
        """
        Ajoute ou met à jour une variable dans le fichier .env.
        """
        set_key(self.env_file, key, value)
        print(f"Variable '{key}' définie avec succès.")

    def delete_variable(self, key):
        """
        Supprime une variable du fichier .env.
        """
        with open(self.env_file, "r") as file:
            lines = file.readlines()

        with open(self.env_file, "w") as file:
            for line in lines:
                if not line.startswith(f"{key}="):
                    file.write(line)
        print(f"Variable '{key}' supprimée avec succès.")

    def list_variables(self):
        """
        Liste toutes les variables d'environnement chargées.
        """
        for key, value in os.environ.items():
            print(f"{key}={value}")