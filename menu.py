from auth import Auth
from manager import Manager
from enum import IntEnum
import getpass
import platform
import os

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

platform_offset = 0
platform_limit = 10

credential_offset = 0
credential_limit = 10

class StartupOption(IntEnum):
    CREATE_ACCOUNT = 1
    LOGIN = 2,
    CLEAR = 3
    EXIT = 4

class VaultOption(IntEnum):
    ADD_CREDENTIAL = 1
    VIEW_CREDENTIALS = 2
    DELETE_CREDENTIALS = 3
    SWITCH_ACCOUNT = 4
    ADD_PLATFORM = 5
    REMOVE_ACCOUNT = 6
    CHANGE_USERNAME = 7
    REMOVE_PLATFORM = 8
    CHANGE_PASSWORD = 9
    CLEAR = 10
    EDIT_PLATFORM = 11
    EDIT_CREDENTIAL = 12
    LOGOUT = 13

class Menu:
    def __init__(self):
        self.version = 0.2
        self.auth = Auth()
        self.manager = Manager(self.auth.username, self.auth.master_password)
        self.quit = False
        self.vault_options = {
                VaultOption.ADD_CREDENTIAL: "Add a Credential",
                VaultOption.VIEW_CREDENTIALS: "View Credentials",
                VaultOption.DELETE_CREDENTIALS: "Delete Credentials",
                VaultOption.SWITCH_ACCOUNT: "Switch Account",
                VaultOption.REMOVE_ACCOUNT: "Remove Account",
                VaultOption.CHANGE_USERNAME: "Change Username",
                VaultOption.REMOVE_PLATFORM: "Remove platform",
                VaultOption.CHANGE_PASSWORD: "Change master password",
                VaultOption.LOGOUT: "Logout",
                VaultOption.ADD_PLATFORM: "Add platform",
                VaultOption.CLEAR: "Clear the screen",
                VaultOption.EDIT_PLATFORM: "Edit the name of a platform",
                VaultOption.EDIT_CREDENTIAL: "Edit the name of a credential"
        }

        self.startup_options = {
                StartupOption.CREATE_ACCOUNT: "Create Account",
                StartupOption.LOGIN: "Login",
                StartupOption.EXIT: "Exit",
                StartupOption.CLEAR: "Clear the screen"
        }

    def clear_screen(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def start(self):
        while not self.quit:
            if not self.auth.logged_in:
                self.startup_menu()
            else:
                self.vault_menu()
        print("Exiting Flexpass Manager...")
        self.auth.write_data()

    def print_startup_menu(self):
        option_list = sorted(self.startup_options)
        print(f"{yellow}version{reset}:{bold}{red} {self.version}\n{reset}")
        for option in option_list:
            option_name = self.startup_options[option]
            print(f"{green}[{yellow}{option}{green}]", end="")
            print(f"{white} {option_name}{reset}")
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
        if option == StartupOption.CREATE_ACCOUNT:
            self.auth.signup()
        elif option == StartupOption.LOGIN:
            self.auth.login()
            self.manager.username = self.auth.username
            self.manager.master_password = self.auth.master_password
        elif option == StartupOption.CLEAR:
            self.clear_screen()
        elif option == StartupOption.EXIT:
            self.quit = True
        else:
            print("The option that you gave is invalid please try again!")
    
    def change_username(self):
        success = self.auth.change_username()
        if success:
            self.manager.change_username(self.auth.username)

    def remove_account(self):
        success = self.auth.remove_user()
        if success:
            self.manager.remove_user()
            self.logout()
        return success

    def edit_platforms(self):
        platforms = self.manager.get_platforms()
        if not platforms:
            print("There is no platforms the current user...")
            return
        platform_count = len(platforms)
        while True:
            self.print_platforms()
            platform_id = input(f"{white}Select a platform ({bold}{red}1-{platform_count}{white}): ")
            if platform_id == "home":
                self.reset_platform_offset()
                break
            elif platform_id == "clear":
                self.clear_screen()
                continue
            elif platform_id == "back":
                self.reset_platform_offset()
                break
            elif platform_id == "next":
                self.next_platform_page(platform_count)
                continue
            elif platform_id == "prev":
                self.prev_platform_page()
                continue
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
            new_platform_name = input("Enter the new name of the platform: ")
            if new_platform_name != input("Confrim the name of the platform: "):
                print("The platform name doesn't match please try again...")
                continue

            if self.manager.edit_platform(platform_id, new_platform_name):
                print("Succesfully edited the platform name!")
            else:
                print("The platform id you gave is invalid.")
                print("Please try again...")

    def edit_credentials(self):
        platforms = self.manager.get_platforms()
        if not platforms:
            print("There is no credential for the current user...")
            return None
        platform_count = len(platforms)
        while True:
            self.print_platforms()
            platform_id = input(f"{white}Select a platform ({bold}{red}1-{platform_count}{white}): ")
            if platform_id == "home":
                self.reset_platform_offset()
                break
            elif platform_id == "clear":
                self.clear_screen()
                continue
            elif platform_id == "back":
                self.reset_platform_offset()
                return None
            elif platform_id == "next":
                self.next_platform_page(platform_count)
                continue
            elif platform_id == "prev":
                self.prev_platform_page()
                continue

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
                if not credential_count:
                    print(f"{red}There is no credentials in the selected platform...")
                    break
                credential_id = input(f"{white}Select a credential ({bold}{red}1-{credential_count}{white}): ")
                if credential_id == "home":
                    self.reset_all_offsets()
                    return
                elif credential_id == "clear":
                    self.clear_screen()
                    continue
                elif credential_id == "back":
                    self.reset_credential_offset()
                    break
                elif credential_id == "next":
                    self.next_credential_page(credential_count)
                    continue
                elif credential_id == "prev":
                    self.prev_credential_page()
                    continue
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


                new_credential_name = input("Enter the new credential name: ")
                if new_credential_name != input("Confirm the credential name: "):
                    print("The credential name doesn't match!")
                    print("Please try again...")
                    continue
                credential_username = credentials[credential_id]
                edited = self.manager.edit_credential(platform_name, credential_id, new_credential_name)
                if not edited:
                    print("Failed to edit the credential...")
                    continue
                print("Successfully edited the credential!")
                print(f"Edited: {credential_username}")
                credentials = self.manager.get_platform(platform_name)
                if len(credentials) == 0:
                    break


    def remove_platform(self):
        platforms = self.manager.get_platforms()
        if not platforms:
            print("There is no platforms for the current user...")
            return
        platform_count = len(platforms)
        while True:
            if not platforms:
                break
            self.print_platforms()
            platform_id = input(f"{white}Select a platform ({bold}{red}1-{platform_count}{white}): ")
            if platform_id == "home":
                self.reset_platform_offset()
                break
            elif platform_id == "clear":
                self.clear_screen()
                continue
            elif platform_id == "back":
                self.reset_platform_offset()
                break
            elif platform_id == "next":
                self.next_platform_page(platform_count)
                continue
            elif platform_id == "prev":
                self.prev_platform_page()
                continue
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
            if self.manager.remove_platform(platform_id):
                print("Succesfully removed the platform!")
            else:
                print("The platform id you gave is invalid.")
                print("Please try again...")

    def logout(self):
        self.manager.write_data()
        self.auth.logged_in = False
        print(f"Logged out of the user {self.auth.username}!")

    def print_vaultmenu(self):
        option_list = sorted(self.vault_options)
        print(banner)
        print(f"Welcome, {self.auth.username}!")
        for option in option_list:
            option_name = self.vault_options[option]
            print(f"{green}[{yellow}{option}{green}]{white} {option_name}{reset}")
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
            if option == VaultOption.ADD_CREDENTIAL:
                self.add_credential()
            elif option == VaultOption.VIEW_CREDENTIALS:
                self.view_credentials()
            elif option == VaultOption.DELETE_CREDENTIALS:
                self.delete_credentials()
            elif option == VaultOption.SWITCH_ACCOUNT:
                self.switch_account()
            elif option == VaultOption.REMOVE_ACCOUNT:
                if self.remove_account():
                    break
            elif option == VaultOption.CHANGE_USERNAME:
                self.change_username()
            elif option == VaultOption.REMOVE_PLATFORM:
                self.remove_platform()
            elif option == VaultOption.CHANGE_PASSWORD:
                self.change_master_password()
            elif option == VaultOption.ADD_PLATFORM:
                self.add_platform()
            elif option == VaultOption.CLEAR:
                self.clear_screen()
            elif option == VaultOption.EDIT_PLATFORM:
                self.edit_platforms()
            elif option == VaultOption.EDIT_CREDENTIAL:
                self.edit_credentials()
            elif option == VaultOption.LOGOUT:
                self.logout()
                break

    def add_platform(self):
        platforms = self.manager.get_platforms()
        while True:
            platform_name = input("Enter the platform (Ex: Gmail): ")
            if platform_name in platforms:
                print("The platform already exists.")
                print("Please try again...")
                continue
            if input("Enter the platform name again: ") == platform_name:
                break
        if self.manager.add_platform(platform_name):
            print(f"{bold}{white}Successfully added the platform {platform_name}!")
            return True
        print(f"{bold}{white}Failed to add the platform {platform_name}!")
        return False

    def change_master_password(self):
        password = getpass.getpass("Please confirm your password: ")
        while True:
            new_password = getpass.getpass("Please enter the new password: ")
            if new_password == getpass.getpass("Confirm the password: "):
                break
            print("Please try again...")
        if self.auth.change_password(password, new_password):
            self.manager.change_password(password, new_password)
            print("Successfully changed the password!")
        else:
            print("The password is incorrect...")
            print("Please try again...")

    def switch_account(self):
        self.logout()
        logged_in = self.auth.login()
        if logged_in:
            self.manager.username = self.auth.username
            print(f"{bold}{white}Successfully switched into account!")
        else:
            print(f"{bold}{white}Failed to switch into the account...")
            self.auth.relogin()

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
            if input("Confirm your username: ") == username:
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
    
    def next_platform_page(self, platform_count):
        global platform_offset
        platform_end = platform_offset + platform_limit
        if platform_end < platform_count:
            platform_offset += platform_limit
    
    def prev_platform_page(self):
        global platform_offset
        if platform_offset > 0:
            platform_offset -= platform_limit

    def reset_platform_offset(self):
        global platform_offset
        platform_offset = 0

    def next_credential_page(self, credential_count):
        global credential_offset
        credential_end = credential_offset + credential_limit
        if credential_end < credential_count:
            credential_offset += credential_limit

    def prev_credential_page(self):
        global credential_offset
        if credential_offset > 0:
            credential_offset -= credential_limit

    def reset_credential_offset(self):
        global credential_offset
        credential_offset = 0

    def reset_all_offsets(self):
        self.reset_platform_offset()
        self.reset_credential_offset()

    def print_shortcuts(self):
        print(f"{bold}{white}Shortcuts:")
        print(f"1. Use {red}back{white} to go {red}back{white} to the main menu.")
        print(f"2. Use {red}next{white} to navigate to the {red}next{white} section.")
        print(f"3. Use {red}prev{white} to navigate to the {red}previous{white} section.")
        print(f"4. Use {red}home{white} to go back to the main menu.")
        print(f"5. Use {red}clear{white} to clear the screen.")
        print()

    def print_platforms(self):
        platforms = list(self.manager.get_platforms())
        platform_count = len(platforms)
        platform_end = platform_offset + platform_limit
        if platform_end > platform_count:
            platform_end = platform_count
        paginated_list = platforms[platform_offset:platform_end]
        print(f"{bold}{white}Displaying {platform_offset+1} to {platform_end} of {platform_count} platforms.")
        for option, platform_name in enumerate(paginated_list):
            option = platform_offset + option + 1
            print(f"{bold}{green}[{yellow}{option}{green}]{white} {platform_name}{reset}") 
        self.print_shortcuts()

    def print_credentials(self, platform_name):
        platform = list(self.manager.get_platform(platform_name))
        credential_count = len(platform)
        credential_end = credential_offset + credential_limit
        if credential_end > credential_count:
            credential_end = credential_count
        paginated_list = platform[credential_offset:credential_end]
        print(f"{bold}{white}Displaying {credential_offset+1} to {credential_end} of {credential_count} credentials.")
        for i, username in enumerate(paginated_list):
            i = credential_offset + i + 1
            print(f"{bold}{green}[{yellow}{i}{green}]{white} {username}{reset}")
        self.print_shortcuts()

    def view_credentials(self):
        platforms = self.manager.get_platforms()
        if not platforms:
            print("There is no credential for the current user...")
            return None
        platform_count = len(platforms)
        while True:
            self.print_platforms()
            platform_id = input(f"{white}Select a platform ({bold}{red}1-{platform_count}{white}): ")
            if platform_id == "home":
                self.reset_platform_offset()
                break
            elif platform_id == "clear":
                self.clear_screen()
                continue
            elif platform_id == "back":
                self.reset_platform_offset()
                break
            elif platform_id == "next":
                self.next_platform_page(platform_count)
                continue
            elif platform_id == "prev":
                self.prev_platform_page()
                continue
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
            platform_name = self.manager.get_platform_name(platform_id)
            credentials = list(self.manager.get_platform(platform_name))
            credential_count = len(credentials)
            if not credential_count:
                print("There are no credentials for the selected platform...")
            while True and credential_count > 0:
                self.print_credentials(platform_name)
                credential_id = input(f"{white}Select a credential ({bold}{red}1-{credential_count}{white}): ")
                if credential_id == "home":
                    self.reset_all_offsets()
                    return platforms
                elif credential_id == "clear":
                    self.clear_screen()
                    continue
                elif credential_id == "back":
                    self.reset_credential_offset()
                    break
                elif credential_id == "next":
                    self.next_credential_page(credential_count)
                    continue
                elif credential_id == "prev":
                    self.prev_credential_page()
                    continue
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
            platform_id = input(f"{white}Select a platform ({bold}{red}1-{platform_count}{white}): ")
            if platform_id == "home":
                self.reset_platform_offset()
                break
            elif platform_id == "clear":
                self.clear_screen()
                continue
            elif platform_id == "back":
                self.reset_platform_offset()
                return None
            elif platform_id == "next":
                self.next_platform_page(platform_count)
                continue
            elif platform_id == "prev":
                self.prev_platform_page()
                continue

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
                if not credential_count:
                    print(f"{red}There is no credentials in the selected platform...")
                    break
                credential_id = input(f"{white}Select a credential ({bold}{red}1-{credential_count}{white}): ")
                if credential_id == "home":
                    self.reset_all_offsets()
                    return
                elif credential_id == "clear":
                    self.clear_screen()
                    continue
                elif credential_id == "back":
                    self.reset_credential_offset()
                    break
                elif credential_id == "next":
                    self.next_credential_page(credential_count)
                    continue
                elif credential_id == "prev":
                    self.prev_credential_page()
                    continue
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

