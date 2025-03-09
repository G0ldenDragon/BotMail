import os
from csv import DictReader, DictWriter, writer as csv_writer
from validate_email import validate_email
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

from DocumentModificator import DocumentModificator
from UserInterface import confirmationUtilisateur, resultatCSV

# ---------------------------------------

# Chemin vers le dossier où est stocké la plupart des fichiers
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")

# !!!!!!! Le CSV doit être formaté sous cette forme !!!!!!!!!!!!!
NOM_COLONNE = ["envoiePrecedent", "nomEntreprise", "emailEntreprise", "adresseEntreprise", "telephoneEntreprise"]
FICHIER_CSV = os.getenv("FICHIER_CSV")

EMAIL_ENVOYEUR = os.getenv("EMAIL_ENVOYEUR")
EMAIL_CONTENU = DOCUMENTS_PATH + os.getenv("EMAIL_CONTENU")
EMAIL_SUJET = os.getenv("EMAIL_SUJET")
# !!!!!!! Il doit être obtenu depuis le mail utilisé, un accès autorisé !!!!!!!
MDP_APPLICATION = os.getenv("MDP_APPLICATION")


LETTRE_MOTIVATION_PDF = DOCUMENTS_PATH + os.getenv("LETTRE_MOTIVATION_PDF")
# !!!!!!! Liste des fichiers PDFs à envoyé et ajout du nom voulu pour l'envoi !!!!!!!!!
PDFFILES = {
    LETTRE_MOTIVATION_PDF : LETTRE_MOTIVATION_PDF,
    os.getenv("CV_PDF") : r"BIGOTTE Owenn - Curriculum Vitae (CV).pdf"
}

CONFIGURATION_STMP = {
    "gmail" : {
        "smtp_server" : "smtp.gmail.com",
        "smtp_port" : 465
    },
    "yahoo" : {
        "smtp_server" : "smtp.mail.yahoo.com",
        "smtp_port" : 465
    },
    "outlook" : {
        "smtp_server" : "smtp-mail.outlook.com",
        "smtp_port" : 465
        # or maybe 587 ?
    }
}

# ------------------------
# Lecture CSV

if __name__ == '__main__':
    try:
        # Vérification du CSV
        if os.stat(DOCUMENTS_PATH + FICHIER_CSV).st_size == 0:
            print("ERREUR : Le fichier CSV est vide.")

        # Lecture et extractions des données du CSV
        with open(DOCUMENTS_PATH + FICHIER_CSV, 'r', encoding='utf-8') as CSVFile:

            # Définition du choix utilisateur
            choixUtilisateur = ""

            # Créer ou demande l'écrasement du fichier CSV de résultats
            try:
                resultFile = open(DOCUMENTS_PATH + "Résultats - " + FICHIER_CSV, 'x', encoding='utf-8')
                resultFile.close()

            except Exception as e:
                messageChoix = ("Le fichier --" + DOCUMENTS_PATH + "Résultats - " + FICHIER_CSV + "-- va être écrasé, voulez-vous continuer ?\n")
                confirmation = ["Oui", "Non"]

                for index, choix in enumerate(confirmation):
                    messageChoix += f'{index+1}) {choix}\n'

                messageChoix += '-> '

                while choixUtilisateur not in confirmation:
                    choixUtilisateur = input(messageChoix)

                print()

                if choixUtilisateur == "Non":
                    print("Arrêt...")
                    exit()

                if choixUtilisateur == "Oui":
                    resultFile = open(DOCUMENTS_PATH + "Résultats - " + FICHIER_CSV, 'w', encoding='utf-8')
                    resultFile.close()
                    choixUtilisateur = ""

            # Chaque colonne d'une ligne est définie comme suis 
            donnees = DictReader(CSVFile, fieldnames = NOM_COLONNE, delimiter=';')

            for ligne in donnees:
                envoiePrecedent = ligne.get("envoiePrecedent")
                nomEntreprise = ligne.get("nomEntreprise").rstrip()
                emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
                # adresseEntreprise = ligne.get("adresseEntreprise")
                # telephoneEntreprise = ligne.get("telephoneEntreprise")

                if (validate_email(emailEntreprise)):

                    # -------------------------------------------
                    # Modification Docx

                    # Impression de l'entreprise à qui va être envoyé le mail.
                    print("---" + nomEntreprise + "---")
                    documentModificator = DocumentModificator(ligne)

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
                    choixUtilisateur = confirmationUtilisateur("Voulez-vous envoyer ce mail ?")

                    if choixUtilisateur != "Oui pour Tout":

                        if envoiePrecedent == "":
                            messageChoix = "\nVoulez-vous envoyer ce mail à --" + nomEntreprise + "-- ?\n"
                            choixUtilisateur = confirmationUtilisateur(messageChoix)

                        if envoiePrecedent == "Envoyé !":
                            messageChoix = "Un mail à déjà été envoyé à --" + nomEntreprise + "--, voulez-vous en renvoyer un ?\n"
                            choixUtilisateur = confirmationUtilisateur(messageChoix)

                    # Si Stop : Arrêt du programme
                    if choixUtilisateur == "Stop":
                        print("Arrêt...")
                        exit()

                    # Si Non : Entreprise suivante
                    if choixUtilisateur == "Non":
                        print("Entreprise suivante...\n")

                    # Si Oui : Envoie d'un mail
                    if choixUtilisateur == "Oui":

                        # Liste des adresses à qui envoyé le mail
                        receveurs = [emailEntreprise]

                        # Construction du mail
                        print("Construction du mail...")
                        mail = EmailMessage()

                        mail['From'] = EMAIL_ENVOYEUR
                        mail['To'] = ', '.join(receveurs)
                        mail['Subject'] = EMAIL_SUJET

                        # Récupération des données du contenu du mail
                        print("Ajout du corps du mail...")
                        try:
                            # Ouvre et lis les données binaires du .txt pour écrire le corps de mail
                            with open(EMAIL_CONTENU, 'r', encoding='utf-8') as file_reader:
                                corps = file_reader.read()

                        except Exception as e:
                            print("ERREUR : Une erreur durant la lecture du fichier --" + EMAIL_CONTENU + "-- contenant le corps du mail s'est produite : \n", e)
                            resultatCSV("! Corps du Texte !", ligne, NOM_COLONNE)
                            exit()

                        # Ajout du corps du mail
                        mail.set_content(corps)

                        # Récupération et ajout des fichiers PDFs au mail
                        print("Ajout des PDFs au mail...")
                        try:
                            for PDFPath, PDFName in PDFFILES.items():
                                with open(PDFPath, 'rb') as file_reader:
                                    file_data = file_reader.read()
                                    mail.add_attachment(file_data, maintype='application', subtype='pdf', filename=PDFName)

                        except Exception as e:
                            print("ERREUR : Une erreur durant la lecture du fichier contenant le corps du mail --" + EMAIL_CONTENU + "-- s'est produite : \n", e)
                            resultatCSV("! Lecture des PDFs !", ligne, NOM_COLONNE)
                            exit()
                        # Text: maintype='text', subtype='plain'
                        # HTML: maintype='text', subtype='html'
                        # Images: maintype='image', subtype='jpeg' or maintype='image', subtype='png'
                        # PDFs: maintype='application', subtype='pdf'

                        # Construction de l'envoie du mail
                        try:
                            # Définition du serveur
                            smtp_server = ""

                            # Trouve la configuration adaptée au mail
                            print("Recherche de la configuration adaptée à l'adresse mail de l'envoyeur...")
                            for provider, config in CONFIGURATION_STMP.items():
                                if provider in EMAIL_ENVOYEUR:
                                    smtp_server = config["smtp_server"]
                                    smtp_port = config["smtp_port"]
                                    break

                            # Si le serveur est toujours vide, aucune configuration n'a été trouvée.
                            if smtp_server == "":
                                raise Exception("L'adresse mail n'a pas été reconnue, la configuration ne peut-être faîtes.")

                            # Envoie du mail
                            print("Envoie à " + nomEntreprise + "...")
                            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                                server.login(EMAIL_ENVOYEUR, MDP_APPLICATION)
                                server.sendmail(EMAIL_ENVOYEUR, receveurs, mail.as_string())

                                print("Mail envoyé !\n\n")

                                # Enregistrement des résultat dans un CSV annexe.
                                resultatCSV("Envoyé !", ligne, NOM_COLONNE)

                        except Exception as e:
                            print("ERREUR : Une erreur durant l'envoie du mail s'est produite : \n", e)
                            resultatCSV("! Problème Envoie du Mail !", ligne, NOM_COLONNE)
                            exit()

                else:
                    print("ERREUR : L'email --" + emailEntreprise + "-- de --" + nomEntreprise + "-- n'est pas valide.\n")
                    resultatCSV("! Email Invalide !", ligne, NOM_COLONNE)

    except FileNotFoundError as e:
        print("ERREUR : Le fichier CSV n'est pas trouvé à partir de ce chemin d'accès.")

    except Exception as e:
        print("ERREUR : Le fichier CSV est bien trouvé mais rencontre un problème : \n", e)