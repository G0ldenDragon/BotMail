import pandas as pd
from csv import DictReader
import Constants

# with open('test_documents/Adresses - Copy 2.csv', 'r', encoding='utf-8') as CSVFile:
#     donnees = DictReader(CSVFile, fieldnames = Constants.NOM_COLONNE, delimiter=';')
#
#     for ligne in donnees:
#         envoiePrecedent = ligne.get("envoiePrecedent")
#         nomEntreprise = ligne.get("nomEntreprise").rstrip()
#         emailEntreprise = ligne.get("emailEntreprise").lower().rstrip()
#         adresseEntreprise = ligne.get("adresseEntreprise")
#         telephoneEntreprise = ligne.get("telephoneEntreprise")
#         print(str(envoiePrecedent), str(nomEntreprise), str(emailEntreprise), str(adresseEntreprise), str(telephoneEntreprise))

df = pd.read_csv('../test_documents/Adresses - Copy 2.csv', sep=';', header=0)
lines = df.values.tolist()
print(df.loc[2, 'XXE'])

print("\n\n")

df = pd.read_excel('test_documents/Classeur1.ods', header=0)
lines = df.values.tolist()
print(lines)

print("\n\n")

df = pd.read_excel("test_documents/Adresses - Copy 2.xlsx", header=0)
lines = df.values.tolist()
print(lines)