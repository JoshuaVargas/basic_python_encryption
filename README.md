# Basic Python Encryption/Decryption

At the root of ransomware is encryption and decryption. Threat actors encrypt a victim's data and hold it for ransom in hopes of a payout. Victims of ransomware, on the other hand, hope for their files to be decrypted after paying up.  

Below is a breakdown of how simple, at its core, file encryption and decryption can be.

## Generating a list of files to encrypt/decrypt

By utilizing python's built-in ```os``` module to access operating system dependent functionality, creating a list is as simple as importing the module and looping through a list of files and directories in either the current or specified directory. Due to the current limitations of this program, it's important to note that certain files will require exclusion (e.g. encrypt.py, decrypt.py, and key.key).

```py
import os

file_list = []

def generate_file_list():
    for file in os.listdir():
            if file == "encrypt.py" or file == "key.key" or file == "decrypt.py":
                continue
            if os.path.isfile(file):
                file_list.append(file)
```
The above snippet of code defines a function which generates a file list by looping through the objects in the directory that the program was run in and appending any files found to the ```file_list``` variable.

Given the scope of this program, it's important to note that a check must be done for whether an object in a given directory is a file or another directory itself before adding it to the file list (further study should include how to handle walking up and down directories to encrypt/decrypt their contents).

## Encrypting a list of files

This project makes use of pyca's ```cryptography``` package to encrypt files. For official documentation, visit their **[website](https://cryptography.io)**. You can install ```cryptography``` with:

```
$ pip install cryptography
```

For complete installation instructions, read their **[docs](https://cryptography.io/en/latest/installation/)**.

The ```cryptography``` package makes use of symmetric encryption, so you only have to generate a single key. Doing so requires importing ```Fernet``` from ```cryptography.fernet```. This program begins by generating a key and storing it in a key file in the current directory. While this isn't a secure method of storing a key, it works for the project's purposes.

```py
from cryptography.fernet import Fernet

def generate_encryption_key():
    key = Fernet.generate_key()

    key_file = open("key.key", "wb")
    key_file.write(key)
    key_file.close()

```

Before any encryption occurs, however, it's important to check that you have a key, and doing so is simple with the ```os``` module.

```py
key_path = "./key.key"

def check_key():
    return os.path.isfile(key_path)
```

File encryption requires reading from and writing to files. We can start with creating a ```Fernet``` object to encrypt the files themselves and then looping through our file list, reading their contents, storing their contents in a variable, encrypting the variable, and overwriting the file's contents with the newly encrypted data (it's important to close the files that you open in order to free the file for any further operations you might perform on them).

```py
def encrypt_files():
    key_file = open("key.key", "rb")
    f = Fernet(key_file.read())
    key_file.close

    for file in file_list:
        file_to_encrypt = open(file, "rb")
        file_contents = file_to_encrypt.read()
        file_to_encrypt.close
        file_to_encrypt = open(file, "wb")
        file_to_encrypt.write(f.encrypt(file_contents))
        file_to_encrypt.close
```

## Putting the encryption program together

The program itself is simple and simply generates a file list, checks whether the key exists or not, and encrypts the files if there is no previously generated key (this is a simple way of preventing multiple rounds of encryption).

```py
generate_file_list()

if check_key():
    print("Key already found.")
    print("Files previously encrypted.")
else:
    print("Key not found.")
    generate_encryption_key()
    encrypt_files()
```
## A quick note on file decryption

Decryption utilizes the same key, so generating a new key isn't required. However, checking that a key exists is, so the decryption program is nearly identical to the encryption program. A simple switch from ```f.encrypt``` to ```f.decrypt``` will get the job done.

The program itself is just as simple as the encryption program. The major difference is deleting the key once the files have been decrypted (simply for demo purposes).

```py
generate_file_list()

if check_key():
    print("Key found.")
    decrypt_files()
    os.remove(key_path)
    print("Key destroyed.")
else:
    print("Key not found.")
    print("Cannot decrypt without key.")
```

## Further developments

This isn't the way to encrypt your files safely. Ensuring that you're properly storing your key is paramount to keeping your files' confidentiality and integrity secure. Further study needs to go into properly storing the key. Just as important is trying to determine whether or not something was previously encrypted in order to prevent unwanted encryption.