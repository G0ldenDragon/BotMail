# Configuration en fonction des mails utilisé
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

# !!!!!!! Le fichier CSV doit être formaté sous cette forme !!!!!!!!!!!!!
NOM_COLONNE = ["envoiePrecedent", "nomEntreprise", "emailEntreprise", "adresseEntreprise", "telephoneEntreprise"]