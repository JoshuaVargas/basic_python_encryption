import os
from cryptography.fernet import Fernet

file_list = []
key_path = "./key.key"

def generate_file_list():
    for file in os.listdir():
            if file == "encrypt.py" or file == "key.key" or file == "decrypt.py":
                continue
            if os.path.isfile(file):
                file_list.append(file)

def check_key():
    return os.path.isfile(key_path)

def decrypt_files():
    key_file = open("key.key", "rb")
    f = Fernet(key_file.read())
    key_file.close

    print("Decrypting files.")

    for file in file_list:
        file_to_decrypt = open(file, "rb")
        file_contents = file_to_decrypt.read()
        file_to_decrypt.close
        file_to_decrypt = open(file, "wb")
        file_to_decrypt.write(f.decrypt(file_contents))
        file_to_decrypt.close
    print("Files decrypted.")

generate_file_list()

if check_key():
    print("Key found.")
    decrypt_files()
    os.remove(key_path)
    print("Key destroyed.")
else:
    print("Key not found.")
    print("Cannot decrypt without key.")