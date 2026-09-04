import customtkinter as ctk
from .dashboard_layout.dashboard_layout import DashboardScreen
from authentication.login import LogIn
from authentication.signup import SignUp
from password_manager.encrypt import Encryption

auth_file = "authfile.json"

ctk.set_default_color_theme('blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Password Manager')
        self.geometry('800x700')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # container for screens
        self.container = ctk.CTkFrame(self,fg_color='transparent')
        self.container.grid(row=0, column=0, sticky='nsew')

        # Make container expandable
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary for screens
        self.screens = {}

        self.createScreens()
        self.showScreen('loginscreen')

    def createScreens(self):
        for Screen in (LoginScreen, SignupScreen, DashboardScreen):
            screen_name = Screen.__name__.lower()
            frame = Screen(parent=self.container, controller=self)
            self.screens[screen_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def showScreen(self, screen_name):
        screen = self.screens[screen_name]
        screen.tkraise() # Bring that frame to the front
        pass


# Log In Screen
class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.login_text = 'Log In'
        self.addWidgets(self.login_text)

    # Add widgets
    def addWidgets(self, title):
        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.place(relx=0.5, rely=0.5, anchor='center') # vertically center

        self.label = ctk.CTkLabel(self.frame, text=title.upper(), font=('Arial', 22))
        self.label.pack(pady=10)

        self.username = ctk.CTkEntry(self.frame, width=190, height=30, corner_radius=5, border_width=2, placeholder_text='Username')
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self.frame, width=190, height=30, corner_radius=5, border_width=2, placeholder_text='Password')
        self.password.pack(pady=10)

        self.submit_btn = ctk.CTkButton(self.frame, width=120, height=30, corner_radius=5, text=title, command=self.logIn)
        self.submit_btn.pack(pady=20)

        self.sign_up_btn = ctk.CTkButton(self.frame, text='New User? Sign Up Here', bg_color='transparent', fg_color='transparent', hover=False, command=self.showSignupScreen)
        self.sign_up_btn.pack()
    
    def logIn(self):
        username = self.username.get().strip()
        password = self.password.get()

        if LogIn().authenticate(username, password):
            self.controller.showScreen('dashboardscreen')
        else: print("Invalid Credentials!")

        print('LogIn')
    
    def showSignupScreen(self):
        self.controller.showScreen('signupscreen')


# Sign Up Screen
class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.signup_text = 'Sign Up'
        self.addWidgets(self.signup_text)

    # Add widgets
    def addWidgets(self, title):
        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.place(relx=0.5, rely=0.5, anchor='center') # vertically center

        self.label = ctk.CTkLabel(self.frame, text=title.upper(), font=('Arial', 22))
        self.label.pack(pady=10)

        self.username = ctk.CTkEntry(self.frame, width=190, height=30, corner_radius=5, border_width=2, placeholder_text='Username')
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self.frame, width=190, height=30, corner_radius=5, border_width=2, placeholder_text='Password')
        self.password.pack(pady=10)

        self.btn = ctk.CTkButton(self.frame, width=120, height=30, corner_radius=5, text=title, command=self.sign_up)
        self.btn.pack(pady=20)

        hover_clr = self.cget('fg_color')
        self.sign_in_btn = ctk.CTkButton(self.frame, text='Already have account? Log In Here', bg_color='transparent', fg_color='transparent', hover=False, command=self.showLoginScreen)
        self.sign_in_btn.pack()

    def showLoginScreen(self):
        self.controller.showScreen('loginscreen')

    def sign_up(self):
        Username = self.username.get().strip()
        password = self.password.get()
        credentials = {"username": Username, "password": password}

        if SignUp().save_credentials(credentials):
            self.controller.showScreen('dashboardscreen')
            print("Account Created Successfully")
        else: print("Error while creating account!")

App().mainloop()
