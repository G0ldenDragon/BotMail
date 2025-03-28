# Utilisation de BotMail

### Fonctionnement
BotMail va, à partir d'un fichier CSV renseignant le nom et l'email du destinataire, modifier la Lettre de Motivation (en ".docx") et envoyer automatiquement des mails.
Puis il va imprimer sous format PDF la Lettre de Motivation et le joindre en tant que document au mail.
Il est possible d'ajouter d'autres documents, tous uniquement sous format PDF.
Chaque problème rencontré va, par sécurité, faire s'arrêter le programme.
Une demande via le CMD permet de choisir si on veut effectivement envoyé ce mail ou non permettant au préalable de s'assurer que la Lettre de Motivation à bien été modifier.

### Version de Python
La version utilisée pour la création de ce Bot est Python 3.9.13

### Rappels d'utilisation
- `git clone https://github.com/G0ldenDragon/BotMail.git` (Permet l'importation du projet)
- `.venv\Scripts\activate` (Permet l'activation de .venv)

### Installation des dépendances safe
``` Bash 
pip freeze > uninstallation.txt
pip uninstall -r uninstallation.txt -y
pip install -r ./requirements.txt
```

### Configuration Nécessaire
- Fichier CSV
    - Le nom du fichier CSV doit comprendre ".csv".
    - Un format de CSV particulier :
        previousSend | recipientName | recipientEmail | recipientAddress | recipientPhone
        VIDE | Nom du destinataire | Email du destinataire | Adresse du destinataire | Numéro de Téléphone du destinataire

- Lettre de Motivation
    - Le remplacement des différentes valeurs se fait sous ce format :
        - XXN : Sera remplacer par le Nom du destinataire.
        - XXE : Sera remplacer par l'Email du destinataire.
        - XXA : Sera remplacer par l'Adresse du destinataire.
        - XXT : Sera remplacer par le numéro de Téléphone du destinataire.

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

    - Un code d'application permettant au code d'utiliser l'email de l'envoyeur. (Trouvé dans Google dans "Mots de passe des applications")

### Constantes à définir
##### CSV
- FILE_SHEET_PATH : Le chemin d'accès vers un fichier ".csv" respectant la configuration nécessaire.
    ``` Python
    r"path/to/Adresses.csv"
    ```

##### Lettre de Motivation
- MOTIVATION_LETTER_PATH : Le chemin d'accès vers la lettre de motivation ".docx" respectant la configuration nécessaire.
    ``` Python
    r"path/to/Lettre de Motivation.docx"
    ```

- MOTIVATION_LETTER_PATH_FINAL : La définition du nom de la lettre de motivation modifiée ".docx" respectant la configuration nécessaire.
    ``` Python
    r"Lettre de Motivation Finale.docx"
    ```

##### PDFs
- LIBRE_OFFICE_PATH = 
    ``` Python
    r"path\to\LibreOffice\program\soffice.exe"
    ```

- MOTIVATION_LETTER_PATH_PDF : La définition du nom de la lettre de motivation imprimer ".pdf" respectant la configuration nécessaire.
    ``` Python
    r"Lettre de Motivation Imprimer.pdf"
    ```

- Les chemins d'accès vers les fichiers PDFs à joindre avec le nom à utiliser en JSON.
    ``` Python (JSON)
    PDFFILES = {
        MOTIVATION_LETTER_PATH_PDF : MOTIVATION_LETTER_PATH_PDF,
        r"path/to/the/file.pdf" : r"name of the attachment.pdf",
        r"second/path/to/the/file.pdf" : r"name of the second attachment.pdf"
    }
    ```

##### Email
- MDP_APPLICATION : Le code d'application générer par l'adresse mail de l'envoyeur
    ``` Python
    r"some thing here code"
    ```

- EMAIL_SENDER : Email de l'envoyeur 
    ``` Python
    r"example.email@gmail.com"
    ```

- EMAIL_CONTENT_PATH : Contenu du mail
    ``` Python
    r"path/to/the.Message.txt"
    ```

- EMAIL_SUBJECT : Sujet du mail
    ``` Python
    r"Candidature Spontanée pour Job Étudiant"
    ```

### Failles et modifications trouvées
- La lecture des fichiers CSV est facilement sujet à la casse. (Mise à jour vers la librairie Panda envisagé)
- Correction de l'interface IHM dans le terminal nécessaire.