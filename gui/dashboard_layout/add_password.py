import customtkinter as ctk
from password_manager.manager import PasswordManager
from password_manager.encrypt import Encryption

passwordManager = PasswordManager("data.json")
encryption = Encryption()

# --- Add Password ---
class AddPassword(ctk.CTkFrame):
    def __init__(self, parent, main_dashboard):
        super().__init__(parent)
        self.main_dashboard = main_dashboard

        self.add_widgets()

    def add_widgets(self):
        label = ctk.CTkLabel(self.main_dashboard, text="Add Password", font=("Arial", 16))
        label.pack(pady=(30,0))

        self.inp_platform = ctk.CTkEntry(self.main_dashboard, width=250, height=35, placeholder_text='Platform Name')
        self.inp_platform.pack(pady=(20, 0))
        self.inp_username = ctk.CTkEntry(self.main_dashboard, width=250, height=35, placeholder_text='Username')
        self.inp_username.pack(pady=(10, 0))
        self.inp_password = ctk.CTkEntry(self.main_dashboard, width=250, height=35, placeholder_text='Password')
        self.inp_password.pack(pady=(10, 0))

        btn = ctk.CTkButton(self.main_dashboard, width=150, height=35, text='Save', cursor='hand2', command=self.add_password)
        btn.pack(pady=(20, 0))
        
        self.info_label = ctk.CTkLabel(self.main_dashboard, text='', font=("Arial", 12))
        self.info_label.pack(pady=10)

    def add_password(self):
        platform = self.inp_platform.get().strip()
        username = self.inp_username.get().strip()
        password = self.inp_password.get().strip()

        # Check if user entered all required values
        if username == '' or password == '':
            self.info_label.configure(text="Username and Password fields are required")
        else:
            enc_pass = encryption.encryptPass(password) # Encrypt Password
            response = passwordManager.add_password(platform, username, enc_pass)
            if response['success'] == True:
                msg = "Password Added Successfully"
                self.info_label.configure(text=msg)
                self.inp_platform.delete(0, 'end')
                self.inp_username.delete(0, 'end')
                self.inp_password.delete(0, 'end')
            else:
                self.info_label.configure(text="Error while adding password!")
   