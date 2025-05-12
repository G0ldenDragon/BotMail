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

# Langues slélectionnables
LANGUAGES = ["FR", "EN"]

# Liste des extensions de fichier valables.
CORRECT_SHEET_FILE_EXTENSIONS = [".csv", ".xlsx", ".xls", ".ods"]

CORRECT_DOCUMENT_FILE_EXTENSIONS = [".docx", ".doc"]

# Colonnes des valeurs.
COLUMNS = ['XXP', 'XXE', 'XXN', 'XXA', 'XXT']