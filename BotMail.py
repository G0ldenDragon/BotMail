import os
from csv import DictReader, DictWriter, writer as csv_writer
from validate_email import validate_email
from dotenv import load_dotenv
load_dotenv()

from DocumentModificator import DocumentModificator
from UserInterface import confirmationUtilisateur, resultatCSV
from EmailSender import EmailSender
import Constants

# ---------------------------------------

# Chemin vers le dossier où est stocké la plupart des fichiers
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")

# !!!!!!! Le CSV doit être formaté sous cette forme !!!!!!!!!!!!!
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")

# ---------------------------------------

# Lecture CSV
if __name__ == '__main__':
    try:
        # Vérification du CSV
        if os.stat(DOCUMENTS_PATH + CSV_FILE_PATH).st_size == 0:
            print("ERREUR : Le fichier CSV est vide.")

        # Lecture et extractions des données du CSV
        with open(DOCUMENTS_PATH + CSV_FILE_PATH, 'r', encoding='utf-8') as CSVFile:

            # Définition du choix utilisateur
            choixUtilisateur = ""

            # Créer ou demande l'écrasement du fichier CSV résultant
            try:
                resultFile = open(DOCUMENTS_PATH + "Résultats - " + CSV_FILE_PATH, 'x', encoding='utf-8')
                resultFile.close()

            except Exception as e:
                choixUtilisateur = confirmationUtilisateur(
                    "Le fichier --" + DOCUMENTS_PATH + "Résultats - " + CSV_FILE_PATH + "-- va être écrasé, voulez-vous continuer ?\n",
                    ["Oui", "Non"]
                )

                if choixUtilisateur == "Non":
                    print("Arrêt...")
                    exit()

                if choixUtilisateur == "Oui":
                    resultFile = open(DOCUMENTS_PATH + "Résultats - " + CSV_FILE_PATH, 'w', encoding='utf-8')
                    resultFile.close()
                    choixUtilisateur = ""

            # Chaque colonne d'une ligne est définie comme suis 
            donnees = DictReader(CSVFile, fieldnames = Constants.NOM_COLONNE, delimiter=';')

            for ligne in donnees:
                envoiePrecedent = ligne.get("envoiePrecedent")
                nomEntreprise = ligne.get("nomEntreprise").rstrip()
                emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
                # adresseEntreprise = ligne.get("adresseEntreprise")
                # telephoneEntreprise = ligne.get("telephoneEntreprise")

                if (validate_email(emailEntreprise)):

                    # Impression de l'entreprise à qui va être envoyé le mail.
                    print("---" + nomEntreprise + "---")
                    documentModificator = DocumentModificator(ligne)

                    # -------------------------------------------
                    # Modification Docx

                    # Modification du Docx en fonction des noms des entreprises
                    print("Modification...")
                    documentModificator.documentModificator()

                    # -------------------------------------------
                    # Création PDF

                    # Conversion du Docx en PDF
                    print("Conversion...")
                    documentModificator.documentConvertor()

                    # -------------------------------------------
                    # Envoie des mails

                    # Choix de l'utilisateur
                    choixUtilisateur = confirmationUtilisateur(
                        "Voulez-vous envoyer ce mail ? (N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n",
                        ["Oui", "Oui pour Tout", "Non", "Stop"]
                        )

                    # Si le
                    if choixUtilisateur != "Oui pour Tout":

                        if envoiePrecedent == "":
                            messageChoix = "\nVoulez-vous envoyer ce mail à --" + nomEntreprise + "-- ?\n"
                            choixUtilisateur = confirmationUtilisateur(messageChoix, ["Oui", "Oui pour Tout", "Non", "Stop"])

                        if envoiePrecedent == "Envoyé !":
                            messageChoix = "Un mail à déjà été envoyé à --" + nomEntreprise + "--, voulez-vous en renvoyer un ?\n"
                            choixUtilisateur = confirmationUtilisateur(messageChoix, ["Oui", "Oui pour Tout", "Non", "Stop"])


                    # Si Stop : Arrêt du programme
                    if choixUtilisateur == "Stop":
                        print("Arrêt...")
                        exit()

                    # Si Non : Entreprise suivante
                    if choixUtilisateur == "Non":
                        print("Entreprise suivante...\n")

                    # Si Oui : Envoie d'un mail
                    if choixUtilisateur == "Oui" or choixUtilisateur == "Oui pour Tout":
                        emailSender = EmailSender(ligne)
                        emailSender.send()

                else:
                    print("ERREUR : L'email --" + emailEntreprise + "-- de --" + nomEntreprise + "-- n'est pas valide.\n")
                    resultatCSV("! Email Invalide !", ligne)

    except FileNotFoundError as e:
        print("ERREUR : Le fichier CSV n'est pas trouvé à partir de ce chemin d'accès.")

    except Exception as e:
        print("ERREUR : Le fichier CSV est bien trouvé mais rencontre un problème : \n", e)