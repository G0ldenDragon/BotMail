# TerminalUtils.py

from pathlib import Path


SCRIPT_NAME = "utilities"


def file_name(chemin):
    return Path(chemin).name

# ---------------------------------------
# Choix de l'utilisateur
def user_confirmation(messageInput: str, userConfirmation: list[str]) -> int:
    userInput = ""

    for index, choix in enumerate(userConfirmation):
        messageInput += f'{index+1}) {choix}\n'

    messageInput += '-> '

    while True:
        userInput = input(messageInput)
        print("")
        if userInput in userConfirmation:
            index = userConfirmation.index(userInput)
            return index
