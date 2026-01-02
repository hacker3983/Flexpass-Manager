import os
import json
import argon2
import getpass

class Auth():
    def __init__(self):
        self.hasher = argon2.PasswordHasher()
        self.auth_info = {
            "Users": {
            }
        }
        self.username = None
        self.master_password = None
        self.logged_in = False
        self.load_info()

    def welcome_screen(self):
        print("Welcome! It appears that this is your first time.")
        print("Let's get started with the setup...")

    def signup(self):
        self.welcome_screen()
        print(f"{'-' * 20}SIGNUP{'-' * 20}")
        username = input("Please enter your username: ")
        while True:
            master_password = getpass.getpass("Please enter your master password: ")
            if master_password != getpass.getpass("Please confirm your master password: "):
                print("Passwords do not match. Please try again...")
                continue
            self.add_user(username, master_password)
            self.write_data()
            break 
 
    def add_user(self, username, master_password):
        users = self.auth_info["Users"]
        if username in users:
            return False
        kdf_hash = self.hasher.hash(master_password)
        users.update({username: kdf_hash})
        return True

    def verify_password(self, kdf_hash, password):
        try:
            verified = self.hasher.verify(kdf_hash, password)
        except:
            verified = False
        return verified

    def login(self):
        attempts = 3
        users = self.auth_info["Users"]
        print(f"{'-' * 20}LOGIN{'-' * 20}")
        verified = False
        while attempts: 
            username = input("Please enter your username: ")
            if username in users:
                kdf_hash = users[username]
            master_password = getpass.getpass("Please enter your master password: ")
            verified = self.verify_password(kdf_hash, master_password)
            if verified:
                print("You have been authorized successfully!")
                self.username = username
                self.master_password = master_password
                self.logged_in = True
                break
            print("Incorrect username or password!")
            attempts -= 1
            print(f"You have {attempts} attempts left! Please try again...")
        if not attempts:
            print("You have exceeded the maximum number of attempts. You are not authorized to access the system...")
        return verified

    def load_info(self):
        if not os.path.isfile("auth.json"):
            return False
        with open("auth.json") as f:
            self.auth_info = json.loads(f.read())
        return True

    def write_data(self):
        with open("auth.json", "w") as f:
            users = self.auth_info["Users"]
            user_count = len(users)
            f.write("{\n")
            f.write('\t"Users":{\n')
            for index, user in enumerate(users):
                username = user
                kdf_hash = users[username]
                f.write(f'\t\t"{username}": "{kdf_hash}"')
                if index != user_count-1:
                    f.write(",\n")
            f.write('\n\t}\n')
            f.write("}")
