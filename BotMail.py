import os
from dotenv import load_dotenv

DOCUMENTS_PATH = "test_documents/"
load_dotenv()

# !!!!!!! Le CSV doit être formaté sous cette forme !!!!!!!!!!!!!
NOM_COLONNE = ["envoiePrecedent", "nomEntreprise", "emailEntreprise", "adresseEntreprise", "telephoneEntreprise"]
FICHIER_CSV = os.getenv("FICHIER_CSV")

# !!!!!!! Le nom de l'entreprise doit être remplacée par "XXN" !!!!!!!!!!!!!
# !!!!!!! L'adresse de l'entreprise doit être remplacée par "XXA" !!!!!!!!!!!!!
# !!!!!!! Le numéro de téléphone de l'entreprise doit être remplacée par "XXT" !!!!!!!!!!!!!
LETTRE_MOTIVATION = DOCUMENTS_PATH + os.getenv("LETTRE_MOTIVATION")
LETTRE_MOTIVATION_FINALE = DOCUMENTS_PATH + os.getenv("LETTRE_MOTIVATION_FINALE")
LETTRE_MOTIVATION_PDF = DOCUMENTS_PATH + os.getenv("LETTRE_MOTIVATION_PDF")
LIBRE_OFFICE_PATH = os.getenv("LIBRE_OFFICE_PATH")

EMAIL_ENVOYEUR = os.getenv("EMAIL_ENVOYEUR")
EMAIL_CONTENU = DOCUMENTS_PATH + os.getenv("EMAIL_CONTENU")
EMAIL_SUJET = os.getenv("EMAIL_SUJET")
# !!!!!!! Il doit être obtenu depuis le mail utilisé, un accès autorisé !!!!!!!
MDP_APPLICATION = os.getenv("MDP_APPLICATION")

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

# ---------------------------------------------------------------------------------------------------------------------------------------------
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

def resultatCSV(resultat, ligne):
    try:
        nomEntreprise = ligne.get("nomEntreprise").rstrip()
        emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
        adresseEntreprise = ligne.get("adresseEntreprise")
        telephoneEntreprise = ligne.get("telephoneEntreprise")

        with open(DOCUMENTS_PATH + "Résultats - " + FICHIER_CSV, 'a', encoding='utf-8') as CSV_file:
            writer = DictWriter(CSV_file, fieldnames=NOM_COLONNE)

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

# ------------------------
# Lecture CSV

if __name__ == '__main__':
    try:
        from csv import DictReader, DictWriter, writer as csv_writer
        import os

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
                print(ligne)
                envoiePrecedent = ligne.get("envoiePrecedent")
                nomEntreprise = ligne.get("nomEntreprise").rstrip()
                emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
                adresseEntreprise = ligne.get("adresseEntreprise")
                telephoneEntreprise = ligne.get("telephoneEntreprise")

                from validate_email import validate_email

                if (validate_email(emailEntreprise)):

                    # -------------------------------------------
                    # Modification Docx

                    from docx import Document

                    # Impression de l'entreprise à qui va être envoyé le mail.
                    print("---" + nomEntreprise + "---")

                    # Modification du Docx en fonction des noms des entreprises
                    print("Modification...")
                    try:
                        motivationLetter = Document(LETTRE_MOTIVATION)
                        for paragraph in motivationLetter.paragraphs:
                            # Remplacement du Nom de l'entreprise
                            if "XXN" in paragraph.text and nomEntreprise != "":
                                paragraph.text = paragraph.text.replace("XXN", nomEntreprise)

                            # Remplacement de l'Email de l'entreprise
                            if "XXE" in paragraph.text and emailEntreprise != "":
                                paragraph.text = paragraph.text.replace("XXE", emailEntreprise)

                            # Remplacement de l'Adresse de l'entreprise
                            if "XXA" in paragraph.text and adresseEntreprise != "":
                                paragraph.text = paragraph.text.replace("XXA", adresseEntreprise)

                            # Remplacement du numéro de Téléphone de l'entreprise
                            if "XXT" in paragraph.text and telephoneEntreprise != "":
                                paragraph.text = paragraph.text.replace("XXT", telephoneEntreprise)

                            # Remplacement de la Date
                            if "XXD" in paragraph.text:
                                import locale
                                import time
                                # Problème de thread-safe.
                                locale.setlocale(locale.LC_ALL, '')
                                # Obtention de la traduction de la date dans la langue actuelle de l'ordinateur.
                                currentDate = time.localtime()
                                # Traduction de la date
                                translatedCurrentDate = time.strftime("%d %B %Y", currentDate)
                                paragraph.text = paragraph.text.replace("XXD", translatedCurrentDate.title())

                        motivationLetter.save(LETTRE_MOTIVATION_FINALE)

                    except Exception as e:
                        print("ERREUR : Une erreur durant la modification du document " + LETTRE_MOTIVATION + " s'est produite : \n", e)
                        resultatCSV("! Modification Lettre de Motivation !", ligne)
                        exit()

                    # -------------------------------------------
                    # Création PDF

                    import subprocess

                    # Conversion du Docx en PDF
                    print("Conversion...")
                    try:
                        subprocess.run(
                            [
                                LIBRE_OFFICE_PATH,
                                "--headless",
                                "--convert-to",
                                "pdf",
                                LETTRE_MOTIVATION_FINALE,
                                "--outdir",
                                os.path.dirname(LETTRE_MOTIVATION_PDF)
                            ])

                    except Exception as e:
                        print("ERREUR : Une erreur durant la conversion du document " + LETTRE_MOTIVATION_FINALE + " s'est produite : \n", e)
                        resultatCSV("! Conversion en PDF !", ligne)
                        exit()

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
                        import smtplib
                        from email.message import EmailMessage

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
                            resultatCSV("! Corps du Texte !", ligne)
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
                            resultatCSV("! Lecture des PDFs !", ligne)
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
                                resultatCSV("Envoyé !", ligne)

                        except Exception as e:
                            print("ERREUR : Une erreur durant l'envoie du mail s'est produite : \n", e)
                            resultatCSV("! Problème Envoie du Mail !", ligne)
                            exit()

                else:
                    print("ERREUR : L'email --" + emailEntreprise + "-- de --" + nomEntreprise + "-- n'est pas valide.\n")
                    resultatCSV("! Email Invalide !", ligne)

    except FileNotFoundError as e:
        print("ERREUR : Le fichier CSV n'est pas trouvé à partir de ce chemin d'accès.")

    except Exception as e:
        print("ERREUR : Le fichier CSV est bien trouvé mais rencontre un problème : \n", e)