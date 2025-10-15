# Constants.py

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
        # ou peut-être 587 ?
    }
}

# Liste des extensions des fichiers valables.
CORRECT_SHEET_FILE_EXTENSIONS = [".csv", ".xlsx", ".xls", ".ods"]
CORRECT_DOCUMENT_FILE_EXTENSIONS = [".docx", ".doc"]

# Colonnes des valeurs.
COLUMNS = ['XXP', 'XXE', 'XXN', 'XXA', 'XXT']

# Couleurs par défaut
COLORS = {
    "white" : (1, 1, 1, 1),
    "black" : (0, 0, 0, 1),
    "grey" : (0.5, 0.5, 0.5, 1),
    "lightBlue" : (0.1, 0.5, 0.9, 1),
    "red" : (1, 0, 0, 1)
}

# Langues sélectionnable
LANGUAGES = ["FR", "EN"]


# ----------------
# DANS LE .env !
# Hauteur des éléments UI standardisés
STANDARDIZED_HEIGHT = 40

# Espace vide pour séparation UI standardisés
STANDARDIZED_VOID_HEIGHT = 20
STANDARDIZED_VOID_WIDTH = 50