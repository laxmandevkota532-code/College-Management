import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class CoursesPage(ctk.CTk):
    def __init__(self):
        super().__init__()

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

        # --- Window Configuration ---
        self.title("Courses Management System")
        self.geometry("1280x720")
        self.configure(fg_color=self.BACKGROUND)
        
        # Open in Full Screen automatically
        self.after(100, lambda: self.state("zoomed"))
        
        # Responsive Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sample Data ---
        self.courses_data = [
            {"id": "CRS001", "name": "BCA", "duration": "4 Years", "fee": "Rs. 450000", "students": "320", "status": "Active"},
            {"id": "CRS002", "name": "BIT", "duration": "4 Years", "fee": "Rs. 480000", "students": "250", "status": "Active"},
            {"id": "CRS003", "name": "CSIT", "duration": "4 Years", "fee": "Rs. 500000", "students": "280", "status": "Active"},
            {"id": "CRS004", "name": "BBS", "duration": "4 Years", "fee": "Rs. 350000", "students": "180", "status": "Inactive"},
            {"id": "CRS005", "name": "BIM", "duration": "4 Years", "fee": "Rs. 470000", "students": "150", "status": "Active"},
        ]

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        """Creates the navigation sidebar mimicking the requested page design."""
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.WHITE)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(8, weight=1)

        # Brand Identity Label
        brand_label = ctk.CTkLabel(sidebar, text="EduManager", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.PRIMARY_BLUE)
        brand_label.grid(row=0, column=0, padx=30, pady=(30, 30), sticky="w")

        # Sidebar Menu Items
        menu_items = ["Dashboard", "Students", "Courses", "Teachers", "Attendance", "Reports", "Settings"]
        
        for idx, item in enumerate(menu_items, start=1):
            if item == "Courses":
                # Active State Design System Stylings
                btn = ctk.CTkButton(sidebar, text=item, font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PANEL_BG, text_color=self.PRIMARY_BLUE, anchor="w", height=40, corner_radius=6)
            else:
                # Standard Passive Menu Items Stylings
                btn = ctk.CTkButton(sidebar, text=item, font=ctk.CTkFont(size=14), fg_color="transparent", text_color=self.TEXT_GRAY, hover_color=self.PANEL_BG, anchor="w", height=40, corner_radius=6)
            
            btn.grid(row=idx, column=0, padx=20, pady=4, sticky="ew")

        # Logout Placed Static at the Base Layout System Container
        logout_btn = ctk.CTkButton(sidebar, text="Logout", font=ctk.CTkFont(size=14), fg_color="transparent", text_color=self.TEXT_GRAY, hover_color=self.PANEL_BG, anchor="w", height=40, corner_radius=6)
        logout_btn.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

    def create_main_content(self):
        """Builds responsive layout area panel structures."""
        main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=self.BACKGROUND)
        main_container.grid(row=0, column=1, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)

        # Top Bar Container Setup Row
        top_bar = ctk.CTkFrame(main_container, height=70, corner_radius=0, fg_color=self.WHITE)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_propagate(False)
        
        page_title = ctk.CTkLabel(top_bar, text="Courses Management", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.TEXT_DARK)
        page_title.grid(row=0, column=0, padx=30, pady=20, sticky="w")
        
        user_profile = ctk.CTkLabel(top_bar, text="Admin User", font=ctk.CTkFont(size=14), text_color=self.TEXT_GRAY)
        user_profile.grid(row=0, column=1, padx=30, pady=20, sticky="e")

        # Top Action Bar Layout Container Subsystem
        action_bar = ctk.CTkFrame(main_container, fg_color="transparent")
        action_bar.grid(row=1, column=0, padx=30, pady=(25, 15), sticky="ew")
        action_bar.grid_columnconfigure(0, weight=1)

        search_entry = ctk.CTkEntry(action_bar, placeholder_text="Search Course...", width=300, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, text_color=self.TEXT_DARK)
        search_entry.grid(row=0, column=0, sticky="w")

        add_btn = ctk.CTkButton(action_bar, text="+ Add Course", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE, height=40, corner_radius=6)
        add_btn.grid(row=0, column=1, sticky="e")

        # Central Layout Data Matrix Display Segment System Box Layer
        table_container = ctk.CTkFrame(main_container, fg_color=self.WHITE, corner_radius=8)
        table_container.grid(row=2, column=0, padx=30, pady=(0, 30), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # Matrix Headers Configuration
        headers = ["Course ID", "Course Name", "Duration", "Fee", "Students", "Status", "Actions"]
        columns_width = [110, 160, 120, 140, 110, 110, 160]

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
        for row_idx, course in enumerate(self.courses_data):
            
            id_lbl = ctk.CTkLabel(self.scroll_frame, text=course["id"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            id_lbl.grid(row=row_idx, column=0, padx=15, pady=12, sticky="ew")

            name_lbl = ctk.CTkLabel(self.scroll_frame, text=course["name"], font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            name_lbl.grid(row=row_idx, column=1, padx=15, pady=12, sticky="ew")

            duration_lbl = ctk.CTkLabel(self.scroll_frame, text=course["duration"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            duration_lbl.grid(row=row_idx, column=2, padx=15, pady=12, sticky="ew")

            fee_lbl = ctk.CTkLabel(self.scroll_frame, text=course["fee"], font=ctk.CTkFont(size=13), text_color=self.TEXT_DARK, anchor="w")
            fee_lbl.grid(row=row_idx, column=3, padx=15, pady=12, sticky="ew")

            students_lbl = ctk.CTkLabel(self.scroll_frame, text=course["students"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            students_lbl.grid(row=row_idx, column=4, padx=15, pady=12, sticky="ew")

            # Status pill design geometry badge injection
            status_text = course["status"]
            badge_color = self.SUCCESS_GREEN if status_text == "Active" else self.DANGER_RED
            
            status_badge = ctk.CTkFrame(self.scroll_frame, fg_color=badge_color, corner_radius=12, width=75, height=24)
            status_badge.grid(row=row_idx, column=5, padx=15, pady=12, sticky="w")
            status_badge.grid_propagate(False)
            
            status_lbl = ctk.CTkLabel(status_badge, text=status_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=self.WHITE)
            status_lbl.place(relx=0.5, rely=0.5, anchor="center")

            # Action Frame Layout Container Row Grid Integration Line Logic
            action_panel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            action_panel.grid(row=row_idx, column=6, padx=15, pady=12, sticky="ew")

            view_btn = ctk.CTkButton(action_panel, text="View", font=ctk.CTkFont(size=11), fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, width=42, height=24, corner_radius=4)
            view_btn.grid(row=0, column=0, padx=2)

            edit_btn = ctk.CTkButton(action_panel, text="Edit", font=ctk.CTkFont(size=11), fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, width=42, height=24, corner_radius=4)
            edit_btn.grid(row=0, column=1, padx=2)

            delete_btn = ctk.CTkButton(action_panel, text="Delete", font=ctk.CTkFont(size=11), fg_color="#FEE2E2", hover_color="#FCA5A5", text_color=self.DANGER_RED, width=46, height=24, corner_radius=4)
            delete_btn.grid(row=0, column=2, padx=2)

if __name__ == "__main__":
    app = CoursesPage()
    app.mainloop()