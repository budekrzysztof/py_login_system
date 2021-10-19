from Utilities import Utilities


class UserPanel:
    def __init__(self, username):
        self.username = username

    def run_user_panel(self):
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

    def settings(self):
        while True:
            Utilities().display_settings()
            choice = input('> ').strip()