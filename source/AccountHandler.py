from DatabaseHandler import DatabaseHandler
from DatabaseConnection import DatabaseConnection
from MailHandler import MailHandler
from UserPanel import UserPanel
from Utilities import Utilities

class AccountHandler:
    def login(self):
        username = input("username: ").strip()

        password = input("password: ").strip()
        password = Utilities().hash_password(password)

        """
        try to connect to database
        if succeeded open login panel
        else print error message and go back to menu
        """

        login_flag = False
        with DatabaseConnection() as connection:
            login_flag = DatabaseHandler().login_command(username, password, connection)

        if login_flag:
            print('login successful')
            UserPanel(username).run_user_panel()
        else:
            print('incorrect username or password')

    def register(self):
        # username validation
        username = input('username: ').strip()

        if not Utilities().is_username_valid(username):
            print('username must be between 6 and 30 characters and contain only alphanumeric characters')
            return

        with DatabaseConnection() as connection:
            if DatabaseHandler().does_username_exists_command(username, connection):
                print('user with that username already exists')
                return

        # name validation
        name = input("name: ").strip()
        if not Utilities().is_name_valid(name):
            print('name must be between 2 and 30 characters and contain only letters')
            return

        # password validation
        password = input("password: ").strip()
        if Utilities().is_strong_password(password):
            # if its valid hash it immediately
            password = Utilities().hash_password(password)
        else:
            print('password must contain 8 characters, both lower and uppercase letter, special sign and a number')
            return

        # repeat password and break if they don't match
        password_repeat = input("password again: ").strip()
        if not password == Utilities().hash_password(password_repeat):
            print('passwords do not match')
            return

        # need email validation here!!!
        email = input("email: ")

        activation_code = Utilities().generate_auth_code()
        # try to connect to database and insert new user
        with DatabaseConnection() as connection:
            if DatabaseHandler().add_user_command(username, name, password, email, connection):
                if DatabaseHandler().start_email_activation_command(username, activation_code, connection):
                    MailHandler().send_activation_code(username, activation_code, email)
                    print(f"successfully registered. activation code was send to {email}")
                    return
        print('something went wrong while trying to create an account. try again')




