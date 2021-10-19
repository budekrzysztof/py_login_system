import sqlite3
from Utilities import Utilities
from MailHandler import MailHandler


class DatabaseHandler:
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
            for row in cur.execute('SELECT login, name, email FROM users ORDER BY id_number').fetchall():
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