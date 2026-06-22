import customtkinter as ctk
import sys

# Set appearance mode and default color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class AttendancePage(ctk.CTk):
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
        self.title("Attendance Management System")
        self.geometry("1280x720")
        self.configure(fg_color=self.BACKGROUND)
        
        # Open in Full Screen automatically with fallback
        self.after(100, self.apply_fullscreen)
        
        # Responsive Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sample Data ---
        self.attendance_data = [
            {"id": "ST001", "name": "John Doe", "course": "BCA", "date": "2026-06-22", "status": "Present"},
            {"id": "ST002", "name": "Jane Smith", "course": "BIT", "date": "2026-06-22", "status": "Present"},
            {"id": "ST003", "name": "Michael Johnson", "course": "CSIT", "date": "2026-06-22", "status": "Absent"},
            {"id": "ST004", "name": "Emily Brown", "course": "BCA", "date": "2026-06-22", "status": "Present"},
            {"id": "ST005", "name": "David Wilson", "course": "BIT", "date": "2026-06-22", "status": "Absent"},
        ]

        self.create_sidebar()
        self.create_main_content()

    def apply_fullscreen(self):
        try:
            if sys.platform.startswith("win"):
                self.state("zoomed")
            else:
                self.attributes("-zoomed", True)
        except Exception:
            # Universal alternative fullscreen method if zoomed fails
            self.attributes("-fullscreen", True)

    def create_sidebar(self):
        """Creates the navigation sidebar matching the uniform design system."""
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
            if item == "Attendance":
                # Active State Styling
                btn = ctk.CTkButton(sidebar, text=item, font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PANEL_BG, text_color=self.PRIMARY_BLUE, anchor="w", height=40, corner_radius=6)
            else:
                # Passive State Styling
                btn = ctk.CTkButton(sidebar, text=item, font=ctk.CTkFont(size=14), fg_color="transparent", text_color=self.TEXT_GRAY, hover_color=self.PANEL_BG, anchor="w", height=40, corner_radius=6)
            
            btn.grid(row=idx, column=0, padx=20, pady=4, sticky="ew")

        # Fixed Logout Placement at Bottom
        logout_btn = ctk.CTkButton(sidebar, text="Logout", font=ctk.CTkFont(size=14), fg_color="transparent", text_color=self.TEXT_GRAY, hover_color=self.PANEL_BG, anchor="w", height=40, corner_radius=6)
        logout_btn.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

    def create_main_content(self):
        """Builds responsive layout area panel structures for main content."""
        main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=self.BACKGROUND)
        main_container.grid(row=0, column=1, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(3, weight=1)

        # 1. Top Bar Container Setup
        top_bar = ctk.CTkFrame(main_container, height=70, corner_radius=0, fg_color=self.WHITE)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_propagate(False)
        
        page_title = ctk.CTkLabel(top_bar, text="Attendance Management", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.TEXT_DARK)
        page_title.grid(row=0, column=0, padx=30, pady=20, sticky="w")
        
        user_profile = ctk.CTkLabel(top_bar, text="Admin User", font=ctk.CTkFont(size=14), text_color=self.TEXT_GRAY)
        user_profile.grid(row=0, column=1, padx=30, pady=20, sticky="e")

        # 2. Summary Cards Metrics Grid Section
        metrics_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        metrics_frame.grid(row=1, column=0, padx=30, pady=(25, 10), sticky="ew")
        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1, uniform="metrics_equal")

        cards_data = [
            {"title": "Total Students", "value": "1,250"},
            {"title": "Present Today", "value": "1,180"},
            {"title": "Absent Today", "value": "70"},
            {"title": "Attendance Rate", "value": "94%"}
        ]

        for idx, card in enumerate(cards_data):
            card_box = ctk.CTkFrame(metrics_frame, fg_color=self.WHITE, height=90, corner_radius=8)
            card_box.grid(row=0, column=idx, padx=(0 if idx == 0 else 10, 0 if idx == 3 else 10), sticky="ew")
            card_box.grid_propagate(False)
            
            # Fixed weight here: changed from "medium" to "normal"
            title_lbl = ctk.CTkLabel(card_box, text=card["title"], font=ctk.CTkFont(size=13, weight="normal"), text_color=self.TEXT_GRAY)
            title_lbl.grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")
            
            val_lbl = ctk.CTkLabel(card_box, text=card["value"], font=ctk.CTkFont(size=22, weight="bold"), text_color=self.TEXT_DARK)
            val_lbl.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # 3. Top Filters / Action Bar Layout Container
        action_bar = ctk.CTkFrame(main_container, fg_color="transparent")
        action_bar.grid(row=2, column=0, padx=30, pady=(15, 15), sticky="ew")
        action_bar.grid_columnconfigure(2, weight=1)

        course_dropdown = ctk.CTkOptionMenu(action_bar, values=["All Courses", "BCA", "BIT", "CSIT", "BBS", "BIM"], width=140, height=40, fg_color=self.PANEL_BG, button_color=self.PANEL_BG, button_hover_color="#E0E7FF", text_color=self.TEXT_DARK, font=ctk.CTkFont(size=13))
        course_dropdown.set("Select Course")
        course_dropdown.grid(row=0, column=0, padx=(0, 10), sticky="w")

        date_entry = ctk.CTkEntry(action_bar, placeholder_text="2026-06-22", width=130, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, text_color=self.TEXT_DARK)
        date_entry.grid(row=0, column=1, padx=(0, 10), sticky="w")

        search_entry = ctk.CTkEntry(action_bar, placeholder_text="Search Student ID or Name...", width=260, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, text_color=self.TEXT_DARK)
        search_entry.grid(row=0, column=2, sticky="w")

        mark_btn = ctk.CTkButton(action_bar, text="Mark Attendance", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE, height=40, corner_radius=6)
        mark_btn.grid(row=0, column=3, sticky="e")

        # 4. Central Layout Table Data Display Section
        table_container = ctk.CTkFrame(main_container, fg_color=self.WHITE, corner_radius=8)
        table_container.grid(row=3, column=0, padx=30, pady=(0, 30), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # Matrix Headers Configuration
        headers = ["Student ID", "Student Name", "Course", "Date", "Status"]
        self.columns_width = [150, 240, 180, 180, 150]

        header_frame = ctk.CTkFrame(table_container, fg_color=self.PANEL_BG, height=45, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        
        for idx, header in enumerate(headers):
            header_frame.grid_columnconfigure(idx, weight=1, minsize=self.columns_width[idx])
            lbl = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            lbl.grid(row=0, column=idx, padx=20, pady=10, sticky="ew")

        # Scrollable Frame Matrix Body Construction Injection
        self.scroll_frame = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        
        for idx in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(idx, weight=1, minsize=self.columns_width[idx])

        self.populate_table_data()

    def populate_table_data(self):
        """Renders raw arrays iteratively matching design systems guidelines precisely."""
        for row_idx, record in enumerate(self.attendance_data):
            
            id_lbl = ctk.CTkLabel(self.scroll_frame, text=record["id"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            id_lbl.grid(row=row_idx, column=0, padx=20, pady=12, sticky="ew")

            name_lbl = ctk.CTkLabel(self.scroll_frame, text=record["name"], font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            name_lbl.grid(row=row_idx, column=1, padx=20, pady=12, sticky="ew")

            course_lbl = ctk.CTkLabel(self.scroll_frame, text=record["course"], font=ctk.CTkFont(size=13), text_color=self.TEXT_DARK, anchor="w")
            course_lbl.grid(row=row_idx, column=2, padx=20, pady=12, sticky="ew")

            date_lbl = ctk.CTkLabel(self.scroll_frame, text=record["date"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            date_lbl.grid(row=row_idx, column=3, padx=20, pady=12, sticky="ew")

            # Status pill design geometry badge injection
            status_text = record["status"]
            badge_color = self.SUCCESS_GREEN if status_text == "Present" else self.DANGER_RED
            
            status_badge = ctk.CTkFrame(self.scroll_frame, fg_color=badge_color, corner_radius=12, width=85, height=24)
            status_badge.grid(row=row_idx, column=4, padx=20, pady=12, sticky="w")
            status_badge.grid_propagate(False)
            
            status_lbl = ctk.CTkLabel(status_badge, text=status_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=self.WHITE)
            status_lbl.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    app = AttendancePage()
    app.mainloop()

