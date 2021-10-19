import re, hashlib

from DatabaseHandler import DatabaseHandler
from DatabaseConnection import DatabaseConnection
from UserPanel import UserPanel

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