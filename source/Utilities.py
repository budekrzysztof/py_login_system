from random import randint


class Utilities:
    def __init__(self):
        self.error_codes = {
            'ec_database_connection': "something went wrong while trying to access database",
            'ec_secure_password': "password does not meet secure password requirements.",
            'ec_pwd_match' : "passwords do not match",
            'ec_account_creation' : "something when wrong while trying to create and account",
            'ec_account_exists' : "username already exists",
            'ec_username_invalid' : "username is not between 6 and 30 characters or contains unrecognized characters",
            'ec_name_invalid' : "name must be between 3 and 26 characters and contain only letters",
            'ec_send_activation_mail' : "an error occurred while trying to send account activation email",
        }

    def generate_auth_code(self):
        return str(randint(103021, 983959))

    def display_main_menu(self):
        print("""
> login
> register
> exit
""")

    def display_user_panel(self):
        print("""
> play
> settings
> logout
> exit
""")

    def display_settings(self):
        print("""
1 > turn on two factor authentification (2FA)
2 > delete account
3 > back
""")