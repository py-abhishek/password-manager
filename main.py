from password_manager.manager import PasswordManager
from password_manager.encrypt import Encryption
from authentication.login import LogIn
from authentication.signup import SignUp
from utils.input_utils import InputUtils
from password_manager.password_generator import PasswordGenerator

pass_file = "data.json"
auth_file = "authfile.json"
passwordManager = PasswordManager(pass_file)
encryption = Encryption()
inputUtils = InputUtils()
passwordGenerator = PasswordGenerator()

# User Athentication
def usrAuth():
    print("-- Password Manager --")
    usr_choice = inputUtils.askInt("Enter 1 for LogIn or 2 for SignUp: ",allowed_values=[1, 2])
    if (usr_choice == 1):
        # LogIn
        return LogIn(auth_file).logIn()
        
    elif (usr_choice == 2):
        # SignUp
        return SignUp(auth_file).signUp()

options = '''
    -------------------
    Choose an Option:
    1. Add Password
    2. Search Password
    3. Delete Password
    4. Update Password
    5. View All
    6. Exit
    -------------------
        '''

password_options = '''
    ----------------------------
    Choose an option:
    1. Enter custom password
    2. Generate Random Password
    ----------------------------
    '''

def initialize():
    if usrAuth():
        # Initializing Project and Providing user multiple opitons
        while True:
            print(options)
            user_choice = inputUtils.askInt("Enter a number to choose relevant option: ", allowed_values=[1, 2, 3, 4, 5, 6])

            # Add Pass
            if user_choice == 1:
                platform_name = input("Enter platform name: ")
                usr_name = input("Enter Email or Username: ")
                pw_choice = inputUtils.askInt(password_options,allowed_values=[1, 2])
                
                if pw_choice == 1:
                    password = input("Enter Password: ")

                elif pw_choice == 2:
                    password = passwordGenerator.generatePassword()
                    print(f"Your password is: {password}")

                # Encrypt Password
                enc_pass_str = encryption.encryptPass(password)
                response = passwordManager.addPassword(platform_name, usr_name, enc_pass_str)
                if response['success'] == True:
                    print("Password Added Successfully!")
                else: print("Error while adding password!")
            
            # Search Password
            elif user_choice == 2:
                usr_input = input("Search Passwords(Enter platform or username): ")
                result = passwordManager.searchPassword(usr_input)
                if result:
                    for i, item in enumerate(result):
                        print(f"{i+1}. Platform: {item[1]} | Username: {item[2]} | Password: {encryption.decryptPass(item[3])}")

                else:
                    print("No result found!")

            # Delete password
            elif user_choice == 3:
                usr_input = input("Delete Password(Enter platform or username): ")
                response = passwordManager.deletePassword(usr_input)
                print(response)
                if response['success'] == True:
                    print("Password deleted successfully!")
                else: print("Error while deleting password!")

            # Update Password
            elif user_choice == 4:
                usr_input = input("Update Password(Enter platform or username): ")
                response = passwordManager.updatePassword(usr_input)
                if response['success'] == True:
                    print("Password updated successfully!")
                else: print("Error while updating password!")
            
            elif user_choice == 5:
                result = passwordManager.getAll()
                if result:
                    for i, item in enumerate(result):
                        print(f"{i+1}. Platform: {item[1]} | Username: {item[2]} | Password: {encryption.decryptPass(item[3])}")
                else:
                    print("No Data Found!")

            # Exit
            elif user_choice == 6:
                break

                

if __name__ == "__main__":
    initialize()