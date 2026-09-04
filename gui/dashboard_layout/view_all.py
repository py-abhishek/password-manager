import customtkinter as ctk
from password_manager.manager import PasswordManager
from password_manager.encrypt import Encryption
from .popup import PopupMenu
from .update_dialog import UpdateDialog
import pyperclip

passwordManager = PasswordManager('data.json')
encryption = Encryption()


# --- View All Passwords ---
class ViewAll(ctk.CTkFrame):
    def __init__(self, parent, main_dashboard):
        super().__init__(parent)
        self.main_dashboard = main_dashboard
        self.parent = parent

        self.add_widgets()

    def add_widgets(self):
        label = ctk.CTkLabel(self.main_dashboard, text="All Passwords", font=("Arial", 16))
        label.pack(pady=(30, 0))
        
        self.search_field = ctk.CTkEntry(self.main_dashboard, width=200, height=35, placeholder_text="Search...")
        self.search_field.pack(pady=(20, 0))

        self.search_field.bind("<KeyRelease>", self.search_password)
        self.table_frame = ctk.CTkScrollableFrame(self.main_dashboard, width=600, height= 600)
        self.table_frame._scrollbar.grid_forget()
        self.table_frame.pack(padx=(40,0), pady=(15,0))
        self.create_table()



    # Create table
    def create_table(self):
        data = [['ID', 'Platform', 'Username', 'Password']]
        saved_data = passwordManager.getAll()
        for index, row in enumerate(saved_data):
            data.append([index+1, row[1], row[2], encryption.decryptPass(row[3])])

        self.cells = [] # list to store grid cells

        for row_index, row in enumerate(data):
            row_cells = [] # list to store row cells
            for col_index, cell_data in enumerate(row):
                row_bg = 'transparent'
                # set row color
                if row_index == 0:
                    row_bg = '#484848'

                elif row_index % 2 == 0:
                    row_bg = '#333333'

                else:
                    row_bg ='#292929'

                cell = ctk.CTkLabel(self.table_frame,
                                    text=cell_data,
                                    width=120,
                                    height=35,
                                    fg_color=row_bg,
                                    text_color="white"
                                    )
                cell.grid(row=row_index, column=col_index, ipady=5, ipadx=10, sticky='ew')
                cell.bind("<Button-3>", lambda e, r = row_index: Options(self, self.table_frame, self.cells).show_popup(e, r))
                
                row_cells.append(cell) # storing grid rows
            
            if row_index != 0:
                self.cells.append(row_cells) # Storing all grid data


    # Search Password
    def search_password(self, event=None):
        query = self.search_field.get().strip().lower()
        for row in self.cells:
            row_text = (row[1].cget("text").lower()+" "+row[2].cget("text").lower())

            if query in row_text:
                # Show row
                for cell in row:
                    cell.grid()
            
            else:
                # hide row
                for cell in row:
                    cell.grid_remove()

# --- Options ---
class Options:
    def __init__(self, parent, table_frame, cells):
        self.parent = parent
        self.cells = cells
        self.table_frame = table_frame

    # show popup on right click
    def show_popup(self, event, row_index):
        # prevent multiple popups
        if getattr(self, "_active_popup", None):
            try:
                self._active_popup.destroy()
            except:
                pass

        # get Id
        # row_widget = self.cells[row_index]
        # record_id = row_widget[0].cget("text")

        # options
        options = [
            ["Edit", lambda: self.open_edit_dialog(row_index)],
            ["Delete", lambda: self.confirm_and_delete(row_index, self.cells)],
            ["Copy Password", lambda: self.copy_password(row_index)],
        ]

        popup = PopupMenu(self.parent, event.x_root, event.y_root, options)
        self._active_popup = popup

        # ensure popup reference removed when destroyed
        popup.bind("<Destroy>", lambda e: setattr(self, "_active_popup", None))

    
    def confirm_and_delete(self, row_index, cells):
        frame = ctk.CTkToplevel(self.parent)

        frame.geometry("250x135")
        frame.attributes('-topmost', True)
        frame.focus_force()

        ctk.CTkLabel(frame, text="Delete Password?", font=("Arial", 14)).pack(pady=(30, 0))
        optn_frame = ctk.CTkFrame(frame)
        optn_frame.pack(pady=(20,0))
        ctk.CTkButton(optn_frame, text="No", width=100, command=lambda: self.safe_destroy(frame)).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkButton(optn_frame, text="Yes", width=100, command=lambda: self.delete_pass(frame, row_index)).grid(row=0, column=1, padx=(10, 0))

    def delete_pass(self, frame, row_index):
        data = passwordManager.getAll()
        id = data[row_index-1][0]
        response = passwordManager.Delete_pass_by_id(id)
        if response['success'] == True:
            print("Password Deleted")
            self.refresh_table()
        self.safe_destroy(frame)

    def safe_destroy(self,frame):
        try:
            frame.destroy()
        except:
            pass

    # Update
    def open_edit_dialog(self, row_index):
        row_data = passwordManager.getAll()[row_index-1]

        UpdateDialog(self.parent, row_data, self.save_updated_password)

    # Save
    def save_updated_password(self, updated_data):
        response = passwordManager.update_pass_by_id(updated_data[0], updated_data[1], updated_data[2], updated_data[3])

        if response['success'] == True:
            print("Password Updated")
            self.refresh_table()
        else:
            print("Error")

    # Refresh table
    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.parent.create_table()

    # copy
    def copy_password(self, row_index):
        enc_pass = passwordManager.getAll()[row_index-1][3]
        password = encryption.decryptPass(enc_pass)
        pyperclip.copy(password)