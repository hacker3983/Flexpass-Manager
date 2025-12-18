# Flexpass Manager
**Flexpass Manager** is a secure and extensible password manager written in Python. It enables users to encrypt, store, and manage credentials locally using strong cryptographic primitives. Encryption keys are derived from a master password using Argon2 and used with AES for secure data storage.

The project currently features a command-line interface, with plans to expand into a graphical user interface in future versions.
---

## Features

- Secure storage of passwords and credentials
- AES-encrypted vault (`creds.json`)
- Argon2-based master password key derivation
- Random, per-vault salts for maximum security
- Interactive CLI menu for managing credentials
- Offline-first design – all data stays on your machine
- Modular code structure for clean and maintainable design

---

## Installation

Clone the repo:

```bash
git clone https://github.com/hacker3983/Flexpass-Manager.git
cd Flexpass-Manager
```

Install dependencies:
```bash
python3 install.py
```


# Usage

Start Flexpass:

```bash
# Linux/macOS with launcher:
flexpass

# Windows or local run without launcher on Mac / Linux:
python3 flexpass.py
```

Once started, you will see an interactive menu with options such as:
1. Initialize your vault (first-time setup)
2. Add a new credential (service, username, password)
3. Retrieve a stored credential
4. List all stored credentials
5. Remove a credential
6. Exit the program

Navigate through the menu by typing the corresponding number and pressing Enter.

# Security Model
* The master password is never stored.
* A unique, random vault salt is generated per vault.
* The master password is used with Argon2 to derive:
    * Authentication verifier (stored in `auth.json` for login)
    * AES encryption key (used to encrypt/decrypt `creds.json`)
* Each password is encrypted with AES-CBC using:
    * AES key derived from master password + vault salt
    * Random IV generated per password
* IV (Initialization Vector) is stored in `creds.json`
* Salt and KDF parameters are stored in plaintext (they are configuration, not secrets)

# Contributing
Contributions are welcome! Open issues or pull requests to improve Flexpass Manager.
