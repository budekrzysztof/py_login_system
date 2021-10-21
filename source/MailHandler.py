import smtplib, ssl

from email.utils import parseaddr
from email.message import EmailMessage

from MailUtils import MailUtils
from Utilities import Utilities


class MailHandler:
    def send_activation_code(self, username, code, receiver_email):
        message = EmailMessage()
        message.set_content(MailUtils().prepare_activation_code_message(username, code))

        message['Subject'] = 'Account activation stiwenparker'
        message['From'] = MailUtils().get_mail_config()['sender_address']
        message['To'] = receiver_email
        password = MailUtils().get_mail_config()['password']

        # Create a secure SSL context
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(MailUtils().smtp_server, MailUtils().port, context=context) as server:
                server.login(message['From'], password)
                server.send_message(message)
        except:
            print(Utilities().error_codes['ec_send_ac'])




