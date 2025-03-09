import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

from UserInterface import confirmationUtilisateur, resultatCSV
import Constants

# ---------------------------------------

# Chemin vers le dossier où est stocké la plupart des fichiers
DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH")

# !!!!!!! Liste des fichiers PDFs à envoyé et ajout du nom voulu pour l'envoi !!!!!!!!!
PDFFILES = {
    DOCUMENTS_PATH + os.getenv("MOTIVATION_LETTER_PDF") : os.getenv("MOTIVATION_LETTER_PDF"),
    os.getenv("CV_PDF") : r"BIGOTTE Owenn - Curriculum Vitae (CV).pdf"
}

EMAIL_ENVOYEUR = os.getenv("EMAIL_ENVOYEUR")
EMAIL_CONTENU = DOCUMENTS_PATH + os.getenv("EMAIL_CONTENU")
EMAIL_SUJET = os.getenv("EMAIL_SUJET")
# !!!!!!! Il doit être obtenu depuis le mail utilisé, un accès autorisé !!!!!!!
MDP_APPLICATION = os.getenv("MDP_APPLICATION")

# ---------------------------------------

class EmailSender:
    def __init__(self, ligne):
        self.ligne = ligne
        self.envoiePrecedent = ligne.get("envoiePrecedent")
        self.nomEntreprise = ligne.get("nomEntreprise").rstrip()
        self.emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
        self.adresseEntreprise = ligne.get("adresseEntreprise")
        self.telephoneEntreprise = ligne.get("telephoneEntreprise")


    def send (self):
        # Liste des adresses à qui envoyer le mail
        receveurs = [self.emailEntreprise]

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
            resultatCSV("! Corps du Texte !", self.ligne)
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
            resultatCSV("! Lecture des PDFs !", self.ligne)
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
            for provider, config in Constants.CONFIGURATION_STMP.items():
                if provider in EMAIL_ENVOYEUR:
                    smtp_server = config["smtp_server"]
                    smtp_port = config["smtp_port"]
                    break

            # Si le serveur est toujours vide, aucune configuration n'a été trouvée.
            if smtp_server == "":
                raise Exception("L'adresse mail n'a pas été reconnue, la configuration ne peut être faîtes.")

            # Envoie du mail
            print("Envoie à " + self.nomEntreprise + "...")
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(EMAIL_ENVOYEUR, MDP_APPLICATION)
                server.sendmail(EMAIL_ENVOYEUR, receveurs, mail.as_string())

                print("Mail envoyé !\n\n")

                # Enregistrement des résultat dans un CSV annexe.
                resultatCSV("Envoyé !", self.ligne)

        except Exception as e:
            print("ERREUR : Une erreur durant l'envoie du mail s'est produite : \n", e)
            resultatCSV("! Problème Envoie du Mail !", self.ligne)
            exit()