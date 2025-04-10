from Constants import CONFIGURATION_STMP

from validate_email import validate_email

class EmailUtils_Model:
    def __init__(self, emailSender : str = ""):
        self.emailSender = emailSender


    def set_email_sender(self, emailSender: str):
        if self.is_email_valid:
            self.emailSender = emailSender
        else:
            raise Exception(f"The email {emailSender} provided is not valid")


    def get_email_sender(self) -> str:
        return self.emailSender


    # Vérifie si l'email est syntaxiquement valide et la configuration STMP est supportée par l'application
    def is_email_valid(self, email: str) -> bool:
        return any(provider in email for provider in CONFIGURATION_STMP) and validate_email(email)


    def send_email(self, emailRecipient: list[str], subject: str, body: str):
        return False