# EmailSender.py

import smtplib
from email.message import EmailMessage


from DataSerializer import DataSerializer
from Models.EnvironmentVariable import load_env, get_variable
load_env()
from Models.Language import Language


from Constants import CONFIGURATION_STMP
# !!!!!!! Liste des fichiers PDFs à envoyé et ajout du nom voulu pour l'envoi !!!!!!!!!
PDFFILES = {
    get_variable("MOTIVATION_LETTER_PATH_PDF") : get_variable("MOTIVATION_LETTER_FILENAME_PDF"),
    get_variable("CV_PDF_PATH") : get_variable("CV_PDF_FILENAME")
}

EMAIL_SENDER = get_variable("EMAIL_SENDER")
EMAIL_CONTENT_PATH = get_variable("EMAIL_CONTENT_PATH")
EMAIL_SUBJECT = get_variable("EMAIL_SUBJECT")
# !!!!!!! Il doit être obtenu depuis le mail utilisé, un accès autorisé !!!!!!!
MDP_APPLICATION = get_variable("MDP_APPLICATION")
SCRIPT_NAME = "email_sender"


def send(data_serializer: DataSerializer):
    language = Language()

    # Liste des adresses à qui envoyer le mail
    receveurs = [data_serializer.recipientEmail]

    # Construction du mail
    print(language.get_translation(SCRIPT_NAME, "email_construction"))

    mail = EmailMessage()

    mail['From'] = EMAIL_SENDER
    mail['To'] = ', '.join(receveurs)
    mail['Subject'] = EMAIL_SUBJECT

    # Récupération des données du contenu du mail
    print(language.get_translation(SCRIPT_NAME, "email_body"))
        
    try:
        # Ouvre et lis les données binaires du .txt pour écrire le corps de mail
        with open(EMAIL_CONTENT_PATH, 'r', encoding='utf-8') as file_reader:
            corps = file_reader.read()

    except Exception as e:
        data_serializer.csv_result(language.get_translation(SCRIPT_NAME, "result_email_body_general"))
        raise Exception(language.get_translation(SCRIPT_NAME, "exception_email_body_general").replace(";;;", EMAIL_CONTENT_PATH) + str(e))

    # Ajout du corps du mail
    mail.set_content(corps)

    # Récupération et ajout des fichiers PDFs au mail
    print(language.get_translation(SCRIPT_NAME, "email_attachments"))

    try:
        for PDFPath, PDFName in PDFFILES.items():
            if PDFPath and PDFName:
                with open(PDFPath, 'rb') as file_reader:
                    file_data = file_reader.read()
                    mail.add_attachment(file_data, maintype='application', subtype='pdf', filename=PDFName)

    except Exception as e:
        data_serializer.csv_result(language.get_translation(SCRIPT_NAME, "result_email_attachments_general"))
        raise Exception(language.get_translation(SCRIPT_NAME, "exception_email_attachments_general") + str(e))


    # Text: maintype='text', subtype='plain'
    # HTML: maintype='text', subtype='html'
    # Images: maintype='image', subtype='jpeg' or maintype='image', subtype='png'
    # PDFs: maintype='application', subtype='pdf'

    # Construction de l'envoi du mail
    try:
        # Définition du serveur
        smtp_server = ""

        # Trouve la configuration adaptée à l'email
        print(language.get_translation(SCRIPT_NAME, "stmp_configuration"))
            
        for provider, config in CONFIGURATION_STMP.items():
            if provider in EMAIL_SENDER:
                smtp_server = config["smtp_server"]
                smtp_port = config["smtp_port"]
                break

        # Si le serveur est toujours vide, aucune configuration n'a été trouvée.
        if smtp_server == "":
            raise Exception(language.get_translation(SCRIPT_NAME, "exception_email_stmp"))

        # Envoie du mail
        print(language.get_translation(SCRIPT_NAME, "email_sending").replace(";;;", data_serializer.recipientName))
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(EMAIL_SENDER, MDP_APPLICATION)
            server.sendmail(EMAIL_SENDER, receveurs, mail.as_string())

        print(language.get_translation(SCRIPT_NAME, "email_sent") + "\n\n")
        
        # Enregistrement des résultat dans un CSV annexe.
        data_serializer.csv_result(language.get_translation(SCRIPT_NAME, "email_sent"))


    except Exception as e:
        data_serializer.csv_result(language.get_translation(SCRIPT_NAME, "result_email_general"))
        raise Exception(language.get_translation(SCRIPT_NAME, "exception_email_general") + str(e))
