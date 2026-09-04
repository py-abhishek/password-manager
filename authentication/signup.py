import json
from authentication.authentication import Authentication

class SignUp(Authentication):
    def __init__(self, auth_file="authfile.json"):
        super().__init__(auth_file)

    # Ask for user credentials
    def getCredentials(self):
        username = input("Enter username: ").strip()
        password = input("Enter Password: ").strip()
        return {"username": username, "password": password}

    def signUp(self):
        print("--- Sign Up ---")
        credentials = self.getCredentials()
        self.save_credentials(credentials)
        
    def save_credentials(self, credentials:dict):
        hash_pass = self.hashPass.hashPassword(credentials.get('password'))
        credentials['password'] = hash_pass
        try:
            with open(self.auth_file, "w") as f:
                json.dump(credentials, f, indent=4)
                print("SignUp Successful!")
                return True

        except Exception as e:
            print(f"Error: {e}")
            return False
        