from cryptography.fernet import Fernet

# Run only for one time
# key = Fernet.generate_key()
# with open("secret.key", "wb") as f:
#     f.write(key) 

class Encryption:
    def __init__(self):
        with open("secret.key", "rb") as f:
            self.key = f.read()
        self.fernet = Fernet(self.key)

    # Encrypt Password
    def encryptPass(self, password):
        return self.fernet.encrypt(password.encode()).decode()

    # Decrypt Password
    def decryptPass(self, enc_pass):
        return self.fernet.decrypt(enc_pass).decode()
    
if __name__ == "__main__":
    enc = Encryption()
    enc_pass = enc.encryptPass("abhishek")
    print(f"Encrypted Pass: {enc_pass}")
    print(f"Decrypted Pass {enc.decryptPass(enc_pass)}")