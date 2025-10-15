# Models/EnvironmentVariable.py

import os
from dotenv import load_dotenv, set_key


ENV_FILE = ".env"


def load_env(env_file: str= ENV_FILE) -> None:
    """
    Charges les variables d'environnements en mémoire.

    Args:
        env_file (str): Chemin d'accès vers le fichier .env.
    """
    load_dotenv(env_file, override=True)


def get_variable(key: str) -> str:
    """
    Récupère une donnée d'une variable d'environnement.

    Args:
        key (str): Nom de la variable d'environnement.

    Returns:
        str: Valeur contenue dans la variable.
    """
    return os.getenv(key)


def set_variable(key: str, value: str, env_file: str= ENV_FILE) -> None:
    """
    Met à jour une variable d'environnement.

    Args:
        key (str): Nom de la variable d'environnement.
        value (str): Nouvelle valeur de la variable d'environnement.
        env_file (str): Chemin d'accès vers le fichier .env.
    """
    set_key(env_file, key, value)
    load_env()
    # print(f"Variable '{key}' définie avec succès : \n-> {value}")


def delete_variable(key: str, env_file: str= ENV_FILE) -> None:
    """
    Supprime une variable d'environnement.

    Args:
        key (str): Nom de la variable d'environnement à supprimer.
        env_file (str): Chemin d'accès vers le fichier .env.
    """
    with open(env_file, "r") as file:
        lines = file.readlines()
    with open(env_file, "w") as file:
        for line in lines:
            if not line.startswith(f"{key}="):
                file.write(line)
    load_env()

    # if not get_variable(key):
    #     print(f"Variable '{key}' supprimée avec succès.")


def list_variables() -> dict:
    """
    Liste l'ensemble des variable d'environnement avec leurs valeurs.

    Returns:
        dict: Dictionnaire avec : clé = nom de la variable ; value = donnée.
    """
    # for key, value in os.environ.items():
    #     print(f"{key}={value}")

    return os.environ.items()
