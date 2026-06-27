import customtkinter as ctk

# ── Navigation imports ───────────────────────────────────────────────────────
from student_management_page import StudentManagementPage
# from settings_page import SettingsPage

# Color Palette Configuration
PRIMARY_BLUE = "#4F5BD5"
HOVER_BLUE = "#3F4ACB"
BACKGROUND = "#F8F9FC"
PANEL_BG = "#EEF2FF"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6B7280"
WHITE = "#FFFFFF"

# Global CustomTkinter Settings
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)
        self.pack(fill="both", expand=True)

        # Configure Main Layout Grid (Sidebar on Left, Main Window Content on Right)
        self.grid_columnconfigure(0, weight=0, minsize=250)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Build structural interface segments
        self.create_sidebar()

        # Right Side Container (Holds Top Bar + Content Canvas)
        self.right_container = ctk.CTkFrame(self, fg_color=BACKGROUND, corner_radius=0)
        self.right_container.grid(row=0, column=1, sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)

        self.create_top_bar()
        self.create_main_content()

    def create_sidebar(self):
        """Creates the static Left Navigation Panel."""
        sidebar = ctk.CTkFrame(self, fg_color=WHITE, width=250, corner_radius=0, border_width=1, border_color="#E5E7EB")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # System Logo Header
        logo_label = ctk.CTkLabel(
            sidebar,
            text="🎓 Student System",
            font=("Helvetica", 18, "bold"),
            text_color=PRIMARY_BLUE
        )
        logo_label.pack(pady=(30, 40), padx=20, anchor="w")

        # Menu Navigation Items — simplified to Dashboard, Students, Settings only
        menu_items = [
            ("🏠 Dashboard", self.menu_dashboard, True),
            ("👨‍🎓 Students", self.menu_students, False),
            ("⚙ Settings", self.menu_settings, False),
        ]

        # Generate Menu Navigation Layout Buttons
        for text, command, is_active in menu_items:
            fg = PRIMARY_BLUE if is_active else "transparent"
            text_col = WHITE if is_active else TEXT_DARK
            hover_col = HOVER_BLUE if is_active else PANEL_BG

            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=("Helvetica", 14, "bold" if is_active else "normal"),
                fg_color=fg,
                text_color=text_col,
                hover_color=hover_col,
                height=45,
                corner_radius=8,
                anchor="w",
                command=command
            )
            btn.pack(fill="x", padx=15, pady=4)

        # Bottom Structural Exit Element
        logout_btn = ctk.CTkButton(
            sidebar,
            text="🚪 Logout",
            font=("Helvetica", 14),
            fg_color="transparent",
            text_color="#EF4444",
            hover_color="#FEE2E2",
            height=45,
            corner_radius=8,
            anchor="w",
            command=self.menu_logout
        )
        logout_btn.pack(side="bottom", fill="x", padx=15, pady=30)

    def create_top_bar(self):
        """Creates the functional header section layer."""
        top_bar = ctk.CTkFrame(self.right_container, fg_color=WHITE, height=80, corner_radius=0, border_width=1, border_color="#E5E7EB")
        top_bar.grid(row=0, column=0, sticky="nsew")
        top_bar.pack_propagate(False)

        # Left Module Segment Title Indicator
        title_label = ctk.CTkLabel(
            top_bar,
            text="Dashboard",
            font=("Helvetica", 20, "bold"),
            text_color=TEXT_DARK
        )
        title_label.pack(side="left", padx=30, pady=25)

        # Right Interaction Dashboard Utilities Grouping Frame
        right_utility_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_utility_frame.pack(side="right", padx=30, pady=15)

        search_entry = ctk.CTkEntry(
            right_utility_frame,
            placeholder_text="Search anything...",
            font=("Helvetica", 13),
            width=220,
            height=40,
            corner_radius=8,
            border_color="#D1D5DB"
        )
        search_entry.pack(side="left", padx=(0, 15))

        notif_btn = ctk.CTkButton(
            right_utility_frame,
            text="🔔",
            font=("Helvetica", 16),
            fg_color=PANEL_BG,
            text_color=TEXT_DARK,
            hover_color="#E0E7FF",
            width=40,
            height=40,
            corner_radius=8
        )
        notif_btn.pack(side="left", padx=(0, 10))

        profile_btn = ctk.CTkButton(
            right_utility_frame,
            text="👤 Admin",
            font=("Helvetica", 13, "bold"),
            fg_color=PANEL_BG,
            text_color=TEXT_DARK,
            hover_color="#E0E7FF",
            height=40,
            corner_radius=8
        )
        profile_btn.pack(side="left")

    def create_main_content(self):
        """Creates and layouts the primary core user data canvas area."""
        # Scrollable container mapping layout to content safely
        scroll_canvas = ctk.CTkScrollableFrame(self.right_container, fg_color=BACKGROUND, corner_radius=0)
        scroll_canvas.grid(row=1, column=0, sticky="nsew", padx=30, pady=25)

        # Store reference so _swap_content_area can destroy it
        self.content_frame = scroll_canvas

        # Header Title
        content_title = ctk.CTkLabel(
            scroll_canvas,
            text="Dashboard Overview",
            font=("Helvetica", 24, "bold"),
            text_color=TEXT_DARK
        )
        content_title.pack(anchor="w", pady=(0, 20))

        # --- Statistics Configuration Layer Grid ---
        # Updated: Total Students / Active Students / Inactive Students only
        stats_frame = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 30))
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1, uniform="stat_card")

        stats_data = [
            ("Total Students", "1,250", 0),
            ("Active Students", "1,143", 1),
            ("Inactive Students", "107", 2),
        ]

        for title, value, col in stats_data:
            card = ctk.CTkFrame(stats_frame, fg_color=WHITE, corner_radius=12, border_width=1, border_color="#E5E7EB", height=110)
            card.grid(row=0, column=col, padx=8, sticky="nsew")
            card.pack_propagate(False)

            # Left vertical aesthetic accent marker strip
            accent = ctk.CTkFrame(card, fg_color=PRIMARY_BLUE, width=5, corner_radius=0)
            accent.pack(side="left", fill="y")

            card_body = ctk.CTkFrame(card, fg_color="transparent")
            card_body.pack(side="left", fill="both", expand=True, padx=15, pady=15)

            ctk.CTkLabel(card_body, text=title, font=("Helvetica", 13), text_color=TEXT_GRAY).pack(anchor="w")
            ctk.CTkLabel(card_body, text=value, font=("Helvetica", 26, "bold"), text_color=TEXT_DARK).pack(anchor="w", pady=(2, 0))

        # --- Split MidSection: Left Table vs Right Side Quick Utilities ---
        split_frame = ctk.CTkFrame(scroll_canvas, fg_color="transparent")
        split_frame.pack(fill="both", expand=True)
        split_frame.grid_columnconfigure(0, weight=3, uniform="split_pane")
        split_frame.grid_columnconfigure(1, weight=1, uniform="split_pane")

        # Left Container: Recent Students Struct
        table_container = ctk.CTkFrame(split_frame, fg_color=WHITE, corner_radius=12, border_width=1, border_color="#E5E7EB")
        table_container.grid(row=0, column=0, padx=(0, 12), sticky="nsew")

        ctk.CTkLabel(table_container, text="Recent Students", font=("Helvetica", 16, "bold"), text_color=TEXT_DARK).pack(anchor="w", pady=(20, 15), padx=20)

        # Table Header Layout Config — Student ID, Name, Course, Status, View
        headers = ["Student ID", "Name", "Course", "Status", "View"]
        hdr_frame = ctk.CTkFrame(table_container, fg_color=PANEL_BG, height=35, corner_radius=6)
        hdr_frame.pack(fill="x", pady=(0, 8), padx=20)
        for idx, h_text in enumerate(headers):
            hdr_frame.grid_columnconfigure(idx, weight=1, uniform="tbl_col")
            ctk.CTkLabel(hdr_frame, text=h_text, font=("Helvetica", 12, "bold"), text_color=TEXT_DARK).grid(row=0, column=idx, sticky="w", padx=10, pady=5)

        # Mock Student Data Sets
        student_records = [
            ("ST001", "John Doe", "BCA", "Active"),
            ("ST002", "Jane Smith", "BIT", "Active"),
            ("ST003", "Michael Johnson", "CSIT", "Active"),
            ("ST004", "Emily Brown", "BCA", "Inactive"),
        ]

        # Populate Rows Inline
        for row_idx, data in enumerate(student_records):
            row_frame = ctk.CTkFrame(table_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=4, padx=20)

            for col_idx in range(5):  # 5 columns including View button
                row_frame.grid_columnconfigure(col_idx, weight=1, uniform="tbl_col")

                if col_idx < 4:
                    text_val = data[col_idx]

                    if col_idx == 3:  # Status column
                        is_active = text_val == "Active"
                        lbl = ctk.CTkLabel(
                            row_frame,
                            text=text_val,
                            font=("Helvetica", 12, "bold"),
                            text_color="#10B981" if is_active else "#EF4444",
                            fg_color="#D1FAE5" if is_active else "#FEE2E2",
                            corner_radius=6,
                            width=65,
                            height=22
                        )
                        lbl.grid(row=0, column=col_idx, sticky="w", padx=10, pady=5)
                    else:
                        ctk.CTkLabel(row_frame, text=text_val, font=("Helvetica", 13), text_color=TEXT_DARK).grid(row=0, column=col_idx, sticky="w", padx=10, pady=5)

                else:  # View button column
                    view_btn = ctk.CTkButton(
                        row_frame,
                        text="View",
                        font=("Helvetica", 12, "bold"),
                        fg_color=PANEL_BG,
                        text_color=PRIMARY_BLUE,
                        hover_color="#E0E7FF",
                        width=55,
                        height=26,
                        corner_radius=6,
                        command=self.menu_students
                    )
                    view_btn.grid(row=0, column=col_idx, sticky="w", padx=10, pady=5)

            # Horizontal separation grid rule lines
            if row_idx < len(student_records) - 1:
                ctk.CTkFrame(table_container, fg_color="#F3F4F6", height=1).pack(fill="x", pady=2, padx=20)

        # Right Container: Quick Actions Grid Setup
        # Updated: Add Student / Student Management / Settings only
        actions_container = ctk.CTkFrame(split_frame, fg_color=WHITE, corner_radius=12, border_width=1, border_color="#E5E7EB")
        actions_container.grid(row=0, column=1, padx=(12, 0), sticky="nsew")

        ctk.CTkLabel(actions_container, text="Quick Actions", font=("Helvetica", 16, "bold"), text_color=TEXT_DARK).pack(anchor="w", pady=(20, 15), padx=20)

        actions_list = [
            ("➕ Add Student", self.menu_students),
            ("👨‍🎓 Student Management", self.menu_students),
            ("⚙ Settings", self.menu_settings),
        ]

        for act_text, act_cmd in actions_list:
            ctk.CTkButton(
                actions_container,
                text=act_text,
                font=("Helvetica", 13, "bold"),
                fg_color=PANEL_BG,
                text_color=PRIMARY_BLUE,
                hover_color="#E0E7FF",
                height=45,
                corner_radius=8,
                anchor="w",
                command=act_cmd
            ).pack(fill="x", pady=6, padx=20)

    # ── Navigation helper ────────────────────────────────────────────────────
    def _swap_content_area(self, new_widget_class, **kwargs):
        """Destroy current content frame and embed new_widget_class in its place."""
        self.content_frame.destroy()
        self.content_frame = new_widget_class(self.right_container, **kwargs)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

    # --- SIDEBAR INTERACTION EVENT METHODS ---
    def menu_dashboard(self):
        self.content_frame.destroy()
        self.create_main_content()

    def menu_students(self):
        self._swap_content_area(StudentManagementPage)

    def menu_settings(self):
        self._swap_content_area(SettingsPage)

    def menu_logout(self):
        print("Logout")


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Student Management System - Dashboard")

    # Process responsive scaling frame constraints cleanly
    root.configure(fg_color=BACKGROUND)
    root.after(100, lambda: root.state("zoomed"))

    # Initialize UI Component Canvas Instance
    app = DashboardPage(root)
    root.mainloop()