from random import randint
import json, hashlib, re


class Utilities:
    def generate_auth_code(self):
        return str(randint(103021, 983959))

    def hash_password(self, password):
        return hashlib.sha512((password + self.get_salty()).encode()).hexdigest()

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
1 > two factor authentification
2 > change password
3 > change email address
4 > delete account
3 > back
""")

    # here locate settings.json too
    def get_salty(self):
         with open("database/settings.json", "r") as jsonfile:
            return json.load(jsonfile)['salt']

    def is_strong_password(self, password):
        return re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?:.{8,})$').search(password)

    def is_name_valid(self, name):
        valid_flag = False

        if name.isalpha() and 1 < len(name) < 31:
            return True

        return False

    def is_username_valid(self, username: str):
        valid_flag = False

        if 5 < len(username) < 31 and username.isalnum():
            valid_flag = True

        return valid_flag