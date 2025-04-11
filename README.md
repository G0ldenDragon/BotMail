# BotMail
## À quoi sert BotMail ?
BotMail a pour but de simplifier l'envoi d'emails avec lettres à plusieurs destinataires depuis n'importe quel système d'exploitation (*par exemple : pour envoyer une demande d'embauche à plusieurs entreprises*).

Ainsi, si une lettre est jointe à l'email, elle s'adaptera (à partir d'un fichier Excel/Calc) au nom du destinataire, à son adresse, à son numéro de téléphone, et à la date (*cf : formatage du fichier Excel/Calc*).

Pour cela, deux versions existent :  
- **BotMail.py** est la version terminal.  
- **BotMailGUI.py** est la version graphique (cette deuxième version est dédiée aux personnes ne sachant pas développer du tout et permet d'être compilée pour en faire un fichier `.exe`, par exemple).

## Fonctionnement 
Le fonctionnement de BotMail est assez simple :  

1. Récupération des informations contenues dans un fichier Excel/Calc (*cf : Formatage du fichier Excel/Calc*).  

2. Renseignement des informations **selon une en-tête très spécifique** (*cf : Formatage du fichier Excel/Calc*) dans la (ou les) lettre donnée (*cf : Formatage du document Word/Writer*).  

3. Après modification de la (ou des) lettre(s), celle-ci est convertie au format PDF.  

4. Le sujet, le (ou les) destinataire(s), le corps ainsi que les fichiers PDF générés et ajoutés en complément sont intégrés à l'email (uniquement au format PDF).  

5. Un blocage automatique est effectué ici pour permettre de vérifier si le document généré est bien sous le format voulu. Cela permet à l'utilisateur de s'assurer qu'aucune erreur ne s'est glissée avant l'envoi de l'email.  
   *Par exemple : si la modification de la lettre s'est mal déroulée, le blocage permet à l'utilisateur de vérifier si le PDF s'est bien généré. Si ce n'est pas le cas, il répond "Non" à la question "Voulez-vous envoyer cet email à XXX ?".*  

6. Enfin, si tout est correct pour l'utilisateur, il suffit de confirmer l'envoi. L'email est alors envoyé avec l'adresse email de l'utilisateur.  
   Il existe aussi un raccourci permettant d'envoyer sans redemander de confirmation à tous les prochains destinataires (à la question "Voulez-vous envoyer cet email à XXX ?", le choix "Oui pour tous").  

7. Si l'email a bien été envoyé, sans aucune erreur, l'inscription "Envoyé" sera ajoutée à la colonne "**XXP**" du fichier Excel/Calc de résultat (*cf : Formatage du fichier Excel/Calc*).

### Sécurité
Par sécurité, tout problème survenant dans le déroulement du programme BotMail entraînera automatiquement son arrêt.  

L'erreur sera également ajoutée à la colonne "**XXP**" dans le fichier Excel/Calc de résultats, ce qui permettra de savoir quels destinataires n'ont pas reçu l'email (*cf : Formatage du fichier Excel/Calc*).

## Installation
### Version de Python
La version utilisée pour la développement de BotMail est Python 3.9.13.

### Rappels d'utilisation
- Importation du projet  : 
`git clone https://github.com/G0ldenDragon/BotMail.git`
- Activation du `.venv` sous Windows : `.venv\Scripts\activate`

### Installation des dépendances sans perte des anciennes
``` Bash 
pip freeze > uninstallation.txt
pip uninstall -r uninstallation.txt -y
pip install -r ./requirements.txt
```

## Configurations Nécessaires  
Cette catégorie recense toutes les informations à renseigner pour l'utilisation de BotMail.  

### Formatage du fichier Excel/Calc  
- Le nom du fichier Excel/Calc doit comporter l'une des extensions supportées :  
    - Actuellement supportées : `.csv`, `.xls`, `.xlsx`, `.ods`  
    (*cf : dans `Constants.py` : `CORRECT_SHEET_EXTENSIONS`, les extensions Excel/Calc supportées par BotMail*).  

- ⚠️ **ATTENTION : Une en-tête doit être présente sur la première ligne du fichier.**  
    - 📧 Écrire "**XXE**" dans la première ligne d'une colonne indique à BotMail que les lignes suivantes de cette colonne correspondront à l'adresse email des destinataires auxquels un email sera envoyé. (Pour chaque adresse email renseignée dans cette colonne, un email sera envoyé.)  
    - 🏭 Écrire "**XXN**" dans la première ligne d'une colonne indique à BotMail que les lignes suivantes de cette colonne correspondront au nom du destinataire.  
    - 📪 Écrire "**XXA**" dans la première ligne d'une colonne indique à BotMail que les lignes suivantes de cette colonne correspondront à l'adresse postale du destinataire.  
    - ☎️ Écrire "**XXT**" dans la première ligne d'une colonne indique que les lignes suivantes de cette colonne correspondront au numéro de téléphone du destinataire.

  *Exemple d'en-tête*  

    | ✅ **XXP** | 📧 **XXE** | 🏭 **XXN** | 📪 **XXA** | ☎️ **XXT** |  
    | --- | --- | --- | --- | --- |  
    | Résultat d'un précédent envoi | Adresse email du destinataire | Nom du destinataire | Adresse postale du destinataire | Numéro de téléphone du destinataire |  
    | Envoyé | example@example.com | ExampleEnterprise | 92 avenue XXX - Paris | +33 7 XX XX XX XX |

### Formatage du document Word/Writer  
- Le nom du document Word/Writer doit comporter l'une des extensions supportées :  
    - Actuellement supportées : `.docx`  
    (*cf : dans `Constants.py` : `CORRECT_DOCUMENT_EXTENSIONS`, les extensions Word/Writer supportées par BotMail*).  

- De la même manière que le fichier Excel/Calc, écrire :  
    - 📧 **XXE** à l'emplacement de l'adresse email du destinataire dans le document pour qu'elle soit remplacée automatiquement.  
    - 🏭 **XXN** à l'emplacement du nom du destinataire dans le document pour qu'il soit remplacé automatiquement.  
    - 📪 **XXA** à l'emplacement de l'adresse postale du destinataire dans le document pour qu'elle soit remplacée automatiquement.  
    - ☎️ **XXT** à l'emplacement du numéro de téléphone du destinataire dans le document pour qu'il soit remplacé automatiquement.  
    - 📅 **AJOUT** ℹ️ : **XXD** à l'emplacement de la date du jour dans le document pour qu'elle soit remplacée automatiquement (format : 10 janvier 2025).  

### Fichiers PDFs  
- Pour permettre l'export obligatoire au format PDF pour l'envoi des emails, LibreOffice Writer doit être installé afin de générer les fichiers.  
- Tous les fichiers à joindre à l'email doivent avoir pour extension `.pdf`.  

### Configuration pour l'envoi des emails  
- Adresses email d'envoi actuellement supportées par BotMail :  
    - Gmail  
    - Yahoo  
    - Outlook  

- Un code d'application est nécessaire pour que BotMail puisse utiliser l'adresse email de l'expéditeur.  
    - Gmail : [Documentation non-officielle ici](https://www.go-soft.ch/index.php/faq-generalites/136-creer-un-mot-de-passe-d-application-sur-google) ou [obtention du code sur site officiel ici](https://myaccount.google.com/apppasswords) (Situé dans le compte Google dans "Mots de passe des applications").
    - Yahoo : [Documentation officielle ici](https://fr.aide.yahoo.com/kb/G%C3%A9n%C3%A9rer-et-g%C3%A9rer-des-mots-de-passe-d%E2%80%99application-tierce-sln15241.html?guccounter=1)
    - Outlook : [Documentation officielle ici](https://support.microsoft.com/fr-fr/account-billing/cr%C3%A9er-des-mots-de-passe-d-application-%C3%A0-partir-de-la-page-informations-de-s%C3%A9curit%C3%A9-aper%C3%A7u-d8bc744a-ce3f-4d4d-89c9-eb38ab9d4137)

- **Pour la version BotMail sur Terminal uniquement**, un fichier ayant pour extension `.txt` doit être créé et utilisé pour contenir le corps de l'email.

## Partie développeurs
<!-- ### Constantes à définir pour l'utilisation du mode terminal
#### Fichier Excel/Calc
- FILE_SHEET_PATH : Le chemin d'accès vers un fichier ".csv" respectant la configuration nécessaire.
    ``` Python
    r"path/to/Adresses.csv"
    ```

#### Document Word/Writer
- MOTIVATION_LETTER_PATH : Le chemin d'accès vers la lettre de motivation ".docx" respectant la configuration nécessaire.
    ``` Python
    r"path/to/Lettre de Motivation.docx"
    ```

- MOTIVATION_LETTER_PATH_FINAL : La définition du nom de la lettre de motivation modifiée ".docx" respectant la configuration nécessaire.
    ``` Python
    r"Lettre de Motivation Finale.docx"
    ```

#### Documents PDF
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

#### Partie Email
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
    ``` -->

## En cours de développement
- Développement de la partie Interface Homme-Machine pour des personnes non initiées.

## Améliorations futures
- [ ] Rendre la lecture des fichiers CSV plus flexible (en supprimant la sensibilité à la casse). → Mise à jour vers la librairie [Pandas](https://pypi.org/project/pandas/) envisagée.
- [ ] Permettre la personnalisation du format de la date.
- [ ] Supprimer la nécessité d'installer LibreOffice Writer pour la génération des PDFs. → Mise à jour vers la librairie [FPDF](https://pyfpdf.github.io/fpdf2/) envisagée.
- [ ] Permettre d'envoyer des emails avec des pièces jointes autres que des fichiers PDF (par exemple, des documents `.docx`).

## Bugs trouvés