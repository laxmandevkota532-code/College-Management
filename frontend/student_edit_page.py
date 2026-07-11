import customtkinter as ctk
from tkinter import StringVar, messagebox

from backend.student_crud import update_student, DuplicateEmailError


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

        # Dummy student data fallback
        self.DUMMY_STUDENT = {
            "student_id": "STU001",
            "fullname": "Rajesh Kumar",
            "email": "rajesh.kumar@email.com",
            "phone": "9801234567",
            "dob": "2003-05-15",
            "course": "Computer Science",
            "gender": "Male",
            "address": "Kathmandu, Nepal",
            "status": "Active",
        }

        # Store original and current student data
        self.student_data = student_data or self.DUMMY_STUDENT.copy()
        self.original_student_data = self.student_data.copy()

        # Form fields storage
        self.form_fields = {}
        
        # Special widgets storage
        self.gender_var = StringVar(value=self.student_data.get("gender", "Male"))
        self.status_widget = None
        self.original_gender = self.student_data.get("gender", "Male")
        self.original_status = self.student_data.get("status", "Active")

        # Responsive Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_header()
        self.build_body()

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

        # Course
        self.create_entry(
            "Course",
            "course"
        )

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

        # Set initial value
        initial_value = str(self.student_data.get(field_key, ""))
        entry.insert(0, initial_value)

        # Disable if read-only
        if read_only:
            entry.configure(state="disabled", text_color=self.TEXT_GRAY)

        # Store reference
        self.form_fields[field_key] = entry

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

        # ComboBox
        self.status_widget = ctk.CTkComboBox(
            self.form_scroll,
            values=["Active", "Inactive", "Suspended"],
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

    def build_summary_card(self, parent):
        """Create right side student summary card."""
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

        id_value = ctk.CTkLabel(
            summary_card,
            text=self.student_data.get("student_id", "N/A"),
            text_color=self.PRIMARY_BLUE,
            font=ctk.CTkFont("Segoe UI", 12, "bold")
        )
        id_value.pack(anchor="w", padx=20, pady=(0, 16))

        # Student Name
        name_label = ctk.CTkLabel(
            summary_card,
            text="Student Name",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 11, "bold")
        )
        name_label.pack(anchor="w", padx=20, pady=(0, 4))

        name_value = ctk.CTkLabel(
            summary_card,
            text=self.student_data.get("fullname", "N/A"),
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            wraplength=240
        )
        name_value.pack(anchor="w", padx=20, pady=(0, 16))

        # Course
        course_label = ctk.CTkLabel(
            summary_card,
            text="Course",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 11, "bold")
        )
        course_label.pack(anchor="w", padx=20, pady=(0, 4))

        course_value = ctk.CTkLabel(
            summary_card,
            text=self.student_data.get("course", "N/A"),
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 12),
            wraplength=240
        )
        course_value.pack(anchor="w", padx=20, pady=(0, 16))

        # Status Badge
        status = self.student_data.get("status", "Active")
        status_color = "#D1FAE5" if status == "Active" else "#FEE2E2"
        status_text_color = "#065F46" if status == "Active" else "#991B1B"

        status_badge = ctk.CTkFrame(
            summary_card,
            fg_color=status_color,
            corner_radius=8
        )
        status_badge.pack(fill="x", padx=20, pady=(0, 16))

        status_label = ctk.CTkLabel(
            status_badge,
            text=f"Status: {status}",
            text_color=status_text_color,
            font=ctk.CTkFont("Segoe UI", 11, "bold")
        )
        status_label.pack(padx=12, pady=10)

        # Last Updated (Dummy)
        updated_label = ctk.CTkLabel(
            summary_card,
            text="Last Updated",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 10)
        )
        updated_label.pack(anchor="w", padx=20, pady=(16, 0))

        updated_value = ctk.CTkLabel(
            summary_card,
            text="Today at 3:45 PM",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 10)
        )
        updated_value.pack(anchor="w", padx=20, pady=(0, 20))

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
        save_btn = ctk.CTkButton(
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
        save_btn.pack(side="right")

    def reset_fields(self):
        """Restore all fields to original values."""
        for field_key, entry_widget in self.form_fields.items():
            if entry_widget.cget("state") != "disabled":
                entry_widget.delete(0, "end")
                entry_widget.insert(0, str(self.original_student_data.get(field_key, "")))
        
        # Reset Gender RadioButton
        self.gender_var.set(self.original_gender)
        
        # Reset Status ComboBox
        if self.status_widget:
            self.status_widget.set(self.original_status)

    def save_changes(self):
        """Validate, persist changes to the database, and navigate back on success."""
        # Collect current values
        updated_data = {
            "student_id": self.student_data.get("student_id", ""),
            "fullname": self.form_fields["fullname"].get().strip(),
            "email": self.form_fields["email"].get().strip(),
            "phone": self.form_fields["phone"].get().strip(),
            "dob": self.form_fields["dob"].get().strip(),
            "course": self.form_fields["course"].get().strip(),
            "address": self.form_fields["address"].get().strip(),
            "gender": self.gender_var.get(),
            "status": self.status_widget.get() if self.status_widget else "Active",
        }

        # Validate required fields
        required_fields = {
            "Full Name": updated_data["fullname"],
            "Email": updated_data["email"],
            "Phone": updated_data["phone"],
            "Course": updated_data["course"],
        }

        missing_fields = [name for name, value in required_fields.items() if not value]
        if missing_fields:
            messagebox.showwarning(
                "Missing Information",
                f"Please fill in the following required fields: {', '.join(missing_fields)}"
            )
            return

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

    # Test student data
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