# Encryption Process Diagram:
# Master Password -> Argon2 + salt -> AES KEY
# Credential -> AES KEY, iv (Initialization Vector) -> Ciphertext
# Store Salt, IV, Ciphertext as JSON Data
import os
import json
from argon2.low_level import hash_secret_raw, Type
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class Manager:
    def __init__(self, username, master_password):
        self.creds_info = {
                "Users": {
                }
        }
        self.username = username
        self.master_password = master_password
        self.load_info()

    def derive_aeskey(self, salt):
        return hash_secret_raw(
                secret=self.master_password.encode(),
                salt=salt,
                time_cost=3,
                memory_cost=65536,
                parallelism=4,
            hash_len=32,
                type=Type.ID
        )

    def encrypt_credential(self, credential):
        salt = os.urandom(16)
        aes_key = self.derive_aeskey(salt)
        aes = AES.new(aes_key, AES.MODE_CBC)
        ciphertext = aes.encrypt(pad(credential.encode(), AES.block_size))
        return {
                "salt": base64.b64encode(salt).decode(),
                "iv": base64.b64encode(aes.iv).decode(),
                "ciphertext": base64.b64encode(ciphertext).decode()
        }

    def decrypt_credential(self, encrypted_data):
        salt = base64.b64decode(encrypted_data["salt"])
        iv = base64.b64decode(encrypted_data["iv"])
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])

        aes_key = self.derive_aeskey(salt)
        aes = AES.new(aes_key, AES.MODE_CBC, iv=iv)
        decrypted_password = unpad(aes.decrypt(ciphertext), AES.block_size).decode()
        return decrypted_password

    def get_users(self):
        return self.creds_info["Users"]

    def get_user(self):
        users = self.get_users()
        return users.get(self.username)

    def add_user(self):
        user = {
                self.username: {
                    "Platforms": {}
                }
        }
        users = self.get_users()
        users.update(user)
        return user

    def add_platform(self, platform_name):
        user = self.get_user()
        platforms = user["Platforms"]
        if platform_name in platforms:
            return None
        platform = {platform_name:{}}
        platforms.update(platform)
        return platform
 
    def get_platforms(self):
        user = self.get_user()
        if not user:
            return None
        platforms = user["Platforms"]
        return platforms
    
    def get_platform_name(self, platform_id):
        platforms = list(self.get_platforms())
        return platforms[platform_id]

    def get_platform(self, platform_name):
        user = self.get_user()
        platforms = user["Platforms"]
        return platforms.get(platform_name)

    def add_credential(self, platform_name, credential_username, credential_password):
        user = self.get_user()
        if not user:
            user = self.add_user()
        self.add_platform(platform_name)
        platform = self.get_platform(platform_name)
        encrypted_data = self.encrypt_credential(credential_password)
        platform.update({credential_username:encrypted_data})
        self.write_data()
        return platform

    def remove_credential(self, platform_name, credential_id):
        user = self.get_user()
        if not user:
            return False
        platform = self.get_platform(platform_name)
        if not platform:
            return False
        for i, credential_username in enumerate(platform):
            if i == credential_id:
                del platform[credential_username]
                self.write_data()
                return True
        return False

    def retrieve_credential(self, platform_name, credential_id):
        user = self.get_user()
        if not user:
            return False
        platform = self.get_platform(platform_name)
        if not platform:
            return False
        for i, credential_username in enumerate(platform):
            if i == credential_id:
                encrypted_data = platform[credential_username]
                decrypted_data = self.decrypt_credential(encrypted_data)
                return decrypted_data

        return None
    
    def load_info(self):
        if not os.path.isfile("creds.json"):
            return False
        with open("creds.json") as f:
            self.creds_info = json.loads(f.read())
        return True

    def write_data(self):
        with open("creds.json", "w") as f:
            f.write(json.dumps(self.creds_info))
