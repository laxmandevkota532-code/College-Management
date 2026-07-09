import customtkinter as ctk

class AddCoursePage(ctk.CTkFrame):
    def __init__(self, parent, back_callback=None, **kwargs):
        super().__init__(parent, fg_color="#F8F9FC", **kwargs)
        self.back_callback = back_callback

        # Styling Constants
        self.PRIMARY_BLUE = "#4F5BD5"
        self.HOVER_BLUE = "#3F4ACB"
        self.BACKGROUND = "#F8F9FC"
        self.CARD = "#FFFFFF"
        self.TEXT_DARK = "#111827"
        self.TEXT_GRAY = "#6B7280"
        self.BORDER = "#E5E7EB"
        self.FONT_FAMILY = "Segoe UI"

        # Initialize form string variables
        self.course_id_var = ctk.StringVar(value="CRS-2026-042")
        self.course_name_var = ctk.StringVar()
        self.course_code_var = ctk.StringVar()
        self.department_var = ctk.StringVar()
        self.credit_hours_var = ctk.StringVar(value="3")
        self.semester_var = ctk.StringVar(value="Semester 1")
        self.course_type_var = ctk.StringVar(value="Theory")
        self.instructor_var = ctk.StringVar()
        self.max_students_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Active")

        # Set up grid layout for the page
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Body (Form & Summary)
        self.grid_rowconfigure(2, weight=0)  # Footer Buttons
        self.grid_columnconfigure(0, weight=1)

        # Traces for dynamic summary updates
        self.course_id_var.trace_add("write", lambda *args: self.update_summary())
        self.department_var.trace_add("write", lambda *args: self.update_summary())
        self.semester_var.trace_add("write", lambda *args: self.update_summary())
        self.credit_hours_var.trace_add("write", lambda *args: self.update_summary())
        self.status_var.trace_add("write", lambda *args: self.update_summary())

        # Build UI Components
        self.build_header()
        self.build_body()
        self.create_buttons()
        self.populate_form()
        self.update_summary()

    def build_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=32, pady=(24, 16))
        header_frame.grid_columnconfigure(0, weight=1)

        # Back Button Architecture
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color=self.PRIMARY_BLUE,
            fg_color="transparent",
            hover_color="#EEF0F6",
            width=80,
            height=32,
            corner_radius=6,
            command=self.go_back
        )
        back_btn.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Title and Subtitle
        title_label = ctk.CTkLabel(
            header_frame,
            text="Add New Course",
            font=(self.FONT_FAMILY, 28, "bold"),
            text_color=self.TEXT_DARK
        )
        title_label.grid(row=1, column=0, sticky="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Create a new course for students.",
            font=(self.FONT_FAMILY, 14),
            text_color=self.TEXT_GRAY
        )
        subtitle_label.grid(row=2, column=0, sticky="w", pady=(4, 0))

    def build_body(self):
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.grid(row=1, column=0, sticky="nsew", padx=32, pady=0)
        body_frame.grid_rowconfigure(0, weight=1)
        body_frame.grid_columnconfigure(0, weight=3)  # Left panel weight
        body_frame.grid_columnconfigure(1, weight=1)  # Right panel weight

        # Left Scrollable Form Panel
        self.form_container = ctk.CTkScrollableFrame(
            body_frame,
            fg_color=self.CARD,
            corner_radius=12,
            border_color=self.BORDER,
            border_width=1
        )
        self.form_container.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        self.form_container.grid_columnconfigure(0, weight=1)
        self.form_container.grid_columnconfigure(1, weight=1)

        # Right Summary Panel
        right_panel = ctk.CTkFrame(body_frame, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=0)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Card 1: Course Summary View
        self.summary_card = ctk.CTkFrame(right_panel, fg_color=self.CARD, corner_radius=12, border_color=self.BORDER, border_width=1)
        self.summary_card.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        self.summary_card.grid_columnconfigure(0, weight=1)

        summary_title = ctk.CTkLabel(self.summary_card, text="Course Summary", font=(self.FONT_FAMILY, 16, "bold"), text_color=self.TEXT_DARK)
        summary_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 12))

        # Dynamic fields container in summary
        self.summary_fields_frame = ctk.CTkFrame(self.summary_card, fg_color="transparent")
        self.summary_fields_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.summary_fields_frame.grid_columnconfigure(1, weight=1)

        # Card 2: Recently Added Courses
        recent_card = ctk.CTkFrame(right_panel, fg_color=self.CARD, corner_radius=12, border_color=self.BORDER, border_width=1)
        recent_card.grid(row=1, column=0, sticky="nsew")
        recent_card.grid_columnconfigure(0, weight=1)

        recent_title = ctk.CTkLabel(recent_card, text="Recently Added Courses", font=(self.FONT_FAMILY, 16, "bold"), text_color=self.TEXT_DARK)
        recent_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 12))

        # Dummy data container
        recent_list = ctk.CTkFrame(recent_card, fg_color="transparent")
        recent_list.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        recent_list.grid_columnconfigure(0, weight=1)

        dummy_courses = [
            {"code": "CS-101", "name": "Introduction to Computer Science", "dept": "Computer Science"},
            {"code": "MATH-201", "name": "Linear Algebra & Calculus", "dept": "Mathematics"},
            {"code": "ENG-104", "name": "Technical Writing Skills", "dept": "Humanities"}
        ]

        for idx, item in enumerate(dummy_courses):
            item_frame = ctk.CTkFrame(recent_list, fg_color="#F9FAFB", corner_radius=8, height=60)
            item_frame.grid(row=idx, column=0, sticky="ew", pady=4)
            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.grid_propagate(False)

            c_name = ctk.CTkLabel(item_frame, text=f"{item['code']} - {item['name']}", font=(self.FONT_FAMILY, 13, "bold"), text_color=self.TEXT_DARK, anchor="w")
            c_name.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 2))

            c_dept = ctk.CTkLabel(item_frame, text=item["dept"], font=(self.FONT_FAMILY, 11), text_color=self.TEXT_GRAY, anchor="w")
            c_dept.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))

    def populate_form(self):
        # Row 0: Course ID & Course Code
        self.create_entry(self.form_container, "Course ID (Read Only)", self.course_id_var, row=0, col=0, readonly=True)
        self.create_entry(self.form_container, "Course Code", self.course_code_var, row=0, col=1)

        # Row 1: Course Name Full Width
        self.create_entry(self.form_container, "Course Name", self.course_name_var, row=1, col=0, columnspan=2)

        # Row 2: Department & Credit Hours
        self.create_entry(self.form_container, "Department", self.department_var, row=2, col=0)
        self.create_combobox(self.form_container, "Credit Hours", self.credit_hours_var, ["1", "2", "3", "4", "5", "6"], row=2, col=1)

        # Row 3: Semester & Course Type
        semesters = [f"Semester {i}" for i in range(1, 9)]
        self.create_combobox(self.form_container, "Semester", self.semester_var, semesters, row=3, col=0)
        self.create_combobox(self.form_container, "Course Type", self.course_type_var, ["Theory", "Practical", "Lab", "Both"], row=3, col=1)

        # Row 4: Instructor & Max Students
        self.create_entry(self.form_container, "Instructor Name", self.instructor_var, row=4, col=0)
        self.create_entry(self.form_container, "Maximum Students", self.max_students_var, row=4, col=1)

        # Row 5: Status
        self.create_combobox(self.form_container, "Status", self.status_var, ["Active", "Inactive"], row=5, col=0)

        # Row 6: Description Full Width
        self.create_textbox(self.form_container, "Description", row=6, col=0, columnspan=2)

    def create_entry(self, parent, label_text, variable, row, col, columnspan=1, readonly=False):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=row, column=col, columnspan=columnspan, sticky="ew", padx=16, pady=12)
        container.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(container, text=label_text, font=(self.FONT_FAMILY, 13, "bold"), text_color=self.TEXT_DARK)
        label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        entry = ctk.CTkEntry(
            container,
            textvariable=variable,
            font=(self.FONT_FAMILY, 14),
            height=40,
            fg_color="#F9FAFB" if readonly else self.CARD,
            border_color=self.BORDER,
            text_color=self.TEXT_GRAY if readonly else self.TEXT_DARK,
            corner_radius=8
        )
        if readonly:
            entry.configure(state="readonly")
        entry.grid(row=1, column=0, sticky="ew")

    def create_combobox(self, parent, label_text, variable, values, row, col, columnspan=1):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=row, column=col, columnspan=columnspan, sticky="ew", padx=16, pady=12)
        container.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(container, text=label_text, font=(self.FONT_FAMILY, 13, "bold"), text_color=self.TEXT_DARK)
        label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        combobox = ctk.CTkComboBox(
            container,
            values=values,
            variable=variable,
            font=(self.FONT_FAMILY, 14),
            dropdown_font=(self.FONT_FAMILY, 13),
            height=40,
            fg_color=self.CARD,
            border_color=self.BORDER,
            button_color=self.BORDER,
            button_hover_color=self.TEXT_GRAY,
            text_color=self.TEXT_DARK,
            corner_radius=8,
            command=lambda choice: variable.set(choice)
        )
        combobox.grid(row=1, column=0, sticky="ew")

    def create_textbox(self, parent, label_text, row, col, columnspan=1):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=row, column=col, columnspan=columnspan, sticky="ew", padx=16, pady=12)
        container.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(container, text=label_text, font=(self.FONT_FAMILY, 13, "bold"), text_color=self.TEXT_DARK)
        label.grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.description_text = ctk.CTkTextbox(
            container,
            font=(self.FONT_FAMILY, 14),
            height=100,
            fg_color=self.CARD,
            border_color=self.BORDER,
            border_width=1,
            text_color=self.TEXT_DARK,
            corner_radius=8
        )
        self.description_text.grid(row=1, column=0, sticky="ew")

    def create_buttons(self):
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=32, pady=24)
        action_frame.grid_columnconfigure(0, weight=1)

        # Left aligned Clear button
        clear_btn = ctk.CTkButton(
            action_frame,
            text="Clear Fields",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color=self.TEXT_DARK,
            fg_color=self.CARD,
            hover_color="#F3F4F6",
            border_color=self.BORDER,
            border_width=1,
            width=120,
            height=44,
            corner_radius=8,
            command=self.clear_fields
        )
        clear_btn.grid(row=0, column=0, sticky="w")

        # Right aligned Save Course button
        save_btn = ctk.CTkButton(
            action_frame,
            text="Save Course",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#FFFFFF",
            fg_color=self.PRIMARY_BLUE,
            hover_color=self.HOVER_BLUE,
            width=140,
            height=44,
            corner_radius=8,
            command=self.save_course
        )
        save_btn.grid(row=0, column=1, sticky="e")

    def update_summary(self):
        # Clear current components inside summary dynamically
        for widget in self.summary_fields_frame.winfo_children():
            widget.destroy()

        summary_data = [
            ("Course ID", self.course_id_var.get()),
            ("Department", self.department_var.get() if self.department_var.get() else "Not Specified"),
            ("Semester", self.semester_var.get()),
            ("Credits", f"{self.credit_hours_var.get()} Credits")
        ]

        # Populate summary rows
        for idx, (label, val) in enumerate(summary_data):
            lbl_widget = ctk.CTkLabel(self.summary_fields_frame, text=label, font=(self.FONT_FAMILY, 12), text_color=self.TEXT_GRAY, anchor="w")
            lbl_widget.grid(row=idx, column=0, sticky="w", pady=6)

            val_widget = ctk.CTkLabel(self.summary_fields_frame, text=val, font=(self.FONT_FAMILY, 13, "bold"), text_color=self.TEXT_DARK, anchor="e")
            val_widget.grid(row=idx, column=1, sticky="e", pady=6)

        # Status Badge Implementation
        status_idx = len(summary_data)
        lbl_status = ctk.CTkLabel(self.summary_fields_frame, text="Status", font=(self.FONT_FAMILY, 12), text_color=self.TEXT_GRAY, anchor="w")
        lbl_status.grid(row=status_idx, column=0, sticky="w", pady=8)

        is_active = self.status_var.get() == "Active"
        badge_bg = "#E6F4EA" if is_active else "#FCE8E6"
        badge_fg = "#137333" if is_active else "#C5221F"

        badge = ctk.CTkLabel(
            self.summary_fields_frame,
            text=self.status_var.get().upper(),
            font=(self.FONT_FAMILY, 11, "bold"),
            text_color=badge_fg,
            fg_color=badge_bg,
            corner_radius=6,
            padx=10,
            pady=2
        )
        badge.grid(row=status_idx, column=1, sticky="e", pady=8)

    def clear_fields(self):
        self.course_name_var.set("")
        self.course_code_var.set("")
        self.department_var.set("")
        self.credit_hours_var.set("3")
        self.semester_var.set("Semester 1")
        self.course_type_var.set("Theory")
        self.instructor_var.set("")
        self.max_students_var.set("")
        self.status_var.set("Active")
        if hasattr(self, 'description_text'):
            self.description_text.delete("1.0", "end")
        self.update_summary()

    def save_course(self):
        print("Course Saved")

    def go_back(self):
        if self.back_callback:
            self.back_callback()
        else:
            print("Back button pressed")


# ==================================================
# TEST RUNNER
# ==================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    
    app = ctk.CTk()
    app.title("Test - Add Course Page")
    app.geometry("1000x700")
    app.configure(fg_color="#F8F9FC")
    
    # Configure grid to make the frame fill the window
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    
    # Initialize and pack the AddCoursePage
    page = AddCoursePage(app)
    page.grid(row=0, column=0, sticky="nsew")
    
    app.mainloop()