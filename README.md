# Utilisation de BotMail

### Packages

- pip freeze > uninstallation.txt
- pip uninstall -r uninstallation.txt -y
- pip install -r ./requirements.txt

### Configuration Nécessaire

- Fichier CSV
    - Le nom du fichier CSV doit comprendre ".csv".

    - Un format de CSV particulier :
        envoiePrecedent | nomEntreprise | emailEntreprise | adresseEntreprise | telephoneEntreprise
        VIDE | Nom de l'entreprise | Email de l'entreprise | Adresse de l'entreprise | Numéro de Téléphone de l'entreprise

- Lettre de Motivation
    - Le remplacement des différentes valeurs se fait sous ce format :
        - XXN : Sera remplacer par le Nom de l'Entreprise.
        - XXE : Sera remplacer par l'Email de l'Entreprise.
        - XXA : Sera remplacer par l'Adresse de l'Entreprise.
        - XXT : Sera remplacer par le numéro de Téléphone de l'Entreprise.

    - La lettre de motivation doit avoir pour extension ".docx".
        Le nom de la lettre de motivation doit aussi avoir ".docx".

- Fichiers PDFs
    - Libre Office doit être installé pour imprimer au format PDF.
        L'utilisation de Word n'est pas encore pris en compte.

    - Tous les fichiers à joindre au mail doivent avoir pour extension ".pdf".
        Tous leurs noms doivent avoir l'extension ".pdf" inclus.
        La lettre de motivation est automatiquement imprimer au format PDF par BotMail.

- Envoie du Mail
    - Le fichier texte contenant le corps du mail doit être et doit avoir dans son nom l'extension ".txt" 

    - Les adresses mails permettant l'envoie d'un mail sont :
        - gmail
        - yahoo
        - outlook

    - Un code d'application permettant au code d'utiliser l'email de l'envoyeur.

### Constantes à définir
##### CSV

- FICHIER_CSV : Le chemin d'accès vers un fichier ".csv" respectant la configuration nécessaire.
    ``` Python
    r"path/to/Adresses.csv"
    ```

##### Lettre de Motivation
- LETTRE_MOTIVATION : Le chemin d'accès vers la lettre de motivation ".docx" respectant la configuration nécessaire.
    ``` Python
    r"path/to/Lettre de Motivation.docx"
    ```

- LETTRE_MOTIVATION_FINALE : La définition du nom de la lettre de motivation modifiée ".docx" respectant la configuration nécessaire.
    ``` Python
    r"Lettre de Motivation Finale.docx"
    ```

##### PDFs
- LIBRE_OFFICE_PATH = 
    ``` Python
    r"path\to\LibreOffice\program\soffice.exe"
    ```

- LETTRE_MOTIVATION_PDF : La définition du nom de la lettre de motivation imprimer ".pdf" respectant la configuration nécessaire.
    ``` Python
    r"Lettre de Motivation Imprimer.pdf"
    ```

- Les chemins d'accès vers les fichiers PDFs à joindre avec le nom à utiliser en JSON.
    ``` Python (JSON)
    PDFFILES = {
        LETTRE_MOTIVATION_PDF : LETTRE_MOTIVATION_PDF,
        r"path/to/the/file.pdf" : r"name of the attachment.pdf",
        r"second/path/to/the/file.pdf" : r"name of the second attachment.pdf"
    }
    ```

##### Email
- MDP_APPLICATION : Le code d'application générer par l'adresse mail de l'envoyeur
    ``` Python
    r"some thing here code"
    ```

- EMAIL_ENVOYEUR : Email de l'envoyeur 
    ``` Python
    r"example.email@gmail.com"
    ```

- EMAIL_CONTENU : Contenu du mail
    ``` Python
    r"path/to/the.Message.txt"
    ```

- EMAIL_SUJET : Sujet du mail
    ``` Python
    r"Candidature Spontanée pour Job Étudiant"
    ```
