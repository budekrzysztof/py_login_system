import sqlite3
from Utilities import Utilities


class DatabaseHandler:
    def add_user_command(self, username, name, password, email, connection):
        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO users(login, name, password, email) VALUES (?, ?, ?, ?)", (username, name, password, email))
            connection.commit()
            return True
        except:
            print('error occurred while trying to access database')
        return False

    def does_username_exists_command(self, username, connection): # return true if such account exists
        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT login FROM users').fetchall():
                if un[0] == username:
                    return True
        except:
            print('error occurred while trying to access database')
        return False

    def login_command(self, username, password, connection):
        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT login, password FROM users').fetchall():
                if un[0] == username and un[1] == password:
                    return True
        except:
            print('error occurred while trying to access database')
        return False

    def is_account_active_command(self, username, connection):
        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT login, status FROM users').fetchall():
                if un[0] == username and un[1] == 'active':
                    return True
        except:
            print('error occurred while trying to access database')
        return False

    def check_if_ac_is_valid(self, username, activation_code, connection):
        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT username, code FROM user_activation_codes').fetchall():
                if un[0] == username and un[1] == int(activation_code):
                    return True
        except:
            print('error occurred while trying to access database')
        return False

    def check_if_ac_was_already_send(self, username, connection):
        try:
            cur = connection.cursor()
            for un in cur.execute('SELECT username FROM user_activation_codes').fetchall():
                if un[0] == username:
                    return True
        except:
            print('error occurred while trying to access database')
        return False

    def account_activation_command(self, username, activation_code, connection):
        try:
            cur = connection.cursor()
            if self.check_if_ac_is_valid(username, activation_code, connection):
                cur.execute("UPDATE users SET status='active' WHERE login=?", (username,))
                connection.commit()
                return True
        except:
            print('error occurred while trying to access database')
        return False

    def check_for_2fa(self, username, connection):
        try:
            cur = connection.cursor()
            for row in cur.execute('SELECT login, two_factor FROM users').fetchall():
                if row[0] == username and row[1] == 'on':
                    return True
        except:
            print('error occurred while trying to access database')
        return False

    def change_password_command(self, username, password, connection):
        try:
            cur = connection.cursor()
            cur.execute("UPDATE users SET password=? WHERE login=?",(password, username))
            connection.commit()
            return True
        except:
            print('error occurred while trying to access database')
        return False

    def change_email_command(self, username, new_mail, connection):
        try:
            cur = connection.cursor()
            cur.execute('UPDATE users SET email=? WHERE login=?', (new_mail, username))
            connection.commit()
            return True
        except:
            print('error occurred while trying to access database')
        return False

    def set_2fa_command(self, username, decision, connection):
        try:
            cur = connection.cursor()
            cur.execute("UPDATE users SET two_factor=? WHERE login=?", (decision, username))
            connection.commit()
            return True
        except:
            print('error occurred while trying to access database')
        return False

    def get_mail_command(self, username, connection):
        try:
            cur = connection.cursor()
            for row in cur.execute('SELECT login, email FROM users').fetchall():
                if row[0] == username:
                    return row[1]
        except:
            print('error occurred while trying to access database')

    def start_email_activation_command(self, username, activation_code, connection):
        try:
            cur = connection.cursor()
            cur.execute("INSERT INTO user_activation_codes(username, code) VALUES (?, ?)", (username, activation_code))
            connection.commit()
            return True
        except:
            print('error occurred while trying to access database')
        return False

    def clear_ac_code(self, username, connection):
        try:
            cur = connection.cursor()
            cur.execute('DELETE FROM user_activation_codes WHERE username=?', (username,))
            connection.commit()
        except:
            print('error occurred while trying to access database')





