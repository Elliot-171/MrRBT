# FileGuard: Password-Based File Encryption

FileGuard is a Python-based utility that provides secure file encryption using AES-128 (via Fernet) and Scrypt for key derivation.
It ensures that even if two users choose the same password, their encryption keys will remain unique thanks to the use of a cryptographic salt.

## 🛡️ How It Works
The security of this tool relies on two main components

Scrypt KDF: Instead of using your password directly as a key, the tool "stretches" your password through the Scrypt Key Derivation Function. This makes "brute-force" attacks significantly slower and more difficult.

Fernet (AES): High-level symmetric encryption that ensures the file cannot be read or tampered with without the correct key.

## 🚀 Features
Password Privacy: Uses getpass to ensure your password is not visible in the terminal while typing.

Unique Salting: Automatically generates and manages a salt.salt file to protect against rainbow table attacks.

Integrity Checks: Fernet prevents the decryption of files if the data has been corrupted or modified.

## 📋 Prerequisites
1. Python 3.x

2. cryptography library

To install the required library, run :
```bash
pip install cryptography
```
## 🛠️ Usage
1. Encrypting a File
   To encrypt a file, use the -e flag. A new salt.salt file will be generated in your current directory.
   ```bash
   python file_tool.py my_data.txt -e
   ```
   You will be prompted to enter a password.
2. Decrypting a File
   To decrypt a file, use the -d flag.

   Ensure the salt.salt file generated during encryption is in the same folder.

   ```bash
   python file_tool.py my_data.txt -d
   ```
Enter the same password used during encryption.
3. Custom Salt Size

   For advanced users, you can specify the size of the salt (in bytes) during encryption:
   ```bash
   python file_tool.py my_data.txt -e -s 32
   ```
## ⚠️ Important Security Note
 Do not lose the salt.salt file.
 
 The encryption key is a combination of your password and the salt. If you lose the salt file or delete it, you will be unable to decrypt your files, even if you have the correct password.

