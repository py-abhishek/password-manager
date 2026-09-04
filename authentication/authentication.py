import json
import bcrypt


class hash_password:
    def __init__(self):
        pass

    # Hashing Password
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
    # Verifying Password
    def verify_password(self, password, stored_hash):
        return bcrypt.checkpw(password.encode(), stored_hash.encode())


class Authentication:
    def __init__(self, auth_file):
        self.auth_file = auth_file
        self.hashPass = hash_password()
        

    # Password Validation
    def authentication(self, username, password):
        data = self.read_pass()
        if data is None:
            return False
        
        stored_username = data.get('username')
        stored_pass = data.get('password')

        if stored_username is None or stored_pass is None:
            return False
        
        verify_pass = self.hashPass.verify_password(password, stored_pass)
        
        if (stored_username == username and verify_pass):
            # Authentication Success
            return True
        # Authentication Failed
        return False

    # Read Stored Password
    def read_pass(self):
        try:
            with open(self.auth_file, "r") as f:
                data = json.load(f)
                return data
            
        except (FileNotFoundError, json.JSONDecodeError):
            # Create new file
            return None


if __name__ == "__main__":
    hp = hash_password()
    print(hp.verify_password("abhi", "$2b$12$eMiSzXiWpT1.7G61pd9r6O2ai26ArquREdDVmCWKxH0fReKTSiNwK"))
    # LogIn("authfile.json").logIn()
