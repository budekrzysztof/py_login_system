import smtplib, ssl, json

from email.utils import parseaddr
from email.message import EmailMessage


class MailHandler:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 465 # For SSL

    def prepare_activation_code_message(self, username, activation_code):
        return "Hi, " + username + "\nThis is auto generated message from https://github.com/stiwenparker/.\nYour activation code is " + activation_code

    def send_activation_code(self, username, code, receiver_email):
        message = EmailMessage()
        message.set_content(self.prepare_activation_code_message(username, code))

        message['Subject'] = 'Account activation stiwenparker'
        message['From'] = self.get_mail_config()['sender_address']
        message['To'] = receiver_email
        password = self.get_mail_config()['password']

        # Create a secure SSL context
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(message['From'], password)
            server.send_message(message)

    def get_mail_config(self):
        """
        here it needs to locate settings.json containing
        {
        "sender_address" : "server email address",
        "password" : "password to servers email"
        }
        """
        with open("../../source/settings.json", "r") as jsonfile:
            return json.load(jsonfile)