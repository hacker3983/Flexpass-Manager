from auth import Auth
from manager import Manager
import getpass

banner = """\u001b[33m
███████╗██╗     ███████╗██╗  ██╗██████╗  █████╗ ███████╗███████╗
██╔════╝██║     ██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝
█████╗  ██║     █████╗   ╚███╔╝ ██████╔╝███████║███████╗███████╗
██╔══╝  ██║     ██╔══╝   ██╔██╗ ██╔═══╝ ██╔══██║╚════██║╚════██║
██║     ███████╗███████╗██╔╝ ██╗██║     ██║  ██║███████║███████║
╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                
███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗   
████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗  
██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝  
██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗  
██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║  
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝  
\u001b[0m"""

class Menu:
    def __init__(self):
        self.version = 0.1
        self.auth = Auth()
        self.manager = Manager(self.auth.username, self.auth.master_password)
        self.quit = False
        self.vault_options = [
                "Add a Credential",
                "View Credentials",
                "Delete Credentials",
                "Logout"
        ]

        self.startup_options = [
                "Create Account",
                "Login",
                "Exit"
        ]

    def start(self):
        while not self.quit:
            if not self.auth.logged_in:
                self.startup_menu()
            else:
                self.vault_menu()
        print("Exiting Flexpass Manager...")
        self.auth.write_data()

    def print_startup_menu(self):
        print("version:", self.version)
        for i, option in enumerate(self.startup_options):
            print(f"[{i+1}] {option}")

    def startup_menu(self):
        print(banner)
        self.print_startup_menu()
        option = int(input(f"Select an option (1-{len(self.startup_options)}): "))
        if option == 1:
            self.auth.signup()
        elif option == 2:
            self.auth.login()
            self.manager.username = self.auth.username
            self.manager.master_password = self.auth.master_password
        elif option == 3:
            self.quit = True

    def logout(self):
        self.auth.logged_in = False
        print(f"Logged out of the user {self.auth.username}!")

    def print_vaultmenu(self):
        print(f"Welcome, {self.auth.username}!")
        for i, option in enumerate(self.vault_options):
                print(f"[{i+1}] {option}")

    def vault_menu(self):
        while True:
            self.print_vaultmenu()
            option = int(input(f"Select an option (1-{len(self.vault_options)})> "))
            if option == 1:
                print(self.add_credential())
            elif option == 2:
                self.view_credentials()
            elif option == 3:
                self.delete_credentials()
            elif option == 4:
                self.logout()
                break

    def ask_credential(self):
        print("Please provide your credential details below...")
        platform_name = input("Enter the platform (Ex: Gmail): ")
        username = input("Enter the username: ")
        password = getpass.getpass("Enter the password: ")
        if password != getpass.getpass("confirm the password: "):
            return None
        return (platform_name, username, password)

    def add_credential(self):
        credential_details = self.ask_credential()
        platform_name, username, password = credential_details
        credential = self.manager.add_credential(platform_name,
                                    username, password)
        if credential:
            print("Successfully added the credential!")
        return credential

    def print_platforms(self):
        platforms = self.manager.get_platforms()
        for option, platform_name in enumerate(platforms):
            print(f"[{option+1}] {platform_name}")

    def print_credentials(self, platform_name):
        platform = self.manager.get_platform(platform_name)
        for i, username in enumerate(platform):
            print(f"[{i+1}] {username}")

    def view_credentials(self):
        platforms = self.manager.get_platforms()
        if not platforms:
            print("There is no credential for the current user...")
            return None
        platform_count = len(platforms)
        self.print_platforms()
        platform_id = int(input(f"Select a platform (1-{platform_count}): ")) - 1

        platform_name = self.manager.get_platform_name(platform_id)
        credentials = list(self.manager.get_platform(platform_name))
        credential_count = len(credentials)
        self.print_credentials(platform_name)
        credential_id = int(input(f"Select a credential (1-{credential_count}): ")) - 1

        credential_username = credentials[credential_id]
        credential_password = self.manager.retrieve_credential(platform_name, credential_id)
        print("Your credential is:")
        print(f"{credential_username} -> {credential_password}")
        return platforms

    def delete_credentials(self):
        platforms = self.manager.get_platforms()
        if not platforms:
            print("There is no credential for the current user...")
            return None
        platform_count = len(platforms)
        self.print_platforms()
        platform_id = int(input(f"Select a platform (1-{platform_count}): ")) - 1

        platform_name = self.manager.get_platform_name(platform_id)
        credentials = list(self.manager.get_platform(platform_name))
        credential_count = len(credentials)
        self.print_credentials(platform_name)
        credential_id = int(input(f"Select a credential (1-{credential_count}): ")) - 1

        credential_username = credentials[credential_id]
        removed = self.manager.remove_credential(platform_name, credential_id)
        if not removed:
            print("Failed to remove the credential...")
            return removed
        print("Successfully removed the credential!")
        print(f"Removed: {credential_username}")
        return removed



















