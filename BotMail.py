import os
from csv import DictReader, DictWriter, writer as csv_writer
from validate_email import validate_email
from dotenv import load_dotenv
load_dotenv()

from DocumentModificator import DocumentModificator
from UserInterface import confirmationUtilisateur, resultatCSV, nomFichierDuChemin
from EmailSender import EmailSender
import Constants

# ---------------------------------------

# Chemin d'accès vers le fichier CSV
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
CSV_RESULT_FILE_PATH = os.getenv("CSV_RESULT_FILE_PATH")

# ---------------------------------------

# Lecture CSV
if __name__ == '__main__':
    extension = os.path.splitext(nomFichierDuChemin(CSV_FILE_PATH))[1]
    print(extension)

    # Vérification du fichier, s'il est vide il ne sert à rien de continuer.
    if os.stat(CSV_FILE_PATH).st_size == 0:
        print("ERREUR : Le fichier CSV est vide.")
        exit()

    # Créer ou demande l'écrasement du fichier CSV résultant
    try:
        resultFile = open(CSV_RESULT_FILE_PATH, 'x', encoding='utf-8')
        resultFile.close()

    except Exception as e:
        choixUtilisateur = confirmationUtilisateur(
            "Le fichier --" + nomFichierDuChemin(CSV_RESULT_FILE_PATH) + "-- va être écrasé, voulez-vous continuer ?\n",
            ["Oui", "Non"]
        )

        if choixUtilisateur == "Non":
            print("Arrêt...")
            exit()

        if choixUtilisateur == "Oui":
            resultFile = open(CSV_RESULT_FILE_PATH, 'w', encoding='utf-8')
            resultFile.close()
            choixUtilisateur = ""

    try:
        # Lecture et extractions des données du CSV
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as CSVFile:

            # Chaque colonne d'une ligne est définie comme suis 
            donnees = DictReader(CSVFile, fieldnames = Constants.NOM_COLONNE, delimiter=';')

            for ligne in donnees:
                # Définition du choix utilisateur
                choixUtilisateur = ""

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
                    print("Modifié !")

                    # -------------------------------------------
                    # Création PDF

                    # Conversion du Docx en PDF
                    print("Conversion en PDF...")
                    documentModificator.documentConvertor()
                    print("Converti !")

                    # -------------------------------------------
                    # Envoie des mails

                    # Si le choix précédent est "Oui pour Tout", on ne pose pas la question
                    if choixUtilisateur != "Oui pour Tout":

                        # Si un email a déjà été envoyé à ce destinataire
                        if envoiePrecedent == "Envoyé !":
                            choixUtilisateur = confirmationUtilisateur(
                                "Un mail à déjà été envoyé à --" + nomEntreprise + "--, voulez-vous en renvoyer un ? (N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n",
                                ["Oui", "Oui pour Tout", "Non", "Stop"]
                            )

                        else:
                            choixUtilisateur = confirmationUtilisateur(
                                "\nVoulez-vous envoyer ce mail à --" + nomEntreprise + "-- ? (N'oubliez pas de vérifier le PDF de la lettre de motivation généner.)\n",
                                ["Oui", "Oui pour Tout", "Non", "Stop"]
                            )

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

            print("Plus aucun destinataire, arrêt...")

    except FileNotFoundError as e:
        print("ERREUR : Le fichier CSV n'est pas trouvé à partir de ce chemin d'accès.")

    except Exception as e:
        print("ERREUR : Le fichier CSV est bien trouvé mais rencontre un problème : \n", e)