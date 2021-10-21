import json


class MailUtils:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 465 # For SSL

    def prepare_activation_code_message(self, username, activation_code):
        return "Hi, " + username + "\nThis is auto generated message from https://github.com/stiwenparker/.\nYour code is " + activation_code

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