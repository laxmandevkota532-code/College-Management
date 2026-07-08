import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class TeachersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#F8F9FC")

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
        
        # Responsive Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Sample Data ---
        self.teachers_data = [
            {"id": "TCH001", "name": "John Smith", "subject": "Database Systems", "phone": "9841000001", "email": "john@gmail.com", "experience": "5 Years", "status": "Active"},
            {"id": "TCH002", "name": "Sarah Johnson", "subject": "OOP", "phone": "9841000002", "email": "sarah@gmail.com", "experience": "4 Years", "status": "Active"},
            {"id": "TCH003", "name": "Michael Brown", "subject": "Mathematics", "phone": "9841000003", "email": "michael@gmail.com", "experience": "7 Years", "status": "Active"},
            {"id": "TCH004", "name": "Emily Davis", "subject": "Software Engineering", "phone": "9841000004", "email": "emily@gmail.com", "experience": "3 Years", "status": "Inactive"},
            {"id": "TCH005", "name": "David Wilson", "subject": "Computer Networks", "phone": "9841000005", "email": "david@gmail.com", "experience": "6 Years", "status": "Active"},
        ]

        self.create_main_content()

    def create_main_content(self):
        """Builds responsive layout area panel structures for main content."""
        # Top Action Bar Layout Container
        action_bar = ctk.CTkFrame(self, fg_color="transparent")
        action_bar.grid(row=0, column=0, padx=30, pady=(25, 15), sticky="ew")
        action_bar.grid_columnconfigure(0, weight=1)

        search_entry = ctk.CTkEntry(action_bar, placeholder_text="Search Teacher...", width=300, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, text_color=self.TEXT_DARK)
        search_entry.grid(row=0, column=0, sticky="w")

        add_btn = ctk.CTkButton(action_bar, text="+ Add Teacher", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE, height=40, corner_radius=6)
        add_btn.grid(row=0, column=1, sticky="e")

        # Central Layout Data Matrix Display Segment
        table_container = ctk.CTkFrame(self, fg_color=self.WHITE, corner_radius=8)
        table_container.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # Matrix Headers Configuration
        headers = ["Teacher ID", "Full Name", "Subject", "Phone", "Email", "Experience", "Status", "Actions"]
        columns_width = [100, 150, 160, 110, 160, 100, 100, 160]

        header_frame = ctk.CTkFrame(table_container, fg_color=self.PANEL_BG, height=45, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        
        for idx, header in enumerate(headers):
            header_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])
            lbl = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            lbl.grid(row=0, column=idx, padx=15, pady=10, sticky="ew")

        # Scrollable Frame Construction Injection
        self.scroll_frame = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        
        for idx in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])

        self.populate_table_data()

    def populate_table_data(self):
        """Renders raw arrays iteratively matching design systems guidelines precisely."""
        for row_idx, teacher in enumerate(self.teachers_data):
            
            id_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["id"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            id_lbl.grid(row=row_idx, column=0, padx=15, pady=12, sticky="ew")

            name_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["name"], font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            name_lbl.grid(row=row_idx, column=1, padx=15, pady=12, sticky="ew")

            subject_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["subject"], font=ctk.CTkFont(size=13), text_color=self.TEXT_DARK, anchor="w")
            subject_lbl.grid(row=row_idx, column=2, padx=15, pady=12, sticky="ew")

            phone_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["phone"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            phone_lbl.grid(row=row_idx, column=3, padx=15, pady=12, sticky="ew")

            email_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["email"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            email_lbl.grid(row=row_idx, column=4, padx=15, pady=12, sticky="ew")

            exp_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["experience"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            exp_lbl.grid(row=row_idx, column=5, padx=15, pady=12, sticky="ew")

            # Status pill design geometry badge injection
            status_text = teacher["status"]
            badge_color = self.SUCCESS_GREEN if status_text == "Active" else self.DANGER_RED
            
            status_badge = ctk.CTkFrame(self.scroll_frame, fg_color=badge_color, corner_radius=12, width=75, height=24)
            status_badge.grid(row=row_idx, column=6, padx=15, pady=12, sticky="w")
            status_badge.grid_propagate(False)
            
            status_lbl = ctk.CTkLabel(status_badge, text=status_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=self.WHITE)
            status_lbl.place(relx=0.5, rely=0.5, anchor="center")

            # Action Frame Layout Container Row Grid Integration
            action_panel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            action_panel.grid(row=row_idx, column=7, padx=15, pady=12, sticky="ew")

            view_btn = ctk.CTkButton(action_panel, text="View", font=ctk.CTkFont(size=11), fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, width=42, height=24, corner_radius=4)
            view_btn.grid(row=0, column=0, padx=2)

            edit_btn = ctk.CTkButton(action_panel, text="Edit", font=ctk.CTkFont(size=11), fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, width=42, height=24, corner_radius=4)
            edit_btn.grid(row=0, column=1, padx=2)

            delete_btn = ctk.CTkButton(action_panel, text="Delete", font=ctk.CTkFont(size=11), fg_color="#FEE2E2", hover_color="#FCA5A5", text_color=self.DANGER_RED, width=46, height=24, corner_radius=4)
            delete_btn.grid(row=0, column=2, padx=2)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x700")
    page = TeachersPage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()

    