from Constants import CONFIGURATION_STMP

from validate_email import validate_email

class EmailGestionnary_Model:
    def __init__(self):
        self.emailSender = ""


    def set_email_sender(self, emailSender: str):
        if self.is_email_valid:
            self.emailSender = emailSender
        else:
            raise Exception(f"The email {emailSender} provided is not valid")


    def get_email_sender(self) -> str:
        return self.emailSender


    def is_email_valid(self, email: str) -> bool:
        for provider, config in CONFIGURATION_STMP.items():
            if provider in email:
               if validate_email(email):
                   return True

        return False


    # def send_email(self, email):