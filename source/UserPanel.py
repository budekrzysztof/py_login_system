from Utilities import Utilities
from DatabaseHandler import DatabaseHandler
from DatabaseConnection import DatabaseConnection


class UserPanel:
    def __init__(self, username):
        self.username = username

    def run_user_panel(self):
        account_active = None

        # check if account is active
        with DatabaseConnection() as connection:
            account_active = DatabaseHandler().is_account_active_command(self.username, connection)

        # if its active continue to user menu, go to activation process instead
        if account_active:
            self.run_user_menu()
        else:
            print('in order to login you must activate your account')
            self.account_activation()

    def run_user_menu(self):
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

    def account_activation(self):
        choice = 'yes'
        while choice == 'yes':
            activation_code = input('enter the activation code that was sent your email address: ').strip()
            if len(activation_code) == 6 and activation_code.isdigit():
                success_flag = False

                # try to activate an account and proceed to menu if succeeded
                with DatabaseConnection() as connection:
                    success_flag = DatabaseHandler().account_activation_command(self.username, activation_code, connection)

                if success_flag:
                    print('account was successfully activated')
                    self.run_user_menu()
                    break
                else:
                    # here will be an option to resend an activation code (but only every one minute)
                    print("activation code was not correct")
            else:
                print("code should only contain 6 digits")
            choice = input('want to try again? ').lower()

    def settings(self):
        while True:
            Utilities().display_settings()
            choice = input('> ').strip()

            if choice == '1':
                print("here you will be able to turn on 2FA")
            elif choice == '2':
                print("here you will be able to delete your account")
            elif choice == '3' or 'back':
                break
            else:
                print('try one of available commands: ')
                continue