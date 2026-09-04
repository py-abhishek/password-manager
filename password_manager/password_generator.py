import string
import secrets

# To generate and suggest password
class PasswordGenerator:
    def __init__(self):
        self.digits = string.digits
        self.symbols = string.punctuation
        self.lower = string.ascii_lowercase
        self.upper = string.ascii_uppercase
        self.length = 14

    def generatePassword(self):
        allowed_char = (self.digits+self.symbols+self.lower+self.upper)
        password = ''.join(secrets.choice(allowed_char) for _ in range(self.length))
        return password


if __name__ == "__main__":
    print(PasswordGenerator().generatePassword())