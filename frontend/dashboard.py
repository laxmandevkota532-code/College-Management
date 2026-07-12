import customtkinter as ctk
from frontend.student_management_page import StudentManagementPage
from frontend.course_management_page import CoursesPage
from frontend.teachers_management_page import TeachersPage
from frontend.attendance_page import AttendancePage
from frontend.reports_page import ReportsPage
from frontend.setting_page import SettingsPage
from frontend.add_student_page import AddStudentPage
from frontend.student_view_page import ViewStudentPage
from frontend.student_edit_page import EditStudentPage
from frontend.add_course_page import AddCoursePage
from frontend.course_view_page import ViewCoursePage
from frontend.add_teacher_page import AddTeacherPage
from frontend.teacher_view_page import ViewTeacherPage
from backend.dashboard_crud import (
    get_total_students,
    get_total_courses,
    get_total_teachers,
    get_attendance_rate,
    get_recent_students
)

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

class DashboardHomePage(ctk.CTkScrollableFrame):
    """Reusable page class for the main dashboard overview."""
    def __init__(
        self,
        master,
        open_add_student_callback=None,
        open_add_course_callback=None
    ):
        super().__init__(master, fg_color=BACKGROUND, corner_radius=0)
        
        # Store the callback as an instance variable
        self.open_add_student_callback = open_add_student_callback
        self.open_add_course_callback = open_add_course_callback
        
        # Inner padding for the page content
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=30, pady=25)

        # Header Title
        content_title = ctk.CTkLabel(
            self.container, 
            text="Dashboard Overview", 
            font=("Helvetica", 24, "bold"), 
            text_color=TEXT_DARK
        )
        content_title.pack(anchor="w", pady=(0, 20))

        # --- Statistics Configuration Layer Grid ---
        stats_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 30))
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1, uniform="stat_card")

        # Load Dashboard Statistics
        total_students = get_total_students()
        total_courses = get_total_courses()
        total_teachers = get_total_teachers()
        attendance_rate = get_attendance_rate()

        stats_data = [
            ("Total Students", str(total_students), 0),
            ("Total Courses", str(total_courses), 1),
            ("Total Teachers", str(total_teachers), 2),
            ("Attendance Rate", f"{attendance_rate}%", 3)
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
        split_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        split_frame.pack(fill="both", expand=True)
        split_frame.grid_columnconfigure(0, weight=3, uniform="split_pane")
        split_frame.grid_columnconfigure(1, weight=1, uniform="split_pane")

        # Left Container: Recent Students Struct
        table_container = ctk.CTkFrame(split_frame, fg_color=WHITE, corner_radius=12, border_width=1, border_color="#E5E7EB")
        table_container.grid(row=0, column=0, padx=(0, 12), sticky="nsew")

        ctk.CTkLabel(table_container, text="Recent Students", font=("Helvetica", 16, "bold"), text_color=TEXT_DARK).pack(anchor="w", pady=(15, 15), padx=20)

        # Table Header Layout Config
        headers = ["Student ID", "Name", "Course", "Email", "Status"]
        hdr_frame = ctk.CTkFrame(table_container, fg_color=PANEL_BG, height=35, corner_radius=6)
        hdr_frame.pack(fill="x", pady=(0, 8), padx=20)
        for idx, h_text in enumerate(headers):
            hdr_frame.grid_columnconfigure(idx, weight=1, uniform="tbl_col")
            ctk.CTkLabel(hdr_frame, text=h_text, font=("Helvetica", 12, "bold"), text_color=TEXT_DARK).grid(row=0, column=idx, sticky="w", padx=10, pady=5)

        # Live Student Data from Database
        student_records = get_recent_students()

        # Populate Rows Inline
        if not student_records:
            ctk.CTkLabel(
                table_container,
                text="No Students Found",
                font=("Helvetica", 13),
                text_color=TEXT_GRAY
            ).pack(pady=20, padx=20)
        else:
            for row_idx, data in enumerate(student_records):
                row_frame = ctk.CTkFrame(table_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=4, padx=20)
                
                for col_idx, text_val in enumerate(data):
                    row_frame.grid_columnconfigure(col_idx, weight=1, uniform="tbl_col")
                    
                    if col_idx == 4:  # Status

                        if str(text_val).lower() == "active":
                            badge_fg = "#D1FAE5"
                            badge_text = "#10B981"
                        else:
                            badge_fg = "#FEE2E2"
                            badge_text = "#EF4444"

                        lbl = ctk.CTkLabel(
                            row_frame,
                            text=text_val,
                            font=("Helvetica", 12, "bold"),
                            text_color=badge_text,
                            fg_color=badge_fg,
                            corner_radius=6,
                            width=70,
                            height=22
                         )

                        lbl.grid(row=0, column=col_idx, sticky="w", padx=10, pady=5)
                    else:
                        ctk.CTkLabel(row_frame, text=text_val, font=("Helvetica", 13), text_color=TEXT_DARK).grid(row=0, column=col_idx, sticky="w", padx=10, pady=5)

                # Horizontal separation grid rule lines
                if row_idx < len(student_records) - 1:
                    ctk.CTkFrame(table_container, fg_color="#F3F4F6", height=1).pack(fill="x", pady=2, padx=20)

        # Right Container: Quick Actions Grid Setup
        actions_container = ctk.CTkFrame(split_frame, fg_color=WHITE, corner_radius=12, border_width=1, border_color="#E5E7EB")
        actions_container.grid(row=0, column=1, padx=(12, 0), sticky="nsew")

        ctk.CTkLabel(actions_container, text="Quick Actions", font=("Helvetica", 16, "bold"), text_color=TEXT_DARK).pack(anchor="w", pady=(15, 15), padx=20)

        actions_list = [
            ("➕ Add Student", self.action_add_student),
            ("📚 Add Course", self.action_add_course),
            ("📊 Generate Report", self.action_gen_report),
            ("📅 Attendance Tracking", self.action_take_attendance)
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

    # --- QUICK UTILITY INTERACTION EVENT METHODS ---
    def action_add_student(self):
        if self.open_add_student_callback:
            self.open_add_student_callback()
    
    def action_add_course(self):
        if self.open_add_course_callback:
            self.open_add_course_callback()
    
    def action_gen_report(self): 
        print("Action: Generate Report Launched")
    
    def action_take_attendance(self): 
        print("Action: Attendance Launched")


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)
        self.pack(fill="both", expand=True)

        # Configure Main Layout Grid (Sidebar on Left, Main Window Content on Right)
        self.grid_columnconfigure(0, weight=0, minsize=250)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_buttons = {}
        self.content_frame = None

        # Build structural interface segments
        self.create_sidebar()
        
        # Right Side Container (Holds Top Bar + Content Canvas)
        self.right_container = ctk.CTkFrame(self, fg_color=BACKGROUND, corner_radius=0)
        self.right_container.grid(row=0, column=1, sticky="nsew")
        self.right_container.grid_columnconfigure(0, weight=1)
        self.right_container.grid_rowconfigure(1, weight=1)
        
        self.create_top_bar()
        
        # Load default page
        self.menu_dashboard()

    def show_page(self, page_class):
        """Generic method to clear current content and load a new page."""
        if self.content_frame is not None:
            self.content_frame.destroy()

        self.content_frame = page_class(self.right_container)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def set_active_menu(self, active_text):
        """Updates the styling of sidebar buttons based on active selection."""
        for text, btn in self.menu_buttons.items():
            if text == active_text:
                btn.configure(
                    fg_color=PRIMARY_BLUE,
                    text_color=WHITE,
                    hover_color=HOVER_BLUE,
                    font=("Helvetica", 14, "bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT_DARK,
                    hover_color=PANEL_BG,
                    font=("Helvetica", 14, "normal")
                )

    def create_sidebar(self):
        """Creates the static Left Navigation Panel."""
        self.sidebar = ctk.CTkFrame(self, fg_color=WHITE, width=250, corner_radius=0, border_width=1, border_color="#E5E7EB")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # System Logo Header
        logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="🎓 Student System", 
            font=("Helvetica", 18, "bold"), 
            text_color=PRIMARY_BLUE
        )
        logo_label.pack(pady=(30, 40), padx=20, anchor="w")

        # Menu Navigation Items Array Config
        menu_items = [
            ("🏠 Dashboard", self.menu_dashboard),
            ("👨‍🎓 Students", self.menu_students),
            ("📚 Courses", self.menu_courses),
            ("👨‍🏫 Teachers", self.menu_teachers),
            ("📅 Attendance", self.menu_attendance),
            ("📊 Reports", self.menu_reports),
            ("⚙ Settings", self.menu_settings)
        ]

        # Generate Menu Navigation Layout Buttons
        for text, command in menu_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                font=("Helvetica", 14, "normal"),
                fg_color="transparent",
                text_color=TEXT_DARK,
                hover_color=PANEL_BG,
                height=45,
                corner_radius=8,
                anchor="w",
                command=command
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.menu_buttons[text] = btn

        # Bottom Structural Exit Element
        logout_btn = ctk.CTkButton(
            self.sidebar,
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

    # --- SIDEBAR INTERACTION EVENT METHODS ---
    
    def menu_dashboard(self):
        self.set_active_menu("🏠 Dashboard")

        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = DashboardHomePage(
            self.right_container,
            open_add_student_callback=self.open_add_student_from_dashboard,
            open_add_course_callback=self.open_add_course_from_dashboard
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
    def menu_students(self):
        self.set_active_menu("👨‍🎓 Students")

        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = StudentManagementPage(
            self.right_container,
            open_add_student_callback=self.open_add_student_from_students,
            open_view_student_callback=self.open_view_student,
            open_edit_student_callback=self.open_edit_student
        )   

        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
    def menu_courses(self):
        self.set_active_menu("📚 Courses")

        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = CoursesPage(
            self.right_container,
            open_add_course_callback=self.open_add_course_from_courses,
            open_view_course_callback=self.open_view_course
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
    def menu_teachers(self): 
        self.set_active_menu("👨‍🏫 Teachers")

        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = TeachersPage(
            self.right_container,
            open_add_teacher_callback=self.open_add_teacher_from_teachers,
            open_view_teacher_callback=self.open_view_teacher,
            open_edit_teacher_callback=self.open_edit_teacher
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")
        
    def menu_attendance(self): 
        self.set_active_menu("📅 Attendance")
        self.show_page(AttendancePage)
        
    def menu_reports(self): 
        self.set_active_menu("📊 Reports")
        self.show_page(ReportsPage)
        
    def menu_settings(self): 
        self.set_active_menu("⚙ Settings")
        self.show_page(SettingsPage)
        
    # ---------------------------------------------------------
    # CHANGED METHOD — the only logic change in this whole file
    # ---------------------------------------------------------
    def menu_logout(self):
        """Confirms logout, destroys the DashboardPage frame, and
        rebuilds LoginPage on the SAME root window (no new window)."""
        import tkinter.messagebox as messagebox
        from frontend.login import LoginPage  # local import avoids circular import with login_page.py

        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if confirm:
            root = self.winfo_toplevel()  # the single ctk.CTk() window shared by Login and Dashboard
            self.destroy()                # remove DashboardPage and everything nested inside it
            LoginPage(root)                # rebuild the login UI directly on that same root
    # ---------------------------------------------------------
    
    def open_add_student_from_dashboard(self):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = AddStudentPage(
            self.right_container,
            back_callback=self.menu_dashboard
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_add_student_from_students(self):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = AddStudentPage(
            self.right_container,
            back_callback=self.menu_students
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_view_student(self, student):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = ViewStudentPage(
            self.right_container,
            student_data=student,
            back_callback=self.menu_students
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_edit_student(self, student):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = EditStudentPage(
            self.right_container,
            student_data=student,
            back_callback=self.menu_students
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_add_course_from_dashboard(self):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = AddCoursePage(
            self.right_container,
            back_callback=self.menu_dashboard
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_add_course_from_courses(self):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = AddCoursePage(
            self.right_container,
            back_callback=self.menu_courses
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_view_course(self, course):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = ViewCoursePage(
            self.right_container,
            course_data=course,
            back_callback=self.menu_courses
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_add_teacher_from_teachers(self):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = AddTeacherPage(
            self.right_container,
            back_callback=self.menu_teachers
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_view_teacher(self, teacher):
        if self.content_frame:
            self.content_frame.destroy()

        self.content_frame = ViewTeacherPage(
            self.right_container,
            teacher_data=teacher,
            back_callback=self.menu_teachers
        )

        self.content_frame.grid(row=1, column=0, sticky="nsew")

    def open_edit_teacher(self, teacher):
        print("Edit Teacher:", teacher)
        # Uncomment lines below when EditTeacherPage is built:
        # if self.content_frame:
        #     self.content_frame.destroy()
        #
        # from frontend.teacher_edit_page import EditTeacherPage
        # self.content_frame = EditTeacherPage(
        #     self.right_container,
        #     teacher_data=teacher,
        #     back_callback=self.menu_teachers
        # )
        #
        # self.content_frame.grid(row=1, column=0, sticky="nsew")