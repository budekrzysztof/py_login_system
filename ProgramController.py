from Utilities import Utilities
from AccountHandler import AccountHandler


class ProgramController:
    def run(self):
        self.main_menu()

    def main_menu(self):
        choice = None

        while choice != 'exit':
            Utilities().display_main_menu()
            choice = input('> ').strip()

            if choice == 'login':
                AccountHandler().login()
            elif choice == 'register':
                AccountHandler().register()
            elif choice == 'exit':
                exit()
            else:
                print('try one of available commands: ')
                continue
