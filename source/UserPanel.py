from Utilities import Utilities
from DatabaseHandler import DatabaseHandler
from DatabaseConnection import DatabaseConnection
from MailHandler import MailHandler


class UserPanel:
    def __init__(self, username):
        self.username = username

    def run_user_panel(self):
        account_active = None
        active_2factor = None

        # check if account is active and if it has 2fa turned on
        with DatabaseConnection() as connection:
            account_active = DatabaseHandler().is_account_active_command(self.username, connection)
            active_2factor = DatabaseHandler().check_for_2fa(self.username, connection)

        if account_active:
            if active_2factor:
                print("your account has 2FA turned on. code was sent to your email address")
                with DatabaseConnection() as connection:
                    receiver_email = DatabaseHandler().get_mail_command(self.username, connection)
                    code = Utilities().generate_auth_code()

                    # if code was already sent let user input this code or let resend a new one
                    if DatabaseHandler().check_if_ac_was_already_send(self.username, connection):
                        print("code was already sent to your email")

                        resend_code = input('do you want to resend code? (yes) ').strip().lower()
                        if resend_code == 'yes':
                            DatabaseHandler().clear_ac_code(self.username, connection)
                            MailHandler().send_activation_code(self.username, code, receiver_email)
                            DatabaseHandler().start_email_activation_command(self.username, code, connection)
                            print("code was successfully resend")

                    # if it was not send before, send it now
                    else:
                        MailHandler().send_activation_code(self.username, code, receiver_email)
                        DatabaseHandler().start_email_activation_command(self.username, code, connection)

                    # input code
                    try_code = input('enter code from email: ').strip()

                    # check if its valid
                    if len(try_code) == 6 and try_code.isdigit() and DatabaseHandler().check_if_ac_is_valid(self.username, try_code, connection):
                        # if its valid delete it from db and let user proceed
                        DatabaseHandler().clear_ac_code(self.username, connection)
                        print('login successful')
                        self.run_user_menu()
                    else:
                        print('code was not correct')
            else:

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
                    if DatabaseHandler().account_activation_command(self.username, activation_code, connection):
                        print('account was successfully activated')
                        DatabaseHandler().clear_ac_code(self.username, connection)
                        self.run_user_menu()
                        break
                    else:
                        print("activation code was not correct")
            else:
                print("code should only contain 6 digits")
            choice = input('want to try again? ').lower()

    def settings(self):
        while True:
            Utilities().display_settings()
            choice = input('> ').strip()

            if choice == '1':
                print('you must confirm your password first.')
                pw = input('password: ').strip()
                pw = Utilities().hash_password(pw)

                with DatabaseConnection() as connection:
                    if DatabaseHandler().login_command(self.username, pw, connection):
                        flag_2fa = DatabaseHandler().check_for_2fa(self.username, connection)

                        if(flag_2fa):
                            if input('2FA: ON do you want to turn it off? (yes)\n').strip() == 'yes':
                                if DatabaseHandler().set_2fa_command(self.username, 'off', connection):
                                    print('2FA was successfully turned off')
                                    break
                        else:
                            if input('2FA: OFF do you want to turn it on? (yes)\n').strip() == 'yes':
                                if DatabaseHandler().set_2fa_command(self.username, 'on', connection):
                                    print('2FA was successfully turned on')
                                    break
                        print('something went wrong while trying to change 2FA options')
                    else:
                        print('you have entered wrong password')

            elif choice == '2':
                print('you must enter your current password first.')
                cur_pw = input('password: ').strip()
                cur_pw = Utilities().hash_password(cur_pw)

                with DatabaseConnection() as connection:
                    if DatabaseHandler().login_command(self.username, cur_pw, connection):
                        new_pw = input('now enter new password: ').strip()
                        if Utilities().is_strong_password(new_pw):
                            repeat_new_pw = input('repeat new password: ').strip()
                            if new_pw == repeat_new_pw:
                                new_pw = Utilities().hash_password(new_pw)
                                if DatabaseHandler().change_password_command(self.username, new_pw, connection):
                                    print('password changed successfully')
                                    break
                                else:
                                    print('something went wrong while trying to change password')
                            else:
                                print('passwords do not match')
                        else:
                            print('password must contain 8 characters, both lower and uppercase letter, special sign and a number')
                    else:
                        print('you have entered wrong password')

            elif choice == '3':
                print('you must enter your current password first.')
                pw = input('password: ').strip()
                pw = Utilities().hash_password(pw)

                with DatabaseConnection() as connection:
                    if DatabaseHandler().login_command(self.username, pw, connection):
                        new_email = input('enter new email address: ').strip()
                        # validate email address here!

                        repeat_new_email = input('repeat your new email address: ').strip()
                        if new_email == repeat_new_email:
                            activation_code = Utilities().generate_auth_code()
                            if DatabaseHandler().start_email_activation_command(self.username, activation_code, connection):
                                MailHandler().send_activation_code(self.username, activation_code, new_email)
                                print('confirmation code was sent to your new email address')
                                incorrect_attempts = 0
                                while(True):
                                    code = input('confirmation code: ')
                                    if activation_code == code:
                                        if DatabaseHandler().change_email_command(self.username, new_email, connection):
                                            DatabaseHandler().clear_ac_code(self.username, connection)
                                            print('email address was changed')
                                            break
                                    else:
                                        incorrect_attempts += 1
                                        if incorrect_attempts >= 3:
                                            print('you entered wrong code too many times')
                                            DatabaseHandler().clear_ac_code(self.username, connection)
                                            break
                                        print('confirmation code was not correct')
                                        decision = input('do you want to try again? (yes) ')
                                        if decision == 'yes':
                                            continue
                                        else:
                                            DatabaseHandler().clear_ac_code(self.username, connection)
                                            break

                            else:
                                print("something went wrong while trying to send activation code")
                        else:
                            print('emails do not match')
                    else:
                        print('you have entered wrong password')
            elif choice == '4':
                print("here you will be able to delete your account")
            elif choice == '5' or 'back':
                break
            else:
                print('try one of available commands: ')