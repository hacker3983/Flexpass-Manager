from auth import Auth
from manager import Manager
import getpass

white = "\033[38;2;255;255;255m"
red = "\033[31m"
bold = "\033[1m"
green = "\033[38;2;;255;m"
yellow = "\033[38;2;255;255;m"
reset = "\033[0m"

banner = f"""{yellow}
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
{reset}"""

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
                "Switch Account",
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
        print(f"{yellow}version{reset}:{bold}{red} {self.version}\n{reset}")
        for i, option in enumerate(self.startup_options):
            print(f"{green}[{yellow}{i+1}{green}]", end="")
            print(f"{white} {option}{reset}")
        print()

    def startup_menu(self):
        print(banner)
        self.print_startup_menu()
        option = None
        try:
            option = int(input(f"{white}Select an option ({bold}{red}1-{len(self.startup_options)}{white})> "))
        except:
            print("The option that you gave is invalid please try again!")
            return
        if option == 1:
            self.auth.signup()
        elif option == 2:
            self.auth.login()
            self.manager.username = self.auth.username
            self.manager.master_password = self.auth.master_password
        elif option == 3:
            self.quit = True
        else:
            print("The option that you gave is invalid please try again!")

    def logout(self):
        self.auth.logged_in = False
        print(f"Logged out of the user {self.auth.username}!")

    def print_vaultmenu(self):
        print(banner)
        print(f"Welcome, {self.auth.username}!")
        for i, option in enumerate(self.vault_options):
            print(f"{green}[{yellow}{i+1}{green}]{white} {option}{reset}")
        print()

    def vault_menu(self):
        while True:
            self.print_vaultmenu()
            option = input(f"{white}Select an option ({bold}{red}1-{len(self.vault_options)}{white})> ")
            try:
                option = int(option)
            except:
                print("The option you entered is invalid please try again...")
                continue
            if option == 1:
                print(self.add_credential())
            elif option == 2:
                self.view_credentials()
            elif option == 3:
                self.delete_credentials()
            elif option == 4:
                self.logout()
                self.auth.login()
                print(f"{bold}{white}Successfully switched into account!")
            elif option == 5:
                self.logout()
                break

    def ask_credential(self):
        print("Please provide your credential details below...")
        platform_name = None
        username = None
        password = None
        while True:
            platform_name = input("Enter the platform (Ex: Gmail): ")
            if input("Enter the platform name again: ") == platform_name:
                break
            print("The platform name you have provided does not match...")
            print("Please try again...")

        while True:
            username = input("Enter the username: ")
            if input("Confirm you username: ") == username:
                break
            print("The username you entered does not match...")
            print("Please try again...")
        while True:
            password = getpass.getpass("Enter the password: ")
            if password == getpass.getpass("confirm the password: "):
                break
            print("The password that you have entered does not match...")
            print("Please try again...")
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
            print(f"{bold}{green}[{yellow}{option+1}{green}]{white} {platform_name}{reset}")

    def print_credentials(self, platform_name):
        platform = self.manager.get_platform(platform_name)
        for i, username in enumerate(platform):
            print(f"{bold}{green}[{yellow}{i+1}{green}]{white} {username}{reset}")

    def view_credentials(self):
        platforms = self.manager.get_platforms()
        if not platforms:
            print("There is no credential for the current user...")
            return None
        platform_count = len(platforms)
        while True:
            self.print_platforms()
            print("Type back to go back to the main menu...")
            platform_id = input(f"{white}Select a platform ({bold}{red}1-{platform_count}{white}): ")
            if platform_id == "back":
                break
            try:
                platform_id = int(platform_id) - 1
            except:
                print("The platform id provided is invalid...")
                print("Please try again...")
                continue
            if platform_id >= platform_count or platform_id < 0:
                print("The platform id provided is invalid...")
                print("Please try again..")
                continue
            print(platform_id)
            platform_name = self.manager.get_platform_name(platform_id)
            credentials = list(self.manager.get_platform(platform_name))
            credential_count = len(credentials)
            while True:
                self.print_credentials(platform_name)
                print("Type back to go back to selecting a platform option...")
                credential_id = input(f"{white}Select a credential ({bold}{red}1-{credential_count}{white}): ")
                if credential_id == "back":
                    break
                try:
                    credential_id = int(credential_id) - 1
                except:
                    print("The credential id you entered is not valid...")
                    print("Please try again...")
                    continue
                if credential_id >= credential_count or credential_id < 0:
                    print("The credential id you entered is invalid...")
                    print("Please try again...")
                    continue
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
        while True:
            self.print_platforms()
            print("Type back to go back to the main menu")
            platform_id = input(f"{white}Select a platform ({bold}{red}1-{platform_count}{white}): ")
            if platform_id == "back":
                return None
            try:
                platform_id = int(platform_id) - 1
            except:
                print("The platform id entered is invalid...")
                print("Please try again...")
                continue
            if platform_id >= platform_count or platform_id < 0:
                print("The platform id is invalid...")
                print("Please try again...")
                continue
            platform_name = self.manager.get_platform_name(platform_id)
            credentials = list(self.manager.get_platform(platform_name))
            credential_count = len(credentials)
            while True:
                self.print_credentials(platform_name)
                print("Type back to go back to platform selection")
                credential_id = input(f"{white}Select a credential ({bold}{red}1-{credential_count}{white}): ")
                if credential_id == "back":
                    break
                try:
                    credential_id = int(credential_id) - 1
                except:
                    print("The credential id is invalid...")
                    print("Please try again...")
                    continue
                if credential_id >= credential_count or credential_id < 0:
                    print("The credential id is invalid...")
                    print("Please try again...")
                    continue

                credential_username = credentials[credential_id]
                removed = self.manager.remove_credential(platform_name, credential_id)
                if not removed:
                    print("Failed to remove the credential...")
                    continue
                print("Successfully removed the credential!")
                print(f"Removed: {credential_username}")
                credentials = self.manager.get_platform(platform_name)
                if len(credentials) == 0:
                    break

