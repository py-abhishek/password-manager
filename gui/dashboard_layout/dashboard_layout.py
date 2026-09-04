import customtkinter as ctk
from password_manager.manager import PasswordManager
from password_manager.encrypt import Encryption
from .view_all import ViewAll
from .add_password import AddPassword

passwordManager = PasswordManager('data.json')
encryption = Encryption()

class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller

        # -- Grid Layout --
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)

        # # -- Sidebar --
        self.dashboard_sidebar = ctk.CTkFrame(self, width=160)
        self.dashboard_sidebar.grid(row=0, column=0, sticky='nsw')

        self.add_sidebar()

        # # -- Main Content --
        self.main_dashboard = ctk.CTkFrame(self, fg_color='transparent')
        self.main_dashboard.grid(row=0, column=1, sticky='nsew')

        self.view_all_btn()

    # sidebar
    def add_sidebar(self):
        title = ctk.CTkLabel(self.dashboard_sidebar, width=160, text='Options', font=('Arial',16))
        title.pack(pady=20)

        btn_viewall_pass = ctk.CTkButton(self.dashboard_sidebar, height=40, text='View All Passwords', command=self.view_all_btn, font=('Arial', 13), corner_radius=3, hover_color='#525252', fg_color='transparent', anchor='w', border_spacing=15, cursor='hand2')
        btn_viewall_pass.pack(fill='x', anchor='w', expand=False)

        btn_new_pass = ctk.CTkButton(self.dashboard_sidebar, height= 40, text='Add New Password', command=self.add_btn, font=('Arial', 13), corner_radius=3, hover_color='#525252', fg_color='transparent', anchor='w', border_spacing=15, cursor='hand2')
        btn_new_pass.pack(fill='x', anchor='w', expand=False)

        btn_signout = ctk.CTkButton(self.dashboard_sidebar, height=40, text='Sign out', command=self.sign_out_btn, font=('Arial', 13), corner_radius=3, hover_color='#525252', fg_color='transparent', anchor='w', border_spacing=15, cursor='hand2')
        btn_signout.pack(fill='x', anchor='w', expand=False)

    # Clear all widgets
    def clear(self):
        for widget in self.main_dashboard.winfo_children():
            widget.destroy()

        
    # All options
    def view_all_btn(self):
        self.clear()
        ViewAll(self.parent, self.main_dashboard)

    def add_btn(self):
        self.clear()
        AddPassword(self.parent, self.main_dashboard)

    def sign_out_btn(self):
        self.controller.showScreen('loginscreen')