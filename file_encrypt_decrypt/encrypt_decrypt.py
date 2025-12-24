import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import secrets
import base64
import getpass
import argparse
import os

def gen_salt(size=16):
    return secrets.token_bytes(size)

def dev_key(salt, password):
    # Fernet requires exactly 32 bytes for the key. 
    # Changed length from 64 to 32.
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def load_s():
    if not os.path.exists("salt.salt"):
        print("Error: 'salt.salt' file not found. You need this to decrypt.")
        exit()
    with open("salt.salt", "rb") as salt_f:
        return salt_f.read()

def gen_key(password, salt_size=16, load_e_salt=False, save_salt=True):
    if load_e_salt:
        salt = load_s()
    else:
        salt = gen_salt(salt_size)
        if save_salt:
            with open("salt.salt", "wb") as salt_f:
                salt_f.write(salt)

    d_key = dev_key(salt, password)
    return base64.urlsafe_b64encode(d_key)

def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as ff:
        file_dat = ff.read()

    encrypt_data = f.encrypt(file_dat)
    with open(filename, "wb") as ff:
        ff.write(encrypt_data)
    print(f"File '{filename}' encrypted successfully.")

def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as ff:
        encrypt_data = ff.read()

    try:
        decrypt_data = f.decrypt(encrypt_data)
        with open(filename, "wb") as ff:
            ff.write(decrypt_data)
        print(f"File '{filename}' decrypted successfully.")
    except cryptography.fernet.InvalidToken:
        print("Invalid token! Most likely the password or salt is incorrect.")

# --- CLI Setup ---
parser = argparse.ArgumentParser(description="File Encryption With Password")
parser.add_argument("file", help="File to encrypt/decrypt")
parser.add_argument("-s", "--salt-size", type=int, default=16, help="Set salt size (default 16)")
parser.add_argument("-e", "--encrypt", action="store_true", help="To encrypt file")
parser.add_argument("-d", "--decrypt", action="store_true", help="To decrypt the file")
args = parser.parse_args()

if args.encrypt and args.decrypt:
    print("Error: Please specify either --encrypt or --decrypt, not both.")
    exit()

if args.encrypt:
    password = getpass.getpass("Enter password for encryption: ")
    # When encrypting, we generate a new salt by default
    key = gen_key(password, salt_size=args.salt_size, save_salt=True)
    encrypt(args.file, key)

elif args.decrypt:
    password = getpass.getpass("Enter password used for encryption: ")
    # When decrypting, we MUST load the existing salt
    key = gen_key(password, load_e_salt=True)
    decrypt(args.file, key)

else:
    print("Please specify whether to encrypt (-e) or decrypt (-d).")
