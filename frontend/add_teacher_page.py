
import sqlite3
import re
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from backend.teacher_crud import (
    generate_teacher_id,
    insert_teacher,
    get_recent_teachers,
    DuplicateTeacherIDError
)

# ------------------------------------------------------------------
# DESIGN SYSTEM CONSTANTS (same as AddStudentPage)
# ------------------------------------------------------------------
COLOR_BG = "#F8F9FC"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY = "#4F5BD5"
COLOR_PRIMARY_HOVER = "#3F4ACB"
COLOR_PANEL = "#EEF2FF"
COLOR_TEXT_DARK = "#111827"
COLOR_TEXT_GRAY = "#6B7280"
COLOR_BORDER = "#E5E7EB"

FONT_FAMILY = "Segoe UI"

CORNER_RADIUS = 12
BUTTON_HEIGHT = 45
SPACING_LG = 30
SPACING_MD = 24

# ------------------------------------------------------------------
# DROPDOWN / OPTION VALUES
# ------------------------------------------------------------------
SUBJECT_VALUES = [
    "Computer Science",
    "Information Technology",
    "Business Administration",
    "Mathematics",
    "Physics",
    "Chemistry",
]

STATUS_VALUES = [
    "Active",
    "Inactive",
    "On Leave",
]


class AddTeacherPage(ctk.CTkFrame):
    """
    AddTeacherPage: A frame-based UI for registering new teachers.
    
    Integrates with teacher_crud backend for database operations.
    Provides form validation, error handling, and recent teacher display.
    """

    def __init__(self, parent, back_callback=None):
        """
        Initialize the AddTeacherPage frame.
        
        Args:
            parent: Parent widget.
            back_callback: Callback function to execute when Back button is clicked.
        """
        super().__init__(parent, fg_color=COLOR_BG)

        self.back_callback = back_callback
        self.current_teacher_id = None
        self.save_button = None

        self._build_layout()
        self._initialize_form()

    # ----------------------------------------------------------------
    # LAYOUT BUILDING
    # ----------------------------------------------------------------
    def _build_layout(self):
        """Build the complete page layout: header, body, bottom bar."""
        container = ctk.CTkFrame(self, fg_color=COLOR_BG)
        container.pack(fill="both", expand=True, padx=SPACING_LG, pady=SPACING_LG)

        self._build_header(container)

        # Body: two-column layout
        body = ctk.CTkFrame(container, fg_color=COLOR_BG)
        body.pack(fill="both", expand=True, pady=(SPACING_MD, 0))
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self._build_form_card(body)
        self._build_recent_card(body)

        self._build_bottom_bar(container)

    # ----------------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------------
    def _build_header(self, parent):
        """Build the page header with title, subtitle, and back button."""
        header = ctk.CTkFrame(parent, fg_color=COLOR_BG)
        header.pack(fill="x")

        back_btn = ctk.CTkButton(
            header,
            text="←  Back",
            width=90,
            height=36,
            corner_radius=CORNER_RADIUS,
            fg_color=COLOR_CARD,
            hover_color=COLOR_PANEL,
            text_color=COLOR_TEXT_DARK,
            border_width=1,
            border_color=COLOR_BORDER,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            command=self.go_back,
        )
        back_btn.pack(anchor="w")

        title = ctk.CTkLabel(
            header,
            text="Register New Teacher",
            font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        title.pack(anchor="w", pady=(12, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="Fill teacher information below.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            text_color=COLOR_TEXT_GRAY,
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    # ----------------------------------------------------------------
    # LEFT SIDE — FORM CARD
    # ----------------------------------------------------------------
    def _build_form_card(self, parent):
        """Build the form card with input fields."""
        card = ctk.CTkFrame(
            parent, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_MD))
        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(
            card, text="Teacher Information",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        heading.grid(row=0, column=0, sticky="w", padx=24, pady=(24, 12))

        scroll = ctk.CTkScrollableFrame(
            card, fg_color="transparent",
            scrollbar_button_color=COLOR_BORDER,
            scrollbar_button_hover_color=COLOR_TEXT_GRAY,
        )
        scroll.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)

        self.entries = {}

        # Teacher ID (read only)
        self.entries["teacher_id"] = self._add_entry(
            scroll, "Teacher ID", 0, 0, placeholder="T001", read_only=True
        )

        # Full Name (maps to fullname in database)
        self.entries["fullname"] = self._add_entry(
            scroll, "Full Name", 0, 1, placeholder="Enter full name"
        )

        # Email Address
        self.entries["email"] = self._add_entry(
            scroll, "Email Address", 1, 0, placeholder="Enter email address"
        )

        # Phone Number
        self.entries["phone"] = self._add_entry(
            scroll, "Phone Number", 1, 1, placeholder="Enter phone number"
        )

        # Subject (maps to subject in database)
        self.subject_combo = self._add_combobox(
            scroll, "Subject", 2, 0, SUBJECT_VALUES
        )

        # Experience (Years)
        self.entries["experience"] = self._add_entry(
            scroll, "Experience (Years)", 2, 1, placeholder="Enter years of experience"
        )

        # Status (ComboBox)
        self.status_combo = self._add_combobox(
            scroll, "Status", 3, 0, STATUS_VALUES
        )

    # ----------------------------------------------------------------
    # FORM FIELD HELPERS
    # ----------------------------------------------------------------
    def _add_entry(self, parent, label, row, col, placeholder="", read_only=False):
        """
        Create a labeled entry field.
        
        Args:
            parent: Parent widget.
            label: Label text.
            row: Grid row.
            col: Grid column.
            placeholder: Placeholder text.
            read_only: If True, entry is disabled.
            
        Returns:
            CTkEntry widget.
        """
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=row, column=col, sticky="ew", padx=8, pady=10)

        label_widget = ctk.CTkLabel(
            wrapper, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        label_widget.pack(anchor="w", pady=(0, 6))

        entry = ctk.CTkEntry(
            wrapper,
            placeholder_text=placeholder,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=COLOR_PANEL if read_only else COLOR_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT_DARK,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
        )
        entry.pack(fill="x")

        if read_only:
            entry.configure(state="disabled")

        return entry

    def _add_combobox(self, parent, label, row, col, values):
        """
        Create a labeled combobox field.
        
        Args:
            parent: Parent widget.
            label: Label text.
            row: Grid row.
            col: Grid column.
            values: List of combobox options.
            
        Returns:
            CTkComboBox widget.
        """
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=row, column=col, sticky="ew", padx=8, pady=10)

        label_widget = ctk.CTkLabel(
            wrapper, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        label_widget.pack(anchor="w", pady=(0, 6))

        combo = ctk.CTkComboBox(
            wrapper,
            values=values,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=COLOR_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            dropdown_fg_color=COLOR_CARD,
            text_color=COLOR_TEXT_DARK,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
        )
        combo.set(values[0])
        combo.pack(fill="x")

        return combo

    # ----------------------------------------------------------------
    # RIGHT SIDE — RECENTLY ADDED TEACHERS
    # ----------------------------------------------------------------
    def _build_recent_card(self, parent):
        """Build the recent teachers card on the right side."""
        self.recent_card = ctk.CTkFrame(
            parent, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        self.recent_card.grid(row=0, column=1, sticky="nsew")

        heading = ctk.CTkLabel(
            self.recent_card, text="Recent Added Teachers",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        heading.pack(anchor="w", padx=24, pady=(24, 16))

        self.recent_teachers_container = ctk.CTkFrame(
            self.recent_card, fg_color=COLOR_CARD
        )
        self.recent_teachers_container.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self.refresh_recent_teachers()

    def refresh_recent_teachers(self):
        """Load and display recent teachers from the database."""
        self.load_recent_teachers()

    def load_recent_teachers(self):
        """Fetch recent teachers from database and display them."""
        # Clear existing widgets
        for widget in self.recent_teachers_container.winfo_children():
            widget.destroy()

        # Fetch recent teachers from database
        recent_teachers = get_recent_teachers(limit=5)

        if not recent_teachers:
            no_data = ctk.CTkLabel(
                self.recent_teachers_container,
                text="No teachers available.",
                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                text_color=COLOR_TEXT_GRAY,
            )
            no_data.pack(pady=20)
            return

        for teacher in recent_teachers:
            self._add_recent_teacher_card(self.recent_teachers_container, teacher)

    def _add_recent_teacher_card(self, parent, teacher):
        """
        Add a single recent teacher card to the container.
        
        Args:
            parent: Parent widget.
            teacher: Dictionary containing teacher data.
        """
        item = ctk.CTkFrame(parent, fg_color=COLOR_PANEL, corner_radius=CORNER_RADIUS)
        item.pack(fill="x", padx=0, pady=8)

        id_label = ctk.CTkLabel(
            item, text=teacher.get("teacher_id", "N/A"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_PRIMARY, anchor="w",
        )
        id_label.pack(anchor="w", padx=16, pady=(12, 0))

        name_label = ctk.CTkLabel(
            item, text=teacher.get("teacher_name", "N/A"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        name_label.pack(anchor="w", padx=16, pady=(2, 0))

        dept_label = ctk.CTkLabel(
            item, text=teacher.get("department", "N/A"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_GRAY, anchor="w",
        )
        dept_label.pack(anchor="w", padx=16, pady=(0, 12))

    # ----------------------------------------------------------------
    # BOTTOM BAR — CLEAR / SAVE BUTTONS
    # ----------------------------------------------------------------
    def _build_bottom_bar(self, parent):
        """Build the bottom button bar."""
        bottom_bar = ctk.CTkFrame(parent, fg_color=COLOR_BG)
        bottom_bar.pack(fill="x", pady=(SPACING_MD, 0))

        clear_btn = ctk.CTkButton(
            bottom_bar,
            text="Clear",
            width=140,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=COLOR_CARD,
            hover_color=COLOR_PANEL,
            text_color=COLOR_TEXT_DARK,
            border_width=1,
            border_color=COLOR_BORDER,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            command=self.clear_fields,
        )
        clear_btn.pack(side="left")

        self.save_button = ctk.CTkButton(
            bottom_bar,
            text="Save Teacher",
            width=160,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            command=self.save_teacher,
        )
        self.save_button.pack(side="right")

    # ----------------------------------------------------------------
    # INITIALIZATION
    # ----------------------------------------------------------------
    def _initialize_form(self):
        """Generate and display the first Teacher ID on page load."""
        self.current_teacher_id = generate_teacher_id()
        self.entries["teacher_id"].configure(state="normal")
        self.entries["teacher_id"].delete(0, "end")
        self.entries["teacher_id"].insert(0, self.current_teacher_id)
        self.entries["teacher_id"].configure(state="disabled")

    # ----------------------------------------------------------------
    # VALIDATION HELPERS
    # ----------------------------------------------------------------
    def _validate_required_field(self, value, field_name):
        """
        Validate that a required field is not empty.
        
        Args:
            value: Field value to validate.
            field_name: Name of the field for error messages.
            
        Returns:
            True if valid, False otherwise.
        """
        if not value or not value.strip():
            CTkMessagebox(
                title="Validation Error",
                message=f"{field_name} is required.",
                icon="warning"
            )
            return False
        return True

    def _validate_email(self, email):
        """
        Validate email format.
        
        Args:
            email: Email address to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            CTkMessagebox(
                title="Validation Error",
                message="Please enter a valid email address.",
                icon="warning"
            )
            return False
        return True

    def _validate_phone(self, phone):
        """
        Validate phone number (digits only, minimum 10 digits).
        
        Args:
            phone: Phone number to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        if not phone.isdigit():
            CTkMessagebox(
                title="Validation Error",
                message="Phone Number must contain only digits.",
                icon="warning"
            )
            return False
        if len(phone) < 10:
            CTkMessagebox(
                title="Validation Error",
                message="Phone Number must be at least 10 digits.",
                icon="warning"
            )
            return False
        return True

    def _validate_experience(self, experience):
        """
        Validate experience (must be numeric and non-negative).
        
        Args:
            experience: Experience value to validate.
            
        Returns:
            True if valid, False otherwise.
        """
        try:
            exp_value = float(experience)
            if exp_value < 0:
                CTkMessagebox(
                    title="Validation Error",
                    message="Experience cannot be negative.",
                    icon="warning"
                )
                return False
            return True
        except ValueError:
            CTkMessagebox(
                title="Validation Error",
                message="Experience must be a valid number.",
                icon="warning"
            )
            return False

    # ----------------------------------------------------------------
    # FORM FUNCTIONS
    # ----------------------------------------------------------------
    def save_teacher(self):
        """
        Validate form data, insert teacher record into database,
        and refresh the UI on success.
        """
        # Disable save button during insertion
        self.save_button.configure(state="disabled")

        try:
            # Retrieve and trim all field values
            fullname = self.entries["fullname"].get().strip()
            email = self.entries["email"].get().strip()
            phone = self.entries["phone"].get().strip()
            subject = self.subject_combo.get().strip()
            experience = self.entries["experience"].get().strip()
            status = self.status_combo.get().strip()

            # Validate required fields
            if not self._validate_required_field(fullname, "Full Name"):
                return
            if not self._validate_required_field(email, "Email Address"):
                return
            if not self._validate_required_field(phone, "Phone Number"):
                return
            if not self._validate_required_field(subject, "Subject"):
                return
            if not self._validate_required_field(experience, "Experience"):
                return
            if not self._validate_required_field(status, "Status"):
                return

            # Validate email format
            if not self._validate_email(email):
                return

            # Validate phone number
            if not self._validate_phone(phone):
                return

            # Validate experience
            if not self._validate_experience(experience):
                return

            # Build teacher data dictionary
            # Maps form fields to backend dictionary keys for insert_teacher()
            teacher_data = {
                "teacher_id": self.current_teacher_id,
                "teacher_name": fullname,  # Maps to fullname in database
                "department": subject,      # Maps to subject in database
                "email": email,
                "phone": phone,
                "qualification": "",        # Not used in actual database
                "experience": experience,
                "status": status,
                "description": ""           # Not used in actual database
            }

            # Attempt to insert teacher
            try:
                success = insert_teacher(teacher_data)
                if success:
                    CTkMessagebox(
                        title="Success",
                        message="Teacher record saved successfully.",
                        icon="check"
                    )
                    self.clear_fields()
                    self.refresh_recent_teachers()
                    self._initialize_form()
                    self.entries["fullname"].focus()
                else:
                    CTkMessagebox(
                        title="Error",
                        message="Failed to save teacher record. Please try again.",
                        icon="cancel"
                    )
            except DuplicateTeacherIDError as e:
                CTkMessagebox(
                    title="Duplicate Error",
                    message=str(e),
                    icon="cancel"
                )
            except sqlite3.Error as e:
                CTkMessagebox(
                    title="Database Error",
                    message=f"A database error occurred: {str(e)}",
                    icon="cancel"
                )
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"An unexpected error occurred: {str(e)}",
                    icon="cancel"
                )
        finally:
            # Re-enable save button
            self.save_button.configure(state="normal")

    def clear_fields(self):
        """
        Clear all form fields except Teacher ID.
        
        Teacher ID is always preserved and managed by _initialize_form().
        """
        self.entries["fullname"].delete(0, "end")
        self.entries["email"].delete(0, "end")
        self.entries["phone"].delete(0, "end")
        self.entries["experience"].delete(0, "end")
        self.subject_combo.set(SUBJECT_VALUES[0])
        self.status_combo.set(STATUS_VALUES[0])

    def go_back(self):
        """Navigate back to the previous page."""
        if self.back_callback:
            self.back_callback()