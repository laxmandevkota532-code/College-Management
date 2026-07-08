import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class StudentManagementPage(ctk.CTkFrame):
    def __init__(self, master, open_add_student_callback=None):
        super().__init__(master, fg_color="#F8F9FC")

        # Navigation Callback Injection
        self.open_add_student_callback = open_add_student_callback

        # --- Color Palette ---
        self.PRIMARY_BLUE = "#4F5BD5"
        self.HOVER_BLUE = "#3F4ACB"
        self.BACKGROUND = "#F8F9FC"
        self.PANEL_BG = "#EEF2FF"
        self.TEXT_DARK = "#111827"
        self.TEXT_GRAY = "#6B7280"
        self.WHITE = "#FFFFFF"
        self.SUCCESS_GREEN = "#10B981"
        self.DANGER_RED = "#EF4444"
        self.BORDER_COLOR = "#E5E7EB"

        # Responsive Layout Configuration 
        # (Only 1 column now, 2 rows: Action Bar and Table)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Sample Data ---
        self.students_data = [
            {"id": "STU001", "name": "Aarav Sharma",    "gender": "Male",   "course": "CSIT",  "phone": "9801234567", "email": "aarav.sharma@email.com",    "status": "Active"},
            {"id": "STU002", "name": "Priya Thapa",     "gender": "Female", "course": "BCA",   "phone": "9812345678", "email": "priya.thapa@email.com",     "status": "Active"},
            {"id": "STU003", "name": "Rohan Karki",     "gender": "Male",   "course": "BIT",   "phone": "9823456789", "email": "rohan.karki@email.com",     "status": "Inactive"},
            {"id": "STU004", "name": "Sita Rai",        "gender": "Female", "course": "BBS",   "phone": "9834567890", "email": "sita.rai@email.com",        "status": "Active"},
            {"id": "STU005", "name": "Bikram Magar",    "gender": "Male",   "course": "BIM",   "phone": "9845678901", "email": "bikram.magar@email.com",    "status": "Active"},
            {"id": "STU006", "name": "Anjali Gurung",   "gender": "Female", "course": "CSIT",  "phone": "9856789012", "email": "anjali.gurung@email.com",   "status": "Inactive"},
            {"id": "STU007", "name": "Suresh Pandey",   "gender": "Male",   "course": "BCA",   "phone": "9867890123", "email": "suresh.pandey@email.com",   "status": "Active"},
            {"id": "STU008", "name": "Nisha Tamang",    "gender": "Female", "course": "BIT",   "phone": "9878901234", "email": "nisha.tamang@email.com",    "status": "Active"},
            {"id": "STU009", "name": "Dipesh Bhandari", "gender": "Male",   "course": "BBS",   "phone": "9889012345", "email": "dipesh.bhandari@email.com", "status": "Active"},
            {"id": "STU010", "name": "Kamala Shrestha", "gender": "Female", "course": "BIM",   "phone": "9890123456", "email": "kamala.shrestha@email.com", "status": "Inactive"},
        ]

        self.create_main_content()

    def create_main_content(self):
        """Builds responsive layout area panel structures."""
        
        # --- Top Action Bar Layout Container ---
        action_bar = ctk.CTkFrame(self, fg_color="transparent")
        action_bar.grid(row=0, column=0, padx=40, pady=(40, 20), sticky="ew")
        action_bar.grid_columnconfigure(0, weight=1)

        search_entry = ctk.CTkEntry(
            action_bar, 
            placeholder_text="Search Student...", 
            width=350, 
            height=45, 
            fg_color=self.WHITE, 
            border_color=self.BORDER_COLOR, 
            border_width=1,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont(size=14)
        )
        search_entry.grid(row=0, column=0, sticky="w")

        add_btn = ctk.CTkButton(
            action_bar, 
            text="+ Add Student", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            fg_color=self.PRIMARY_BLUE, 
            hover_color=self.HOVER_BLUE, 
            text_color=self.WHITE, 
            height=45, 
            corner_radius=8,
            command=self.open_add_student
        )
        add_btn.grid(row=0, column=1, sticky="e")

        # --- Central Table Card Container ---
        table_container = ctk.CTkFrame(
            self, 
            fg_color=self.WHITE, 
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER_COLOR
        )
        table_container.grid(row=1, column=0, padx=40, pady=(0, 40), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # Matrix Headers Configuration
        headers = ["Student ID", "Full Name", "Gender", "Course", "Phone", "Email", "Status", "Actions"]
        columns_width = [100, 160, 90, 90, 120, 220, 100, 180]

        header_frame = ctk.CTkFrame(table_container, fg_color=self.PANEL_BG, height=55, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        header_frame.grid_propagate(False)
        
        for idx, header in enumerate(headers):
            header_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])
            lbl = ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(size=13, weight="bold"), 
                text_color=self.TEXT_DARK, 
                anchor="w"
            )
            lbl.grid(row=0, column=idx, padx=20, pady=15, sticky="ew")

        # Scrollable Frame Construction
        self.scroll_frame = ctk.CTkScrollableFrame(
            table_container, 
            fg_color="transparent", 
            corner_radius=0
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        
        for idx in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])

        self.populate_table_data()

    def populate_table_data(self):
        """Renders raw arrays iteratively matching design systems guidelines precisely."""
        
        px = 20  # Consistent X padding
        py = 18  # Consistent Y padding for better row height

        for row_idx, student in enumerate(self.students_data):
            
            id_lbl = ctk.CTkLabel(self.scroll_frame, text=student["id"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            id_lbl.grid(row=row_idx, column=0, padx=px, pady=py, sticky="ew")

            name_lbl = ctk.CTkLabel(self.scroll_frame, text=student["name"], font=ctk.CTkFont(size=14, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            name_lbl.grid(row=row_idx, column=1, padx=px, pady=py, sticky="ew")

            gender_lbl = ctk.CTkLabel(self.scroll_frame, text=student["gender"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            gender_lbl.grid(row=row_idx, column=2, padx=px, pady=py, sticky="ew")

            course_lbl = ctk.CTkLabel(self.scroll_frame, text=student["course"], font=ctk.CTkFont(size=13, weight="bold"), text_color=self.PRIMARY_BLUE, anchor="w")
            course_lbl.grid(row=row_idx, column=3, padx=px, pady=py, sticky="ew")

            phone_lbl = ctk.CTkLabel(self.scroll_frame, text=student["phone"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            phone_lbl.grid(row=row_idx, column=4, padx=px, pady=py, sticky="ew")

            email_lbl = ctk.CTkLabel(self.scroll_frame, text=student["email"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            email_lbl.grid(row=row_idx, column=5, padx=px, pady=py, sticky="ew")

            # Status pill design geometry badge injection (Modern soft colors)
            status_text = student["status"]
            badge_color = "#D1FAE5" if status_text == "Active" else "#FEE2E2"
            text_color = "#065F46" if status_text == "Active" else "#991B1B"
            
            status_badge = ctk.CTkFrame(self.scroll_frame, fg_color=badge_color, corner_radius=12, width=75, height=26)
            status_badge.grid(row=row_idx, column=6, padx=px, pady=py, sticky="w")
            status_badge.grid_propagate(False)
            
            status_lbl = ctk.CTkLabel(status_badge, text=status_text, font=ctk.CTkFont(size=12, weight="bold"), text_color=text_color)
            status_lbl.place(relx=0.5, rely=0.5, anchor="center")

            # Action Frame Layout Container
            action_panel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            action_panel.grid(row=row_idx, column=7, padx=px, pady=py, sticky="ew")

            view_btn = ctk.CTkButton(
                action_panel, text="View", font=ctk.CTkFont(size=12, weight="bold"), 
                fg_color="#F3F4F6", hover_color="#E5E7EB", text_color=self.TEXT_DARK, 
                width=46, height=28, corner_radius=6
            )
            view_btn.grid(row=0, column=0, padx=3)

            edit_btn = ctk.CTkButton(
                action_panel, text="Edit", font=ctk.CTkFont(size=12, weight="bold"), 
                fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, 
                width=46, height=28, corner_radius=6
            )
            edit_btn.grid(row=0, column=1, padx=3)

            delete_btn = ctk.CTkButton(
                action_panel, text="Delete", font=ctk.CTkFont(size=12, weight="bold"), 
                fg_color="#FEE2E2", hover_color="#FCA5A5", text_color=self.DANGER_RED, 
                width=50, height=28, corner_radius=6
            )
            delete_btn.grid(row=0, column=2, padx=3)

    def open_add_student(self):
        """Triggers UI navigation frame routing workflow via parent dashboard state injection handles."""
        if self.open_add_student_callback:
            self.open_add_student_callback()
        else:
            print("Open Add Student")


if __name__ == "__main__":
    # Kept ONLY for standalone file testing. 
    # Your Dashboard integration will naturally ignore this block.
    root = ctk.CTk()
    root.geometry("1100x700")
    page = StudentManagementPage(root, open_add_student_callback=lambda: print("Open Add Student"))
    page.pack(fill="both", expand=True)
    root.mainloop()