from authentication.signup import SignUp
from utils.input_utils import InputUtils

class LogIn(SignUp):
    def __init__(self, auth_file="authfile.json"):
        super().__init__(auth_file)
    
    # Validation
    def logIn(self):
        print("--- Log In ---")

        while True:
            credentials = self.get_credentials()
            authentication_success = self.authentication(credentials["username"], credentials["password"])

            if (authentication_success):
                print("LogIn Successful")
                return True
            
            print("Invalid Credentials or User does not exist!")
            usr_choice = InputUtils.askInt("Enter 1 for LogIn or 2 for Sign Up: ", allowed_values=[1, 2])
            if usr_choice == 1:
                continue
            elif usr_choice == 2:
                return self.sign_up()
            
    
    def authenticate(self, username, password):
        authentication_success = self.authentication(username, password)
        if (authentication_success):
            print("LogIn Successful")
            return True
        
        print("Invalid Credentials or User does not exist!")

            