import os
from csv import DictReader, DictWriter, writer as csv_writer
from dotenv import load_dotenv
load_dotenv()

import Constants

# ---------------------------------------

# Chemin vers le dossier où est stockée la plupart des fichiers
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")

CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")

# ---------------------------------------

# Choix de l'utilisateur
def confirmationUtilisateur(messageChoix, confirmation):
    choixUtilisateur = ""

    for index, choix in enumerate(confirmation):
        messageChoix += f'{index+1}) {choix}\n'

    messageChoix += '-> '

    while choixUtilisateur not in confirmation:
        choixUtilisateur = input(messageChoix)

    print("")
    return choixUtilisateur

# ---------------------
# Ajout dans le fichier CSV Résultat

def resultatCSV(resultat, ligne):
    try:
        nomEntreprise = ligne.get("nomEntreprise").rstrip()
        emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
        adresseEntreprise = ligne.get("adresseEntreprise")
        telephoneEntreprise = ligne.get("telephoneEntreprise")

        with open(DOCUMENTS_PATH + "Résultats - " + CSV_FILE_PATH, 'a', encoding='utf-8') as CSV_file:
            writer = DictWriter(CSV_file, fieldnames=Constants.NOM_COLONNE)

            writer.writerow({
                "envoiePrecedent": resultat,
                "nomEntreprise" : nomEntreprise,
                "emailEntreprise" : emailEntreprise,
                "adresseEntreprise" : adresseEntreprise,
                "telephoneEntreprise" : telephoneEntreprise
            })

    except Exception as e:
        print("ERREUR : Une erreur durant l'enregistrement du résultat s'est produite : \n", e)
        exit()