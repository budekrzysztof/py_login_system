import sqlite3
import hashlib
import smtplib, ssl
import re
import json

from random import randint
from email.utils import parseaddr
from email.message import EmailMessage


class Utilities:
    def __init__(self):
        """
        error_codes = {
            'secure_password': "password does not meet secure password requirements."

        }
        """

    def generate_auth_code(self):
        return str(randint(103021, 983959))

    def display_user_panel(self):
        print("""
> play
> settings
> logout
> exit
""")

    def display_main_menu(self):
        print("""
> login
> register
> exit
""")

    def display_settings(self):
        print("""
> login
> register
> exit
""")


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
        message['From'] = DatabaseHandler().get_mail_config()['sender_address']
        message['To'] = receiver_email
        password = DatabaseHandler().get_mail_config()['password']

        # Create a secure SSL context
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(message['From'], password)
            server.send_message(message)


class DatabaseHandler:
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

    def add_user_command(self, username, name, password, email, connection):
        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO users(login, name, password, email) VALUES (?, ?, ?, ?)", (username, name, password, email))
            connection.commit()
            return True
        except:
            return False

    def display_users_command(self, connection):
        try:
            cur = connection.cursor()
            print("users: ")
            for row in cur.execute('SELECT login, name, email FROM users ORDER BY id_number'):
                print(row)
        except:
            print("an error occurred while trying to display all users")

    def does_username_exists_command(self, username, connection): # return true if such account exists
        valid_flag = False

        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT login FROM users').fetchall():
                if un[0] == username:
                    valid_flag = True
                    break
        except:
            print("an error occurred while trying to check if username exists")

        return valid_flag

    def login_command(self, username, password, connection):
        success_flag = False

        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT login, password FROM users').fetchall():
                if un[0] == username and un[1] == password:
                    success_flag = True
                    break
        except:
            print("error occurred while trying to login an user")

        return success_flag

    def start_email_activation_command(self, username, email, connection):
        try:
            activation_code = Utilities().generate_auth_code()
            cur = connection.cursor()
            cur.execute("INSERT INTO user_activation_codes(username, code) VALUES (?, ?)", (username, activation_code))
            connection.commit()
            MailHandler().send_activation_code(username, activation_code, email)
        except:
            print("an error occurred while trying to send account activation email")

class DatabaseConnection:
    def __enter__(self):
        self.con = sqlite3.connect('../../source/database/database.db')
        return self.con

    def __exit__(self, *args):
        self.con.close()



class UserPanel:
    def __init__(self, username):
        self.username = username

    def run_user_panel(self):
        while True:
            Utilities().display_user_panel()
            choice = input('> ').strip()

            if choice == 'play':
                print('nothing here yet')
            elif choice == 'settings':
                self.settings()
            elif choice == 'logout':
                break
            elif choice == "exit":
                exit()
            else:
                print('try one of available commands: ')
                continue

    def settings(self):
        pass


class AccountHandler:
    def __init__(self):
        self.salt = "pierd" # <- should be randomly generated

    def login(self):
        username = input("username: ").strip()
        password = input("password: ").strip()
        # convert password to its hash using given salt
        password = hashlib.sha512((password + self.salt).encode()).hexdigest()

        """
        try to connect to database
        if succeeded open login panel
        else print error message and go back to menu
        """
        with DatabaseConnection() as connection:
            if DatabaseHandler().login_command(username, password, connection):
                print("login successful")
                UserPanel(username).run_user_panel()
            else:
                print("incorrect username or password")

    def register(self):
        # username input - break if username already exists or its invalid (not enough/too many or unrecognized characters)
        username = input("username: ").strip()

        if not self.is_username_valid(username):
            print("username is not between 6 and 30 characters.")
            return

        with DatabaseConnection() as connection:
            if DatabaseHandler().does_username_exists_command(username, connection):
                print("username already exists")
                return

        # input for a name which needs more validation too!
        name = input("name: ").strip()
        if not 2 < len(name) < 27:
            print("enter a name between 3 and 26 characters.")
            return

        # password input - break if password does not cover requirements for strong password
        password = input("password: ").strip()
        if self.is_strong_password(password):
            password = hashlib.sha512((password + self.salt).encode()).hexdigest()
        else:
            print("password does not meet secure password requirements.")
            return

        # repeat password and break if they don't match
        password_repeat = input("password again: ").strip()
        if not password == hashlib.sha512((password_repeat + self.salt).encode()).hexdigest():
            print("passwords do not match.")
            return

        # need email validation here!!!
        email = input("email: ")

        # try to connect to database and insert new user
        with DatabaseConnection() as connection:
            try:
                DatabaseHandler().add_user_command(username, name, password, email, connection)
                DatabaseHandler().start_email_activation_command(username, email, connection)
                print(f"successfully registered. activation code was send to {email}")
            except:
                print("something when wrong while trying to create and account")

    def is_strong_password(self, password) ->bool:
        return re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?:.{8,})$').search(password)

    def is_username_valid(self, username) ->bool:
        valid_flag = False

        # need more validation for username
        if 5 < len(username) < 31:
            valid_flag = True

        return valid_flag


class ProgramController:
    def run(self):
        self.main_menu()

    def main_menu(self):
        choice = None

        while choice != 'exit':
            Utilities().display_main_menu()
            choice = input('> ').strip()

            if choice == 'login':
                AccountHandler().login()
            elif choice == 'register':
                AccountHandler().register()
            elif choice == 'exit':
                exit()
            else:
                print('try one of available commands: ')
                continue


if __name__ == '__main__':
    ProgramController().run()
