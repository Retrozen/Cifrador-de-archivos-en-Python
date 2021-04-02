import os
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Hash import SHA512
from Crypto import Random
from Crypto.Random import get_random_bytes

def Instructions():
    print("Welcome to the file encryptor!")
    print("Instructions:")
    print("1- Insert the name of the file + extension.")
    print("2- E to encrypt.")
    print("3- D to decrypt.")

# Cifrar
def Encrypt(key, filename):
    chunksize = 64 * 1024
    outputExtension = ".bin"
    outputFile = filename + outputExtension
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile: # Open file as read
        with open(outputFile, 'wb') as outfile: # Enable write 
            outfile.write(filesize.encode('UTF-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                
                outfile.write(encryptor.encrypt(chunk))

# Descifrar
def Decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = input("Output filename (Include extension): ")

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

# Contraseña
def getKey(password):
    hasher = SHA256.new(password.encode('UTF-8'))
    return hasher.digest()

def Main():
    Instructions()
    choice = input("Do you want to (E) encrypt or (D) decrypt?: ")

    if choice == "E":
        filename = input("File to encrypt: ")
        password = input("Password: ")
        Encrypt(getKey(password), filename)
        print("Done.")
        
    elif choice == "D":
        filename = input("File to decrypt: ")
        password = input("Password: ")
        
        Decrypt(getKey(password), filename)
        print("Done.")
        
    else:
        print("Incorrect option, closing ...")

if __name__ == '__main__':
    Main()
