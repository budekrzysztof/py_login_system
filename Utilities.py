from random import randint


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