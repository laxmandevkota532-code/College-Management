import re
from datetime import datetime

import customtkinter as ctk
from tkinter import StringVar, messagebox

from backend.student_crud import update_student, DuplicateEmailError
from backend.course_crud import get_all_courses

# --------------------------------------------------
# BACKEND INTEGRATION NOTES
# --------------------------------------------------
# backend/student_crud.py exposes:
#   update_student(student_data: dict) -> None
#       expects keys: student_id, fullname, email, phone, dob, course,
#                     gender, address, status
#   DuplicateEmailError
#
# backend/course_crud.py exposes:
#   get_all_courses() -> list[dict]
#       each dict has key: course_name (among possibly others)

# --------------------------------------------------
# VALIDATION PATTERNS (mirrors AddStudentPage)
# --------------------------------------------------
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\+?[0-9()\-\s]{7,20}$")
DOB_FORMAT = "%Y-%m-%d"

# --------------------------------------------------
# PLACEHOLDER TEXT WHEN NO COURSES EXIST IN DATABASE
# --------------------------------------------------
NO_COURSES_PLACEHOLDER = "No Courses Available"


class EditStudentPage(ctk.CTkFrame):
    def __init__(self, master, student_data=None, back_callback=None):
        super().__init__(master, fg_color="#F8F9FC")

        # Navigation Callback Injection
        self.back_callback = back_callback

        # --- Color Palette ---
        self.PRIMARY_BLUE = "#4F5BD5"
        self.HOVER_BLUE = "#3F4ACB"
        self.BACKGROUND = "#F8F9FC"
        self.CARD = "#FFFFFF"
        self.TEXT_DARK = "#111827"
        self.TEXT_GRAY = "#6B7280"
        self.BORDER = "#E5E7EB"
        self.PANEL_BG = "#EEF2FF"

        # --------------------------------------------------
        # STUDENT DATA (no dummy fallback)
        # --------------------------------------------------
        # This page must always be opened with real student_data coming from
        # Student Management. If it isn't provided, we do NOT fabricate a
        # fake record -- instead we render the page in a disabled,
        # error state so the user can't silently edit/save garbage data.
        self.data_missing = student_data is None
        self.student_data = student_data.copy() if student_data else {}
        self.original_student_data = self.student_data.copy()

        # Form fields storage
        self.form_fields = {}

        # Special widgets storage
        self.gender_var = StringVar(value=self.student_data.get("gender", ""))
        self.gender_radios = []  # Track radio buttons so we can disable them if needed
        self.status_widget = None
        self.course_widget = None
        self.save_btn = None
        self.original_gender = self.student_data.get("gender", "")
        self.original_status = self.student_data.get("status", "")

        # Tracks whether the database currently has at least one course available.
        # Set inside create_course_selector().
        self.courses_available = True

        # Summary card value labels (updated live, kept as references for clarity)
        self.summary_id_value = None
        self.summary_name_value = None
        self.summary_course_value = None
        self.status_badge_label = None
        self.status_badge_frame = None

        # Responsive Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_header()
        self.build_body()

        # If no student data was supplied, alert the user and lock the form
        # down after all widgets have been created.
        if self.data_missing:
            messagebox.showerror(
                "No Student Selected",
                "No student data was provided. Please select a student from "
                "Student Management before editing."
            )
            self.disable_all_editing()

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    def build_header(self):
        """Create header with back button and title."""
        header_frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)

        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            text_color=self.PRIMARY_BLUE,
            fg_color="transparent",
            hover_color=self.BACKGROUND,
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            cursor="hand2",
            command=self.go_back
        )
        back_btn.grid(row=0, column=0, padx=40, pady=20, sticky="w")

        # Title container
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.grid(row=0, column=1, sticky="w", padx=40, pady=20)

        title_label = ctk.CTkLabel(
            title_container,
            text="Edit Student",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 28, "bold")
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Update student information.",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 13)
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))

        # Bottom border
        border = ctk.CTkFrame(self, fg_color=self.BORDER, height=1)
        border.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

    # --------------------------------------------------
    # BODY
    # --------------------------------------------------
    def build_body(self):
        """Create main content area with form and right panel."""
        body_frame = ctk.CTkFrame(self, fg_color=self.BACKGROUND)
        body_frame.grid(row=2, column=0, sticky="nsew", padx=40, pady=40)
        body_frame.grid_columnconfigure(0, weight=1)
        body_frame.grid_columnconfigure(1, weight=0)
        body_frame.grid_rowconfigure(0, weight=1)

        # Left side - Form Card
        form_card = ctk.CTkFrame(
            body_frame,
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 24))
        form_card.grid_columnconfigure(0, weight=1)

        # Form title
        form_title = ctk.CTkLabel(
            form_card,
            text="Student Information",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 16, "bold")
        )
        form_title.pack(anchor="w", padx=30, pady=(30, 20))

        # Scrollable form
        self.form_scroll = ctk.CTkScrollableFrame(
            form_card,
            fg_color=self.CARD,
            corner_radius=12
        )
        self.form_scroll.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        self.form_scroll.grid_columnconfigure(0, weight=1)

        # Build form fields
        self.populate_form()

        # Right side - Student Summary Card
        self.build_summary_card(body_frame)

        # Bottom buttons
        self.build_buttons()

        # Now that the Course ComboBox and Save button both exist, apply the
        # correct enabled/disabled state based on course availability.
        self.update_save_button_state()

    def populate_form(self):
        """Create form input fields."""
        # Student ID (Read-Only)
        self.create_entry(
            "Student ID",
            "student_id",
            read_only=True
        )

        # Full Name
        self.create_entry(
            "Full Name",
            "fullname"
        )

        # Email Address
        self.create_entry(
            "Email Address",
            "email"
        )

        # Phone Number
        self.create_entry(
            "Phone Number",
            "phone"
        )

        # Date of Birth
        self.create_entry(
            "Date of Birth",
            "dob"
        )

        # Course (dynamically loaded ComboBox)
        self.create_course_selector()

        # Gender (RadioButtons)
        self.create_gender_selector()

        # Address
        self.create_entry(
            "Address",
            "address"
        )

        # Status (ComboBox)
        self.create_status_selector()

    def create_entry(self, label_text, field_key, read_only=False):
        """Create a labeled entry field."""
        # Label
        label = ctk.CTkLabel(
            self.form_scroll,
            text=label_text,
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 12, "bold")
        )
        label.pack(anchor="w", pady=(16, 8))

        # Entry field
        entry = ctk.CTkEntry(
            self.form_scroll,
            fg_color=self.BACKGROUND,
            border_color=self.BORDER,
            border_width=1,
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 13),
            height=45,
            corner_radius=8
        )
        entry.pack(fill="x", pady=(0, 16))

        # Set initial value directly from real student_data (never a dummy fallback)
        initial_value = str(self.student_data.get(field_key, ""))
        entry.insert(0, initial_value)

        # Disable if read-only
        if read_only:
            entry.configure(state="disabled", text_color=self.TEXT_GRAY)

        # Store reference
        self.form_fields[field_key] = entry

    def load_course_names(self):
        """
        Fetches all courses from the database and extracts their course_name values.

        Returns:
            list[str]: A list of course names. Empty if no courses exist in the database.
        """
        courses = get_all_courses() or []
        return [course.get("course_name") for course in courses if course.get("course_name")]

    def create_course_selector(self):
        """Create the Course ComboBox, populated dynamically from the database."""
        # Label
        label = ctk.CTkLabel(
            self.form_scroll,
            text="Course",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 12, "bold")
        )
        label.pack(anchor="w", pady=(16, 8))

        course_names = self.load_course_names()
        current_course = self.student_data.get("course", "")

        # Preserve the student's current course selection even if, for some
        # reason, it isn't present in the active course list anymore.
        if course_names and current_course and current_course not in course_names:
            course_names = [current_course] + course_names

        if course_names:
            self.courses_available = True
            self.course_widget = ctk.CTkComboBox(
                self.form_scroll,
                values=course_names,
                state="readonly",
                fg_color=self.BACKGROUND,
                border_color=self.BORDER,
                border_width=1,
                text_color=self.TEXT_DARK,
                button_color=self.PRIMARY_BLUE,
                button_hover_color=self.HOVER_BLUE,
                font=ctk.CTkFont("Segoe UI", 13),
                height=45,
                corner_radius=8
            )
            self.course_widget.set(current_course if current_course else course_names[0])
        else:
            # No courses exist: show placeholder, disable, and warn the user
            self.courses_available = False
            self.course_widget = ctk.CTkComboBox(
                self.form_scroll,
                values=[NO_COURSES_PLACEHOLDER],
                state="disabled",
                fg_color=self.BACKGROUND,
                border_color=self.BORDER,
                border_width=1,
                text_color=self.TEXT_DARK,
                button_color=self.PRIMARY_BLUE,
                button_hover_color=self.HOVER_BLUE,
                font=ctk.CTkFont("Segoe UI", 13),
                height=45,
                corner_radius=8
            )
            self.course_widget.set(NO_COURSES_PLACEHOLDER)
            messagebox.showwarning(
                "No Courses Found",
                "Please add at least one course before editing students."
            )

        self.course_widget.pack(fill="x", pady=(0, 16))

    def create_gender_selector(self):
        """Create gender selector with radio buttons."""
        # Label
        label = ctk.CTkLabel(
            self.form_scroll,
            text="Gender",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 12, "bold")
        )
        label.pack(anchor="w", pady=(16, 12))

        # Radio buttons frame
        radio_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
        radio_frame.pack(fill="x", pady=(0, 16))

        # Male radio button
        male_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Male",
            variable=self.gender_var,
            value="Male",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 13)
        )
        male_radio.pack(side="left", padx=(0, 24))

        # Female radio button
        female_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Female",
            variable=self.gender_var,
            value="Female",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 13)
        )
        female_radio.pack(side="left", padx=(0, 24))

        # Other radio button
        other_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Other",
            variable=self.gender_var,
            value="Other",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 13)
        )
        other_radio.pack(side="left")

        # Keep references so we can disable them together if there's no student data
        self.gender_radios = [male_radio, female_radio, other_radio]

    def create_status_selector(self):
        """Create status selector with combobox."""
        # Label
        label = ctk.CTkLabel(
            self.form_scroll,
            text="Status",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 12, "bold")
        )
        label.pack(anchor="w", pady=(16, 8))

        # ComboBox ("Suspended" removed -- only Active / Inactive remain)
        self.status_widget = ctk.CTkComboBox(
            self.form_scroll,
            values=["Active", "Inactive"],
            state="readonly",
            fg_color=self.BACKGROUND,
            border_color=self.BORDER,
            border_width=1,
            text_color=self.TEXT_DARK,
            button_color=self.PRIMARY_BLUE,
            button_hover_color=self.HOVER_BLUE,
            font=ctk.CTkFont("Segoe UI", 13),
            height=45,
            corner_radius=8
        )
        self.status_widget.pack(fill="x", pady=(0, 16))
        self.status_widget.set(self.student_data.get("status", "Active"))

    # --------------------------------------------------
    # SUMMARY CARD
    # --------------------------------------------------
    def build_summary_card(self, parent):
        """Create right side student summary card, populated with live student_data."""
        summary_card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER,
            width=280
        )
        summary_card.grid(row=0, column=1, sticky="n")
        summary_card.grid_propagate(False)

        # Title
        title = ctk.CTkLabel(
            summary_card,
            text="Student Summary",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 14, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(20, 16))

        # Divider
        divider = ctk.CTkFrame(summary_card, fg_color=self.BORDER, height=1)
        divider.pack(fill="x", padx=20, pady=(0, 16))

        # Student ID
        id_label = ctk.CTkLabel(
            summary_card,
            text="Student ID",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 11, "bold")
        )
        id_label.pack(anchor="w", padx=20, pady=(0, 4))

        self.summary_id_value = ctk.CTkLabel(
            summary_card,
            text=self.student_data.get("student_id", "N/A"),
            text_color=self.PRIMARY_BLUE,
            font=ctk.CTkFont("Segoe UI", 12, "bold")
        )
        self.summary_id_value.pack(anchor="w", padx=20, pady=(0, 16))

        # Student Name
        name_label = ctk.CTkLabel(
            summary_card,
            text="Student Name",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 11, "bold")
        )
        name_label.pack(anchor="w", padx=20, pady=(0, 4))

        self.summary_name_value = ctk.CTkLabel(
            summary_card,
            text=self.student_data.get("fullname", "N/A"),
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            wraplength=240
        )
        self.summary_name_value.pack(anchor="w", padx=20, pady=(0, 16))

        # Course
        course_label = ctk.CTkLabel(
            summary_card,
            text="Course",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 11, "bold")
        )
        course_label.pack(anchor="w", padx=20, pady=(0, 4))

        self.summary_course_value = ctk.CTkLabel(
            summary_card,
            text=self.student_data.get("course", "N/A"),
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 12),
            wraplength=240
        )
        self.summary_course_value.pack(anchor="w", padx=20, pady=(0, 16))

        # Status Badge (Green = Active, Gray = Inactive)
        self.status_badge_frame = ctk.CTkFrame(
            summary_card,
            corner_radius=8
        )
        self.status_badge_frame.pack(fill="x", padx=20, pady=(0, 16))

        self.status_badge_label = ctk.CTkLabel(
            self.status_badge_frame,
            font=ctk.CTkFont("Segoe UI", 11, "bold")
        )
        self.status_badge_label.pack(padx=12, pady=10)

        self.refresh_status_badge(self.student_data.get("status", "Active"))

        # Footer caption (replaces the old dummy "Last Updated / Today at 3:45 PM")
        info_label = ctk.CTkLabel(
            summary_card,
            text="Current Student Information",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 10, "italic")
        )
        info_label.pack(anchor="w", padx=20, pady=(16, 20))

    def refresh_status_badge(self, status):
        """Updates the status badge's color and text based on the given status."""
        if status == "Active":
            badge_color = "#D1FAE5"   # green
            text_color = "#065F46"
        else:
            badge_color = "#E5E7EB"   # gray (Inactive, or unknown)
            text_color = "#374151"

        self.status_badge_frame.configure(fg_color=badge_color)
        self.status_badge_label.configure(text=f"Status: {status}", text_color=text_color)

    # --------------------------------------------------
    # BUTTONS
    # --------------------------------------------------
    def build_buttons(self):
        """Create bottom action buttons."""
        button_frame = ctk.CTkFrame(self, fg_color=self.BACKGROUND)
        button_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=(0, 40))
        button_frame.grid_columnconfigure(1, weight=1)

        # Reset Changes button
        reset_btn = ctk.CTkButton(
            button_frame,
            text="Reset Changes",
            text_color=self.PRIMARY_BLUE,
            fg_color="transparent",
            hover_color=self.PANEL_BG,
            border_width=1,
            border_color=self.PRIMARY_BLUE,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            height=45,
            corner_radius=8,
            cursor="hand2",
            command=self.reset_fields
        )
        reset_btn.pack(side="left", padx=(0, 12))

        # Spacer
        spacer = ctk.CTkFrame(button_frame, fg_color="transparent")
        spacer.pack(side="left", fill="x", expand=True)

        # Save Changes button
        self.save_btn = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            text_color=self.CARD,
            fg_color=self.PRIMARY_BLUE,
            hover_color=self.HOVER_BLUE,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            height=45,
            corner_radius=8,
            cursor="hand2",
            command=self.save_changes
        )
        self.save_btn.pack(side="right")

    def update_save_button_state(self):
        """Enables or disables the Save Changes button based on course availability."""
        if self.save_btn is None:
            return

        if self.courses_available and not self.data_missing:
            self.save_btn.configure(state="normal")
        else:
            self.save_btn.configure(state="disabled")

    # --------------------------------------------------
    # DISABLE-ALL (used when student_data is missing)
    # --------------------------------------------------
    def disable_all_editing(self):
        """Disables every editable widget on the page when no student_data was supplied."""
        for field_key, entry_widget in self.form_fields.items():
            entry_widget.configure(state="disabled")

        if self.course_widget is not None:
            self.course_widget.configure(state="disabled")

        if self.status_widget is not None:
            self.status_widget.configure(state="disabled")

        for radio in self.gender_radios:
            radio.configure(state="disabled")

        self.update_save_button_state()

    # --------------------------------------------------
    # VALIDATION (mirrors AddStudentPage)
    # --------------------------------------------------
    def validate_fields(self):
        """Checks required fields are filled and correctly formatted before saving. Returns True if valid."""
        name = self.form_fields["fullname"].get().strip()
        email = self.form_fields["email"].get().strip()
        phone = self.form_fields["phone"].get().strip()
        dob = self.form_fields["dob"].get().strip()
        address = self.form_fields["address"].get().strip()

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

    # --------------------------------------------------
    # RESET / SAVE / NAVIGATION
    # --------------------------------------------------
    def reset_fields(self):
        """Restore all fields to their original database values."""
        if self.data_missing:
            return  # Nothing to reset -- editing is locked

        for field_key, entry_widget in self.form_fields.items():
            if entry_widget.cget("state") != "disabled":
                entry_widget.delete(0, "end")
                entry_widget.insert(0, str(self.original_student_data.get(field_key, "")))

        # Reset Course ComboBox
        if self.course_widget is not None and self.courses_available:
            self.course_widget.set(self.original_student_data.get("course", ""))

        # Reset Gender RadioButton
        self.gender_var.set(self.original_gender)

        # Reset Status ComboBox
        if self.status_widget:
            self.status_widget.set(self.original_status)

    def save_changes(self):
        """Validate, persist changes to the database, and navigate back on success."""
        # Guard against saving when no student data was ever loaded
        if self.data_missing:
            messagebox.showerror(
                "No Student Selected",
                "No student data was provided. Please select a student from "
                "Student Management before editing."
            )
            return

        # Guard against saving when no courses exist in the database
        if not self.courses_available:
            messagebox.showwarning(
                "No Courses Found",
                "Please add at least one course before editing students."
            )
            return

        # Validate all required fields and formats
        if not self.validate_fields():
            return

        # Collect current values
        updated_data = {
            "student_id": self.student_data.get("student_id", ""),
            "fullname": self.form_fields["fullname"].get().strip(),
            "email": self.form_fields["email"].get().strip(),
            "phone": self.form_fields["phone"].get().strip(),
            "dob": self.form_fields["dob"].get().strip(),
            "course": self.course_widget.get() if self.course_widget else "",
            "address": self.form_fields["address"].get().strip(),
            "gender": self.gender_var.get(),
            "status": self.status_widget.get() if self.status_widget else "Active",
        }

        # Persist to database
        try:
            update_student(updated_data)
        except DuplicateEmailError:
            messagebox.showerror(
                "Duplicate Email",
                f"Email '{updated_data['email']}' is already registered to another student."
            )
            return
        except Exception as e:
            messagebox.showerror(
                "Update Failed",
                f"An error occurred while updating the student: {e}"
            )
            return

        messagebox.showinfo(
            "Success",
            "Student updated successfully."
        )

        if self.back_callback:
            self.back_callback()

    def go_back(self):
        """Navigate back using callback."""
        if self.back_callback:
            self.back_callback()


if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("1200x800")
    root.title("Edit Student Page")

    # Test student data (for local preview only -- real usage must always
    # pass an actual student record loaded from Student Management)
    test_student = {
        "student_id": "STU001",
        "fullname": "Aarav Sharma",
        "email": "aarav.sharma@email.com",
        "phone": "9801234567",
        "dob": "2003-05-15",
        "course": "CSIT",
        "gender": "Male",
        "address": "Kathmandu, Nepal",
        "status": "Active",
    }

    # Back callback
    def go_back():
        print("Back to Student Management")
        root.quit()

    # Create and display page
    page = EditStudentPage(root, student_data=test_student, back_callback=go_back)
    page.pack(fill="both", expand=True)

    root.mainloop()