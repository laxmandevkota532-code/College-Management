import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class StudentsPage(ctk.CTk):
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
        self.title("Students Management System")
        self.geometry("1280x720")
        self.configure(fg_color=self.BACKGROUND)
        
        # Make full screen responsive
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sample Data ---
        self.students_data = [
            {"id": "STU001", "name": "Alex Morgan", "gender": "Male", "course": "Computer Science", "phone": "+1 555-0101", "email": "alex@university.edu", "status": "Active"},
            {"id": "STU002", "name": "Emma Watson", "gender": "Female", "course": "Data Science", "phone": "+1 555-0102", "email": "emma@university.edu", "status": "Active"},
            {"id": "STU003", "name": "Liam Neeson", "gender": "Male", "course": "Cyber Security", "phone": "+1 555-0103", "email": "liam@university.edu", "status": "Inactive"},
            {"id": "STU004", "name": "Sophia Loren", "gender": "Female", "course": "Artificial Intelligence", "phone": "+1 555-0104", "email": "sophia@university.edu", "status": "Active"},
            {"id": "STU005", "name": "Oliver Twist", "gender": "Male", "course": "Software Engineering", "phone": "+1 555-0105", "email": "oliver@university.edu", "status": "Inactive"},
        ]

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        """Creates the exact sidebar layout matching the dashboard."""
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.WHITE)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(4, weight=1)

        # Logo / Brand Section
        brand_label = ctk.CTkLabel(sidebar, text="EduManager", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.PRIMARY_BLUE)
        brand_label.grid(row=0, column=0, padx=30, pady=(30, 40), sticky="w")

        # Navigation Buttons
        dash_btn = ctk.CTkButton(sidebar, text="Dashboard", font=ctk.CTkFont(size=14), fg_color="transparent", text_color=self.TEXT_GRAY, anchor="w", height=40)
        dash_btn.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        students_btn = ctk.CTkButton(sidebar, text="Students", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PANEL_BG, text_color=self.PRIMARY_BLUE, anchor="w", height=40)
        students_btn.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        courses_btn = ctk.CTkButton(sidebar, text="Courses", font=ctk.CTkFont(size=14), fg_color="transparent", text_color=self.TEXT_GRAY, anchor="w", height=40)
        courses_btn.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Footer / Logout entry placement
        logout_btn = ctk.CTkButton(sidebar, text="Logout", font=ctk.CTkFont(size=14), fg_color="transparent", text_color=self.TEXT_GRAY, anchor="w", height=40)
        logout_btn.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def create_main_content(self):
        """Creates the top bar and main container area."""
        main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=self.BACKGROUND)
        main_container.grid(row=0, column=1, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)

        # 1. Top Bar
        top_bar = ctk.CTkFrame(main_container, height=70, corner_radius=0, fg_color=self.WHITE)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        
        page_title = ctk.CTkLabel(top_bar, text="Students Management", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.TEXT_DARK)
        page_title.grid(row=0, column=0, padx=30, pady=20, sticky="w")
        
        user_profile = ctk.CTkLabel(top_bar, text="Admin User", font=ctk.CTkFont(size=14), text_color=self.TEXT_GRAY)
        user_profile.grid(row=0, column=1, padx=30, pady=20, sticky="e")

        # 2. Top Action Bar Frame
        action_bar = ctk.CTkFrame(main_container, fg_color="transparent")
        action_bar.grid(row=1, column=0, padx=30, pady=(25, 15), sticky="ew")
        action_bar.grid_columnconfigure(0, weight=1)

        search_entry = ctk.CTkEntry(action_bar, placeholder_text="Search Student...", width=300, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, text_color=self.TEXT_DARK)
        search_entry.grid(row=0, column=0, sticky="w")

        add_btn = ctk.CTkButton(action_bar, text="+ Add Student", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE, height=40)
        add_btn.grid(row=0, column=1, sticky="e")

        # 3. Student Table Container Matrix Frame
        table_container = ctk.CTkFrame(main_container, fg_color=self.WHITE, corner_radius=8)
        table_container.grid(row=2, column=0, padx=30, pady=(0, 30), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # Table Header Setup
        headers = ["Student ID", "Full Name", "Gender", "Course", "Phone", "Email", "Status", "Actions"]
        columns_width = [100, 150, 90, 160, 120, 180, 100, 160]

        header_frame = ctk.CTkFrame(table_container, fg_color=self.PANEL_BG, height=45, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        
        for idx, header in enumerate(headers):
            header_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])
            lbl = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            lbl.grid(row=0, column=idx, padx=15, pady=10, sticky="ew")

        # Table Body Contents inside CTkScrollableFrame
        self.scroll_frame = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        
        for idx in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])

        self.populate_table_data()

    def populate_table_data(self):
        """Populates the rows within the scrollable frame layer."""
        for row_idx, student in enumerate(self.students_data):
            # Design a subtle wrapper/separator line row structure logic implicitly by pacing rows
            # Alternating styles or generic borders can be simulated, but cleaner to use strict clean geometry configs
            
            id_lbl = ctk.CTkLabel(self.scroll_frame, text=student["id"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            id_lbl.grid(row=row_idx, column=0, padx=15, pady=12, sticky="ew")

            name_lbl = ctk.CTkLabel(self.scroll_frame, text=student["name"], font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            name_lbl.grid(row=row_idx, column=1, padx=15, pady=12, sticky="ew")

            gender_lbl = ctk.CTkLabel(self.scroll_frame, text=student["gender"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            gender_lbl.grid(row=row_idx, column=2, padx=15, pady=12, sticky="ew")

            course_lbl = ctk.CTkLabel(self.scroll_frame, text=student["course"], font=ctk.CTkFont(size=13), text_color=self.TEXT_DARK, anchor="w")
            course_lbl.grid(row=row_idx, column=3, padx=15, pady=12, sticky="ew")

            phone_lbl = ctk.CTkLabel(self.scroll_frame, text=student["phone"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            phone_lbl.grid(row=row_idx, column=4, padx=15, pady=12, sticky="ew")

            email_lbl = ctk.CTkLabel(self.scroll_frame, text=student["email"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            email_lbl.grid(row=row_idx, column=5, padx=15, pady=12, sticky="ew")

            # Status badge frame rendering logic
            status_text = student["status"]
            badge_color = self.SUCCESS_GREEN if status_text == "Active" else self.DANGER_RED
            
            status_badge = ctk.CTkFrame(self.scroll_frame, fg_color=badge_color, corner_radius=12, width=75, height=24)
            status_badge.grid(row=row_idx, column=6, padx=15, pady=12, sticky="w")
            status_badge.grid_propagate(False)
            
            status_lbl = ctk.CTkLabel(status_badge, text=status_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=self.WHITE)
            status_lbl.place(relx=0.5, rely=0.5, anchor="center")

            # Action Buttons Panel Group Wrapper Layout 
            action_panel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            action_panel.grid(row=row_idx, column=7, padx=15, pady=12, sticky="ew")

            view_btn = ctk.CTkButton(action_panel, text="View", font=ctk.CTkFont(size=11), fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, width=42, height=24, corner_radius=4)
            view_btn.grid(row=0, column=0, padx=2)

            edit_btn = ctk.CTkButton(action_panel, text="Edit", font=ctk.CTkFont(size=11), fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, width=42, height=24, corner_radius=4)
            edit_btn.grid(row=0, column=1, padx=2)

            delete_btn = ctk.CTkButton(action_panel, text="Delete", font=ctk.CTkFont(size=11), fg_color="#FEE2E2", hover_color="#FCA5A5", text_color=self.DANGER_RED, width=46, height=24, corner_radius=4)
            delete_btn.grid(row=0, column=2, padx=2)

if __name__ == "__main__":
    app = StudentsPage()
    app.mainloop()

    