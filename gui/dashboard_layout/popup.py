import customtkinter as ctk

class PopupMenu(ctk.CTkToplevel):
    def __init__(self, parent, x, y, options):
        super().__init__(parent)
        self.overrideredirect(True)
        # self.configure(fg_color="transparent")
        self.geometry(f"130x140+{x}+{y}")
        self.attributes('-topmost', True)
        TRANSPARENT = "#010101"
        self.wm_attributes("-transparentcolor", TRANSPARENT)
        self.configure(bg=TRANSPARENT)

        # Main container
        self.container = ctk.CTkFrame(self, fg_color="#3d3d3d", corner_radius=10)
        self.container.pack(fill="both", expand=True)

        self.options = options
        self.add_widgets()
        self.focus_force()

    def add_widgets(self):
        # --- Title ---
        title = ctk.CTkLabel(self.container, text="Options", text_color="white", font=("Arial", 12))
        title.pack(fill="x")
        
        # --- Separator ---
        separator = ctk.CTkFrame(self.container, fg_color="#5a5a5a", height=2)
        separator.pack(pady=(0, 10), fill="x")

        # adding options
        for text, cmd in self.options:
            btn = ctk.CTkButton(self.container,
                          text=text,
                          height=30,
                          fg_color='transparent',
                          hover_color='#333333',
                          command=lambda c=cmd: self._run_and_close(c)
                          )
            btn.pack(fill='x')
            # close while loosing focus or outside click
            self.bind("<FocusOut>", lambda e: self.destroy())

        

    def _run_and_close(self, command):
        try:
            if command:
                command()
                print("p2")

        finally:
            self.destroy()

        