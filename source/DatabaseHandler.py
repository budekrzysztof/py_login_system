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
            print(Utilities().error_codes['ec_database_connection'])
        return False

    def display_users_command(self, connection):
        try:
            cur = connection.cursor()
            print("users: ")
            for row in cur.execute('SELECT login, name, email FROM users ORDER BY id_number').fetchall():
                print(row)
        except:
            print(Utilities().error_codes['ec_database_connection'])

    def does_username_exists_command(self, username, connection): # return true if such account exists
        valid_flag = False
        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT login FROM users').fetchall():
                if un[0] == username:
                    valid_flag = True
                    break
        except:
            print(Utilities().error_codes['ec_database_connection'])
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
            print(Utilities().error_codes['ec_database_connection'])
        return success_flag

    def start_email_activation_command(self, username, email, connection):
        try:
            activation_code = Utilities().generate_auth_code()
            cur = connection.cursor()
            cur.execute("INSERT INTO user_activation_codes(username, code) VALUES (?, ?)", (username, activation_code))
            connection.commit()
            MailHandler().send_activation_code(username, activation_code, email)
        except:
            print(Utilities().error_codes['ec_send_activation_mail'])

    def is_account_active(self, username, connection):
        active_flag = False
        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT login, status FROM users').fetchall():
                if un[0] == username and un[1] == 'active':
                    active_flag = True
                    break
        except:
            print(Utilities().error_codes['ec_database_connection'])
        return active_flag

    def account_activation(self, username, activation_code, connection):
        success_flag = False

        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT username, code FROM user_activation_codes').fetchall():
                 if un[0] == username and un[1] == int(activation_code):
                    success_flag = True
            if success_flag == True:
                cur.execute('DELETE FROM user_activation_codes WHERE username=?', (username,))
                cur.execute("UPDATE users SET status='active' WHERE login=?", (username,))
                connection.commit()
        except sqlite3.Error as error:
            print(f"error code: {error}")

        return success_flag


