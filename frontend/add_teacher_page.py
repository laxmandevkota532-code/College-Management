"""
College Management System
Page: Add Teacher

Mirrors the exact design system, spacing, colors, typography, and layout
used in the existing AddStudentPage — same header, same back button,
same two-column layout, same white cards, same bottom buttons.

No database. No TreeView. No ttk/tkinter widgets — CustomTkinter only.
"""

import customtkinter as ctk

# ------------------------------------------------------------------
# GLOBAL APPEARANCE
# ------------------------------------------------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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
DEPARTMENT_VALUES = [
    "Computer Science",
    "Information Technology",
    "Business Administration",
    "Mathematics",
    "Physics",
    "Chemistry",
]

DESIGNATION_VALUES = [
    "Professor",
    "Associate Professor",
    "Assistant Professor",
    "Lecturer",
    "Instructor",
]

STATUS_VALUES = [
    "Active",
    "Inactive",
    "On Leave",
]

# ------------------------------------------------------------------
# DUMMY DATA — RECENTLY ADDED TEACHERS
# ------------------------------------------------------------------
RECENT_TEACHERS = [
    {"id": "TEC001", "name": "Dr. Robert Wilson", "department": "Computer Science"},
    {"id": "TEC002", "name": "Sarah Johnson", "department": "Mathematics"},
    {"id": "TEC003", "name": "David Brown", "department": "Physics"},
    {"id": "TEC004", "name": "Emily Davis", "department": "Information Technology"},
]


class AddTeacherPage(ctk.CTk):
    def __init__(self, back_callback=None):
        super().__init__()

        self.back_callback = back_callback

        self.title("College Management System - Add Teacher")
        self.geometry("1300x820")
        self.configure(fg_color=COLOR_BG)

        self._build_layout()

    # ----------------------------------------------------------------
    # LAYOUT
    # ----------------------------------------------------------------
    def _build_layout(self):
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
            scroll, "Teacher ID", 0, 0, placeholder="TEC005", read_only=True
        )

        # Full Name
        self.entries["full_name"] = self._add_entry(
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

        # Date of Birth
        self.entries["dob"] = self._add_entry(
            scroll, "Date of Birth", 2, 0, placeholder="DD/MM/YYYY"
        )

        # Department (ComboBox)
        self.department_combo = self._add_combobox(
            scroll, "Department", 2, 1, DEPARTMENT_VALUES
        )

        # Designation (ComboBox)
        self.designation_combo = self._add_combobox(
            scroll, "Designation", 3, 0, DESIGNATION_VALUES
        )

        # Gender (Radio Buttons)
        self.gender_var = ctk.StringVar(value="Male")
        self._add_radio_group(scroll, "Gender", 3, 1, ["Male", "Female", "Other"], self.gender_var)

        # Qualification
        self.entries["qualification"] = self._add_entry(
            scroll, "Qualification", 4, 0, placeholder="e.g. Ph.D. in Computer Science"
        )

        # Experience (Years)
        self.entries["experience"] = self._add_entry(
            scroll, "Experience (Years)", 4, 1, placeholder="Enter years of experience"
        )

        # Salary
        self.entries["salary"] = self._add_entry(
            scroll, "Salary", 5, 0, placeholder="Enter salary"
        )

        # Status (ComboBox)
        self.status_combo = self._add_combobox(
            scroll, "Status", 5, 1, STATUS_VALUES
        )

        # Address (Textbox) — spans both columns
        self._add_textbox(scroll, "Address", 6)

    # ----------------------------------------------------------------
    # FORM FIELD HELPERS
    # ----------------------------------------------------------------
    def _add_entry(self, parent, label, row, col, placeholder="", read_only=False):
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
            entry.insert(0, placeholder)
            entry.configure(state="disabled")

        return entry

    def _add_combobox(self, parent, label, row, col, values):
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

    def _add_radio_group(self, parent, label, row, col, options, variable):
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=row, column=col, sticky="ew", padx=8, pady=10)

        label_widget = ctk.CTkLabel(
            wrapper, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        label_widget.pack(anchor="w", pady=(0, 6))

        radio_row = ctk.CTkFrame(wrapper, fg_color="transparent")
        radio_row.pack(fill="x")

        for option in options:
            radio_btn = ctk.CTkRadioButton(
                radio_row,
                text=option,
                value=option,
                variable=variable,
                fg_color=COLOR_PRIMARY,
                hover_color=COLOR_PRIMARY_HOVER,
                text_color=COLOR_TEXT_DARK,
                font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            )
            radio_btn.pack(side="left", padx=(0, 18))

    def _add_textbox(self, parent, label, row):
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=row, column=0, columnspan=2, sticky="ew", padx=8, pady=10)

        label_widget = ctk.CTkLabel(
            wrapper, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        label_widget.pack(anchor="w", pady=(0, 6))

        self.address_textbox = ctk.CTkTextbox(
            wrapper,
            height=90,
            corner_radius=CORNER_RADIUS,
            fg_color=COLOR_CARD,
            border_width=1,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT_DARK,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
        )
        self.address_textbox.pack(fill="x")

    # ----------------------------------------------------------------
    # RIGHT SIDE — RECENTLY ADDED TEACHERS
    # ----------------------------------------------------------------
    def _build_recent_card(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=1, sticky="nsew")

        heading = ctk.CTkLabel(
            card, text="Recent Added Teachers",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        heading.pack(anchor="w", padx=24, pady=(24, 16))

        for teacher in RECENT_TEACHERS:
            self._add_recent_teacher_card(card, teacher)

    def _add_recent_teacher_card(self, parent, teacher):
        item = ctk.CTkFrame(parent, fg_color=COLOR_PANEL, corner_radius=CORNER_RADIUS)
        item.pack(fill="x", padx=24, pady=8)

        id_label = ctk.CTkLabel(
            item, text=teacher["id"],
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_PRIMARY, anchor="w",
        )
        id_label.pack(anchor="w", padx=16, pady=(12, 0))

        name_label = ctk.CTkLabel(
            item, text=teacher["name"],
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        name_label.pack(anchor="w", padx=16, pady=(2, 0))

        dept_label = ctk.CTkLabel(
            item, text=teacher["department"],
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_GRAY, anchor="w",
        )
        dept_label.pack(anchor="w", padx=16, pady=(0, 12))

    # ----------------------------------------------------------------
    # BOTTOM BAR — CLEAR / SAVE BUTTONS
    # ----------------------------------------------------------------
    def _build_bottom_bar(self, parent):
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

        save_btn = ctk.CTkButton(
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
        save_btn.pack(side="right")

    # ----------------------------------------------------------------
    # FUNCTIONS
    # ----------------------------------------------------------------
    def save_teacher(self):
        print("[save_teacher] Saving new teacher record...")
        print(f"  Full Name: {self.entries['full_name'].get()}")
        print(f"  Email: {self.entries['email'].get()}")
        print(f"  Phone: {self.entries['phone'].get()}")
        print(f"  Date of Birth: {self.entries['dob'].get()}")
        print(f"  Department: {self.department_combo.get()}")
        print(f"  Designation: {self.designation_combo.get()}")
        print(f"  Gender: {self.gender_var.get()}")
        print(f"  Qualification: {self.entries['qualification'].get()}")
        print(f"  Experience (Years): {self.entries['experience'].get()}")
        print(f"  Salary: {self.entries['salary'].get()}")
        print(f"  Status: {self.status_combo.get()}")
        print(f"  Address: {self.address_textbox.get('1.0', 'end').strip()}")

    def clear_fields(self):
        print("[clear_fields] Clearing all form fields.")
        for key, entry in self.entries.items():
            if key == "teacher_id":
                continue
            entry.delete(0, "end")
        self.department_combo.set(DEPARTMENT_VALUES[0])
        self.designation_combo.set(DESIGNATION_VALUES[0])
        self.status_combo.set(STATUS_VALUES[0])
        self.gender_var.set("Male")
        self.address_textbox.delete("1.0", "end")

    def go_back(self):
        print("[go_back] Navigating back to previous page.")
        if self.back_callback:
            self.back_callback()
        else:
            self.destroy()


if __name__ == "__main__":
    app = AddTeacherPage(back_callback=None)
    app.mainloop()