# Input Utils Class
class InputUtils:
    @staticmethod
    def askInt(msg, allowed_values=None):
        while True:
            choice = input(msg)
            if choice.isdigit():
                value = int(choice)
                if (allowed_values is None or value in allowed_values): 
                    return value
                
            print("Enter a valid number!")

    @staticmethod
    def askString(msg):
        return input(msg)