import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

from UserInterface import resultatCSV, MessagePrinter, ExceptionRaiser
import Constants

# ---------------------------------------

# !!!!!!! Liste des fichiers PDFs à envoyé et ajout du nom voulu pour l'envoi !!!!!!!!!
PDFFILES = {
    os.getenv("MOTIVATION_LETTER_PATH_PDF") : os.getenv("MOTIVATION_LETTER_FILENAME_PDF"),
    os.getenv("CV_PDF_PATH") : os.getenv("CV_PDF_FILENAME")
}

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_CONTENT_PATH = os.getenv("EMAIL_CONTENT_PATH")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT")
# !!!!!!! Il doit être obtenu depuis le mail utilisé, un accès autorisé !!!!!!!
MDP_APPLICATION = os.getenv("MDP_APPLICATION")

# ---------------------------------------

def send (dataSerializer):
    # Liste des adresses à qui envoyer le mail
    receveurs = [dataSerializer.recipientEmail]

    # Construction du mail
    MessagePrinter({
        "FR" : "Construction du mail...",
        "EN" : "Creation of the mail..."
    })

    mail = EmailMessage()

    mail['From'] = EMAIL_SENDER
    mail['To'] = ', '.join(receveurs)
    mail['Subject'] = EMAIL_SUBJECT

    # Récupération des données du contenu du mail
    MessagePrinter({
        "FR" : "Ajout du corps du mail...",
        "EN" : "Adding the email body..."
    })
    try:
        # Ouvre et lis les données binaires du .txt pour écrire le corps de mail
        with open(EMAIL_CONTENT_PATH, 'r', encoding='utf-8') as file_reader:
            corps = file_reader.read()

    except Exception as e:
        ExceptionRaiser({
            "FR" : "Une erreur durant la lecture du fichier --" + EMAIL_CONTENT_PATH + "-- contenant le corps du mail s'est produite : \n" + str(e),
            "EN" : "An error occurred during the reading of the following file which contains the body of the mail : --" + EMAIL_CONTENT_PATH + "-- \n" + str(e)
        })
        resultatCSV("! Corps du Texte !", dataSerializer)
        exit()

    # Ajout du corps du mail
    mail.set_content(corps)

    # Récupération et ajout des fichiers PDFs au mail
    MessagePrinter({
        "FR" : "Ajout des PDFs au mail...",
        "EN" : "Adding PFF attachments to the mail..."
    })
    try:
        for PDFPath, PDFName in PDFFILES.items():
            with open(PDFPath, 'rb') as file_reader:
                file_data = file_reader.read()
                mail.add_attachment(file_data, maintype='application', subtype='pdf', filename=PDFName)

    except Exception as e:
        ExceptionRaiser({
            "FR" : "Une erreur durant la lecture du fichier contenant le corps du mail --" + EMAIL_CONTENT_PATH + "-- s'est produite : \n" + str(e),
            "EN" : "An error occurred during the reading of the following PDF file : --" + EMAIL_CONTENT_PATH + "-- \n" + str(e)
        })
        resultatCSV("! Lecture des PDFs !", dataSerializer)
        exit()

    # Text: maintype='text', subtype='plain'
    # HTML: maintype='text', subtype='html'
    # Images: maintype='image', subtype='jpeg' or maintype='image', subtype='png'
    # PDFs: maintype='application', subtype='pdf'

    # Construction de l'envoi du mail
    try:
        # Définition du serveur
        smtp_server = ""

        # Trouve la configuration adaptée au mail
        MessagePrinter({
            "FR" : "Recherche de la configuration adaptée à l'adresse mail de l'envoyeur...",
            "EN" : "Searching for the configuration adapted to the sender's email address..."
        })
        for provider, config in Constants.CONFIGURATION_STMP.items():
            if provider in EMAIL_SENDER:
                smtp_server = config["smtp_server"]
                smtp_port = config["smtp_port"]
                break

        # Si le serveur est toujours vide, aucune configuration n'a été trouvée.
        if smtp_server == "":
            ExceptionRaiser({
                "FR" : "L'adresse mail n'a pas été reconnue, la configuration ne peut être faîtes.",
                "EN" : "The mail address isn't recognized, configuration can't be set up."
            })

        # Envoie du mail
        MessagePrinter({
            "FR" : "Envoie à " + dataSerializer.recipientName + "...",
            "EN" : "Sending to " + dataSerializer.recipientName + "..."
        })
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(EMAIL_SENDER, MDP_APPLICATION)
            server.sendmail(EMAIL_SENDER, receveurs, mail.as_string())

        MessagePrinter({
            "FR" : "Mail envoyé !\n\n",
            "EN" : "Mail sent !\n\n"
        })

        # Enregistrement des résultat dans un CSV annexe.
        resultatCSV("Envoyé !", dataSerializer)

    except Exception as e:
        ExceptionRaiser({
            "FR" : "Une erreur durant l'envoie du mail s'est produite : \n" + str(e),
            "EN" : "An error occurred during the sending of the mail : \n" + str(e)
        })
        resultatCSV("! Problème Envoie du Mail !", dataSerializer)
        exit()