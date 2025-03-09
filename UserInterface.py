import os
from csv import DictReader, DictWriter, writer as csv_writer
from dotenv import load_dotenv
load_dotenv()


# Chemin vers le dossier où est stockée la plupart des fichiers
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")
FICHIER_CSV = os.getenv("FICHIER_CSV")


# Choix de l'utilisateur
def confirmationUtilisateur(messageChoix):
    messageChoix += "(N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n"
    confirmation = ["Oui", "Oui pour Tout", "Non", "Stop"]
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

def resultatCSV(resultat, ligne, nomColonne):
    try:
        nomEntreprise = ligne.get("nomEntreprise").rstrip()
        emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
        adresseEntreprise = ligne.get("adresseEntreprise")
        telephoneEntreprise = ligne.get("telephoneEntreprise")

        with open(DOCUMENTS_PATH + "Résultats - " + FICHIER_CSV, 'a', encoding='utf-8') as CSV_file:
            writer = DictWriter(CSV_file, fieldnames=nomColonne)

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