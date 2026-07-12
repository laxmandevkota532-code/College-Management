import re
from datetime import datetime

import customtkinter as ctk
from tkinter import messagebox

from backend.student_crud import (
    generate_student_id,
    insert_student,
    get_recent_students,
    DuplicateStudentIDError,
    DuplicateEmailError,
)
from backend.course_crud import get_all_courses

# --------------------------------------------------
# BACKEND INTEGRATION NOTES
# --------------------------------------------------
# backend/student_crud.py exposes:
#   generate_student_id() -> str
#   insert_student(student_data: dict) -> None
#       expects keys: student_id, fullname, email, phone, dob, course,
#                     gender, address, status
#   get_recent_students(limit: int = 4) -> list[dict]
#       each dict has keys: student_id, fullname
#   DuplicateStudentIDError, DuplicateEmailError
#
# backend/course_crud.py exposes:
#   get_all_courses() -> list[dict]
#       each dict has key: course_name (among possibly others)

# --------------------------------------------------
# DESIGN SYSTEM CONSTANTS
# --------------------------------------------------
BACKGROUND = "#F8F9FC"
CARD = "#FFFFFF"

PRIMARY_BLUE = "#4F5BD5"
HOVER_BLUE = "#3F4ACB"

TEXT_DARK = "#111827"
TEXT_GRAY = "#6B7280"

BORDER = "#E5E7EB"

FONT = "Segoe UI"

# --------------------------------------------------
# VALIDATION PATTERNS
# --------------------------------------------------
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\+?[0-9()\-\s]{7,20}$")
DOB_FORMAT = "%Y-%m-%d"

# --------------------------------------------------
# PLACEHOLDER TEXT WHEN NO COURSES EXIST IN DATABASE
# --------------------------------------------------
NO_COURSES_PLACEHOLDER = "No Courses Available"


# --------------------------------------------------
# ADD STUDENT PAGE COMPONENT
# --------------------------------------------------
class AddStudentPage(ctk.CTkFrame):

    def __init__(self, master, back_callback=None, **kwargs):
        super().__init__(master, fg_color=BACKGROUND, **kwargs)

        # Store navigation callback
        self.back_callback = back_callback

        # Track form field widgets
        self.fields = {}

        # Reference to the scrollable "Recent Added Students" list container (set in build_body)
        self.recent_list_frame = None

        # Reference to the Save Student button (set in create_buttons), used to
        # enable/disable saving when no courses exist in the database
        self.save_btn = None

        # Tracks whether the database currently has at least one course available.
        # Set inside populate_form_fields() when the Course ComboBox is built.
        self.courses_available = True

        # Configure main full-page frame grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Top Header
        self.grid_rowconfigure(1, weight=1)  # Two-column Body Split

        # Component builder pipeline
        self.build_header()
        self.build_body()

    def go_back(self):
        """Triggers the navigation callback routing workflow back to the previous layout view."""
        if self.back_callback:
            self.back_callback()

    def set_back_callback(self, back_callback):
        """Dynamically updates the navigation callback when opened from different pages."""
        self.back_callback = back_callback

    def build_header(self):
        """Builds full-width top header with back button and breadcrumb layout information."""
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="ew", padx=40, pady=(30, 20))

        # Horizontal stacking layout setup
        header_container.grid_rowconfigure(0, weight=1)
        header_container.grid_columnconfigure(1, weight=1)

        # 1. Back button
        back_btn = ctk.CTkButton(
            header_container,
            text="← Back",
            font=(FONT, 14, "bold"),
            text_color=PRIMARY_BLUE,
            fg_color="transparent",
            hover_color=BORDER,
            width=80,
            height=36,
            corner_radius=6,
            command=self.go_back
        )
        back_btn.grid(row=0, column=0, sticky="w", padx=(0, 20))

        # 2. Text titles stack panel
        text_frame = ctk.CTkFrame(header_container, fg_color="transparent")
        text_frame.grid(row=0, column=1, sticky="w")

        title = ctk.CTkLabel(
            text_frame,
            text="Register New Student",
            font=(FONT, 24, "bold"),
            text_color=TEXT_DARK
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            text_frame,
            text="Fill student information below.",
            font=(FONT, 13),
            text_color=TEXT_GRAY
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    def build_body(self):
        """Constructs the responsive 70/30 main container layout grid split configuration."""
        body_container = ctk.CTkFrame(self, fg_color="transparent")
        body_container.grid(row=1, column=0, sticky="nsew", padx=40, pady=(0, 40))

        body_container.grid_rowconfigure(0, weight=1)
        body_container.grid_columnconfigure(0, weight=7)  # Left Column Form Panel (70%)
        body_container.grid_columnconfigure(1, weight=3)  # Right Column Side Panel (30%)

        # --------------------------------------------------
        # LEFT COLUMN: FORM PANEL CARD
        # --------------------------------------------------
        left_card = ctk.CTkFrame(
            body_container,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_card.grid_rowconfigure(0, weight=1)  # Form container fills workspace space
        left_card.grid_rowconfigure(1, weight=0)  # Fixed action buttons container area at bottom
        left_card.grid_columnconfigure(0, weight=1)

        # Scrollable form layout canvas viewport
        self.form_container = ctk.CTkScrollableFrame(
            left_card,
            fg_color="transparent",
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=TEXT_GRAY
        )
        self.form_container.grid(row=0, column=0, sticky="nsew", padx=35, pady=(25, 10))

        self.populate_form_fields()
        self.create_buttons(left_card)

        # Apply the Save button's enabled/disabled state now that both the
        # Course ComboBox (populate_form_fields) and Save button (create_buttons)
        # have been created.
        self.update_save_button_state()

        # --------------------------------------------------
        # RIGHT COLUMN: RECENT STUDENTS PANEL CARD
        # --------------------------------------------------
        right_card = ctk.CTkFrame(
            body_container,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )
        right_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        right_card.grid_columnconfigure(0, weight=1)

        recent_title = ctk.CTkLabel(
            right_card,
            text="Recent Added Students",
            font=(FONT, 16, "bold"),
            text_color=TEXT_DARK
        )
        recent_title.grid(row=0, column=0, sticky="w", padx=25, pady=(25, 15))

        # Container viewport list panel stack logic
        self.recent_list_frame = ctk.CTkFrame(right_card, fg_color="transparent")
        self.recent_list_frame.grid(row=1, column=0, sticky="ew", padx=25)
        self.recent_list_frame.grid_columnconfigure(0, weight=1)

        # Populate the panel with live data from the database
        self.refresh_recent_list()

    def refresh_recent_list(self):
        """Clears and repopulates the Recent Added Students panel using live database records."""
        if self.recent_list_frame is None:
            return

        # Clear any existing entries before re-rendering
        for widget in self.recent_list_frame.winfo_children():
            widget.destroy()

        recent_students = get_recent_students(limit=4)

        if not recent_students:
            empty_label = ctk.CTkLabel(
                self.recent_list_frame,
                text="No students added yet.",
                font=(FONT, 12),
                text_color=TEXT_GRAY
            )
            empty_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
            return

        for i, student in enumerate(recent_students):
            item_card = ctk.CTkFrame(
                self.recent_list_frame,
                fg_color=BACKGROUND,
                corner_radius=8,
                border_width=1,
                border_color=BORDER,
                height=65
            )
            item_card.grid(row=i, column=0, sticky="ew", pady=(0, 10))
            item_card.pack_propagate(False)

            lbl_id = ctk.CTkLabel(
                item_card,
                text=student.get("student_id", ""),
                font=(FONT, 11, "bold"),
                text_color=PRIMARY_BLUE
            )
            lbl_id.pack(anchor="w", padx=15, pady=(10, 0))

            lbl_name = ctk.CTkLabel(
                item_card,
                text=student.get("fullname", ""),
                font=(FONT, 13, "bold"),
                text_color=TEXT_DARK
            )
            lbl_name.pack(anchor="w", padx=15, pady=(0, 10))

    def load_course_names(self):
        """
        Fetches all courses from the database and extracts their course_name values.

        Returns:
            list[str]: A list of course names. Empty if no courses exist in the database.
        """
        courses = get_all_courses() or []
        return [course.get("course_name") for course in courses if course.get("course_name")]

    def populate_form_fields(self):
        """Renders grid structure form elements linearly down inside the viewport panel canvas container."""
        # 1. Student ID (Read Only, auto-generated by backend)
        initial_student_id = generate_student_id()

        self.create_label(self.form_container, "Student ID").pack(anchor="w", pady=(10, 4))
        self.fields["id"] = self.create_entry(self.form_container, placeholder=initial_student_id, readonly=True)
        self.fields["id"].pack(fill="x", pady=(0, 12))

        # 2. Full Name
        self.create_label(self.form_container, "Full Name").pack(anchor="w", pady=(10, 4))
        self.fields["name"] = self.create_entry(self.form_container, placeholder="John Doe")
        self.fields["name"].pack(fill="x", pady=(0, 12))

        # 3. Email Address
        self.create_label(self.form_container, "Email Address").pack(anchor="w", pady=(10, 4))
        self.fields["email"] = self.create_entry(self.form_container, placeholder="johndoe@example.com")
        self.fields["email"].pack(fill="x", pady=(0, 12))

        # 4. Phone Number
        self.create_label(self.form_container, "Phone Number").pack(anchor="w", pady=(10, 4))
        self.fields["phone"] = self.create_entry(self.form_container, placeholder="+1 (555) 012-3456")
        self.fields["phone"].pack(fill="x", pady=(0, 12))

        # 5. Date of Birth
        self.create_label(self.form_container, "Date of Birth").pack(anchor="w", pady=(10, 4))
        self.fields["dob"] = self.create_entry(self.form_container, placeholder="YYYY-MM-DD")
        self.fields["dob"].pack(fill="x", pady=(0, 12))

        # 6. Course Selection (dynamically loaded from the database)
        self.create_label(self.form_container, "Course").pack(anchor="w", pady=(10, 4))

        course_names = self.load_course_names()

        if course_names:
            # Courses exist: populate normally and mark the ComboBox as enabled
            self.fields["course"] = self.create_combobox(self.form_container, course_names)
            self.courses_available = True
        else:
            # No courses exist: show placeholder, disable the ComboBox, and warn the user
            self.fields["course"] = self.create_combobox(self.form_container, [NO_COURSES_PLACEHOLDER])
            self.fields["course"].configure(state="disabled")
            self.courses_available = False
            messagebox.showwarning(
                "No Courses Found",
                "Please add at least one course before registering a student."
            )

        self.fields["course"].pack(fill="x", pady=(0, 12))

        # 7. Gender Segment (Radio buttons)
        self.create_label(self.form_container, "Gender").pack(anchor="w", pady=(10, 6))
        gender_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        gender_frame.pack(fill="x", pady=(0, 12))

        self.gender_var = ctk.StringVar(value="Male")
        for gender in ["Male", "Female", "Other"]:
            radio = ctk.CTkRadioButton(
                gender_frame,
                text=gender,
                variable=self.gender_var,
                value=gender,
                font=(FONT, 13),
                text_color=TEXT_DARK,
                fg_color=PRIMARY_BLUE,
                hover_color=HOVER_BLUE
            )
            radio.pack(side="left", padx=(0, 24))

        # 8. Address Box
        self.create_label(self.form_container, "Address").pack(anchor="w", pady=(10, 4))
        self.fields["address"] = self.create_textbox(self.form_container)
        self.fields["address"].pack(fill="x", pady=(0, 12))

        # 9. Status Framework
        self.create_label(self.form_container, "Status").pack(anchor="w", pady=(10, 4))
        statuses = ["Active", "Inactive"]
        self.fields["status"] = self.create_combobox(self.form_container, statuses)
        self.fields["status"].pack(fill="x", pady=(0, 20))

    def create_label(self, parent, text):
        return ctk.CTkLabel(
            parent,
            text=text,
            font=(FONT, 13, "bold"),
            text_color=TEXT_DARK
        )

    def create_entry(self, parent, placeholder="", readonly=False):
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=(FONT, 13),
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT_DARK,
            placeholder_text_color=TEXT_GRAY
        )
        if readonly:
            entry.insert(0, placeholder)
            entry.configure(state="readonly")
        return entry

    def create_combobox(self, parent, values):
        box = ctk.CTkComboBox(
            parent,
            values=values,
            font=(FONT, 13),
            dropdown_font=(FONT, 13),
            height=40,
            corner_radius=8,
            border_width=1,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT_DARK,
            button_color=BORDER,
            button_hover_color=TEXT_GRAY,
            dropdown_fg_color=CARD,
            dropdown_text_color=TEXT_DARK,
            dropdown_hover_color=BACKGROUND,
            state="readonly"
        )
        box.set(values[0] if values else "")
        return box

    def create_textbox(self, parent):
        return ctk.CTkTextbox(
            parent,
            font=(FONT, 13),
            height=85,
            corner_radius=8,
            border_width=1,
            border_color=BORDER,
            fg_color=CARD,
            text_color=TEXT_DARK,
            wrap="word"
        )

    def create_buttons(self, parent_container):
        """Constructs primary form commit button groups along bottom section layout structure."""
        btn_frame = ctk.CTkFrame(parent_container, fg_color="transparent")
        btn_frame.grid(row=1, column=0, sticky="ew", padx=35, pady=(15, 25))

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # Clear Interface Button
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear",
            font=(FONT, 14, "bold"),
            height=44,
            corner_radius=8,
            fg_color="transparent",
            text_color=TEXT_DARK,
            border_width=1,
            border_color=BORDER,
            hover_color=BACKGROUND,
            command=self.clear_fields
        )
        clear_btn.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        # Save Student Action Commit Button
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Student",
            font=(FONT, 14, "bold"),
            height=44,
            corner_radius=8,
            fg_color=PRIMARY_BLUE,
            text_color="#FFFFFF",
            hover_color=HOVER_BLUE,
            command=self.save_student
        )
        self.save_btn.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def update_save_button_state(self):
        """Enables or disables the Save Student button based on course availability."""
        if self.save_btn is None:
            return

        if self.courses_available:
            self.save_btn.configure(state="normal")
        else:
            self.save_btn.configure(state="disabled")

    def validate_fields(self):
        """Checks required fields are filled and correctly formatted before saving. Returns True if valid."""
        name = self.fields["name"].get().strip()
        email = self.fields["email"].get().strip()
        phone = self.fields["phone"].get().strip()
        dob = self.fields["dob"].get().strip()
        address = self.fields["address"].get("1.0", "end").strip()

        required_fields = {
            "Full Name": name,
            "Email Address": email,
            "Phone Number": phone,
            "Date of Birth": dob,
            "Address": address,
        }

        missing = [label for label, value in required_fields.items() if not value]
        if missing:
            messagebox.showerror(
                "Missing Information",
                "Please fill in the following required field(s):\n- " + "\n- ".join(missing)
            )
            return False

        format_errors = []

        if not EMAIL_PATTERN.match(email):
            format_errors.append("Email Address must be a valid email (e.g. johndoe@example.com).")

        if not PHONE_PATTERN.match(phone):
            format_errors.append("Phone Number must contain 7-20 digits and may include +, -, (), or spaces.")

        try:
            parsed_dob = datetime.strptime(dob, DOB_FORMAT)
            if parsed_dob.date() > datetime.now().date():
                format_errors.append("Date of Birth cannot be in the future.")
        except ValueError:
            format_errors.append("Date of Birth must be in YYYY-MM-DD format.")

        if format_errors:
            messagebox.showerror(
                "Invalid Information",
                "Please correct the following field(s):\n- " + "\n- ".join(format_errors)
            )
            return False

        return True

    def set_student_id_field(self, student_id):
        """Updates the read-only Student ID field with the given value."""
        id_entry = self.fields["id"]
        id_entry.configure(state="normal")
        id_entry.delete(0, "end")
        id_entry.insert(0, student_id)
        id_entry.configure(state="readonly")

    def refresh_student_id(self):
        """Fetches a freshly generated Student ID from the backend and updates the form field."""
        new_id = generate_student_id()
        self.set_student_id_field(new_id)

    def save_student(self):
        # Guard against saving when no courses exist in the database
        if not self.courses_available:
            messagebox.showwarning(
                "No Courses Found",
                "Please add at least one course before registering a student."
            )
            return

        if not self.validate_fields():
            return

        student_data = {
            "student_id": self.fields["id"].get().strip(),
            "fullname": self.fields["name"].get().strip(),
            "email": self.fields["email"].get().strip(),
            "phone": self.fields["phone"].get().strip(),
            "dob": self.fields["dob"].get().strip(),
            "course": self.fields["course"].get(),
            "gender": self.gender_var.get(),
            "address": self.fields["address"].get("1.0", "end").strip(),
            "status": self.fields["status"].get(),
        }

        try:
            insert_student(student_data)
        except DuplicateStudentIDError:
            messagebox.showerror(
                "Duplicate Student ID",
                "This Student ID already exists. Please try saving again to generate a new ID."
            )
            self.refresh_student_id()
            return
        except DuplicateEmailError:
            messagebox.showerror(
                "Duplicate Email",
                "A student with this email address is already registered."
            )
            return

        messagebox.showinfo("Success", "Student added successfully.")

        self.clear_fields()
        self.refresh_student_id()
        self.refresh_recent_list()

    def clear_fields(self):
        for key, widget in self.fields.items():
            if key == "id":
                continue  # Maintain Read-Only Student ID template default string label

            if key == "course":
                continue  # Course field is refreshed separately (dynamic values, may be disabled)

            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            elif isinstance(widget, ctk.CTkComboBox):
                default_val = widget.cget("values")[0] if widget.cget("values") else ""
                widget.set(default_val)
            elif isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")

        # Reset the Course ComboBox back to its first available value (if any)
        course_box = self.fields.get("course")
        if course_box is not None and self.courses_available:
            values = course_box.cget("values")
            course_box.set(values[0] if values else "")

        self.gender_var.set("Male")


# --------------------------------------------------
# ISOLATED WINDOW INSTANTIATION (LOCAL RUN PREVIEW)
# --------------------------------------------------
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Student Management System - Full Add Student Page UI")
    root.geometry("1100x750")
    root.wm_geometry("1100x750")
    root.configure(fg_color=BACKGROUND)

    # Component easily integrates back within main application controller dashboard structures
    page = AddStudentPage(root, back_callback=lambda: print("Go Back Call Initiated"))
    page.pack(fill="both", expand=True)

    root.mainloop()