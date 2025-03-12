# Configuration en fonction des mails utilisée
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

# Liste des extensions de fichier valables.
CORRECT_EXTENSIONS = [".csv", ".xlsx", ".xls", ".ods"]

# Colonnes des valeurs.
COLUMNS = ['XXP', 'XXE', 'XXN', 'XXA', 'XXT']