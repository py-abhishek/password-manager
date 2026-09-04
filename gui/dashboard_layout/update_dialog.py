import customtkinter as ctk
from password_manager.encrypt import Encryption
class UpdateDialog(ctk.CTkToplevel):
    def __init__(self, parent, row_data, on_save):
        super().__init__(parent)
        self.title("Update Password")
        self.geometry("320x345")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.row_data = row_data
        self.on_save = on_save


        self.focus_force()
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        _id, platform, username, password, _created_at = self.row_data

        ctk.CTkLabel(self, text="Update Password", font=("Arial", 14)).pack(pady=10)

        # Platform name
        ctk.CTkLabel(self, text="Platform", font=("Arial", 13)).pack(pady=(5, 0), anchor="w", padx=(25, 0))
        self.platform_entry = ctk.CTkEntry(self, width=280)
        self.platform_entry.pack(pady="5")
        self.platform_entry.insert(0, platform)

        # Username
        ctk.CTkLabel(self, text="Username", font=("Arial", 13)).pack(pady=(5, 0), anchor="w", padx=(25, 0))
        self.username_entry = ctk.CTkEntry(self, width=280)
        self.username_entry.pack(pady="5")
        self.username_entry.insert(0, username)

        # Password
        ctk.CTkLabel(self, text="Password", font=("Arial", 13)).pack(pady=(5, 0), anchor="w", padx=(25, 0))
        self.password_entry = ctk.CTkEntry(self, width=280)
        self.password_entry.pack(pady="5")
        dec_pass = Encryption().decryptPass(password)
        self.password_entry.insert(0, dec_pass)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", width=100, command=self.safe_destroy)
        cancel_btn.grid(row=0, column=0, pady=10, padx=(0, 20))

        save_btn = ctk.CTkButton(btn_frame, text="Update", width=100, command=self.save)
        save_btn.grid(row=0, column=1, pady=10, padx=(20, 0))

    def safe_destroy(self):
        try:
            self.destroy()
        except:
            pass

    def _run_and_close(self, command):
        # Run the clicked command AFTER closing popup
        if command:
            self.after(10, command)

        # Destroy popup safely after Tk finishes all internal events
        self.after(1, self.safe_destroy)


    # Save
    def save(self):
        updated_data=[
            self.row_data[0],
            self.platform_entry.get().strip(),
            self.username_entry.get().strip(),
            self.password_entry.get().strip()
        ]

        self.on_save(updated_data)
        self.safe_destroy()