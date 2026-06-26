"""
Student Management System - UI Only
Designed to be embedded inside an existing Dashboard (no sidebar, no navbar).
Requires: pip install customtkinter
"""

import customtkinter as ctk

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
BG_PAGE         = "#F8F9FC"
BG_CARD         = "#FFFFFF"
BG_HEADER_ROW   = "#F3F4F6"
BG_ALT_ROW      = "#F9FAFB"
BG_ROW          = "#FFFFFF"

COLOR_PRIMARY   = "#4F5BD5"
COLOR_HOVER     = "#3F4ACB"
COLOR_BORDER    = "#E5E7EB"
COLOR_DIVIDER   = "#E5E7EB"
COLOR_TEXT      = "#111827"
COLOR_SECONDARY = "#6B7280"
COLOR_READONLY  = "#F3F4F6"

BADGE_SUCCESS_BG   = "#D1FAE5"
BADGE_SUCCESS_FG   = "#065F46"
BADGE_INACTIVE_BG  = "#FEE2E2"
BADGE_INACTIVE_FG  = "#991B1B"

FONT_FAMILY = "Segoe UI"

COURSES = ["Computer Science", "Information Technology", "Business Admin",
           "Electrical Engineering", "Mechanical Engineering", "Civil Engineering",
           "Mathematics", "Physics", "Chemistry", "Economics"]

STATUSES = ["Active", "Inactive"]

GENDER_OPTIONS = ["Male", "Female", "Other"]

TABLE_HEADERS = ["Student ID", "Full Name", "Course", "Email Address", "Phone Number", "Status"]

DUMMY_RECORDS = [
    ("STU-0001", "Alice Johnson",   "Computer Science",        "alice@uni.edu",   "+1-202-555-0101", "Active"),
    ("STU-0002", "Bob Martinez",    "Information Technology",  "bob@uni.edu",     "+1-202-555-0102", "Inactive"),
    ("STU-0003", "Clara Kim",       "Business Admin",          "clara@uni.edu",   "+1-202-555-0103", "Active"),
    ("STU-0004", "David Osei",      "Electrical Engineering",  "david@uni.edu",   "+1-202-555-0104", "Active"),
    ("STU-0005", "Elena Petrov",    "Mathematics",             "elena@uni.edu",   "+1-202-555-0105", "Inactive"),
]


# ─────────────────────────────────────────────
# STUDENT MANAGEMENT PAGE
# ─────────────────────────────────────────────
class StudentManagementPage(ctk.CTkFrame):
    """
    Top-level page widget. Drop this into any parent container.
    The host dashboard is responsible for placing / packing / gridding this widget.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=BG_PAGE, **kwargs)
        self.gender_var = ctk.StringVar(value="Male")
        self._build_page_header()
        self._build_body()

    # ─── Page Header ──────────────────────────
    def _build_page_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=BG_PAGE)
        header_frame.pack(fill="x", padx=28, pady=(24, 0))

        ctk.CTkLabel(
            header_frame,
            text="Student Management",
            font=(FONT_FAMILY, 22, "bold"),
            text_color=COLOR_TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Manage student records efficiently.",
            font=(FONT_FAMILY, 13),
            text_color=COLOR_SECONDARY,
        ).pack(anchor="w", pady=(2, 0))

    # ─── Two-column body ──────────────────────
    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color=BG_PAGE)
        body.pack(fill="both", expand=True, padx=28, pady=20)

        body.columnconfigure(0, weight=40)   # left card  ~40 %
        body.columnconfigure(1, weight=60)   # right card ~60 %
        body.rowconfigure(0, weight=1)

        self._build_form_card(body)
        self._build_table_card(body)

    # ─────────────────────────────────────────
    # LEFT CARD — Register New Student
    # ─────────────────────────────────────────
    def _build_form_card(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Card title
        ctk.CTkLabel(
            card,
            text="Register New Student",
            font=(FONT_FAMILY, 15, "bold"),
            text_color=COLOR_TEXT,
        ).pack(anchor="w", padx=20, pady=(18, 0))

        # Divider
        self._divider(card)

        # Scrollable form area
        scroll_area = ctk.CTkScrollableFrame(
            card,
            fg_color=BG_CARD,
            scrollbar_button_color=COLOR_BORDER,
            scrollbar_button_hover_color=COLOR_SECONDARY,
        )
        scroll_area.pack(fill="both", expand=True, padx=0, pady=0)
        scroll_area.columnconfigure(0, weight=1)
        scroll_area.columnconfigure(1, weight=1)

        self._build_form(scroll_area)

        # ── Fixed buttons (outside scroll) ────
        btn_frame = ctk.CTkFrame(card, fg_color=BG_CARD)
        btn_frame.pack(fill="x", padx=20, pady=(10, 18))
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Add Student",
            font=(FONT_FAMILY, 13, "bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_HOVER,
            text_color="#FFFFFF",
            corner_radius=8,
            height=38,
            command=self.add_student,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            btn_frame,
            text="Clear",
            font=(FONT_FAMILY, 13),
            fg_color=BG_CARD,
            hover_color=BG_HEADER_ROW,
            text_color=COLOR_TEXT,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=8,
            height=38,
            command=self.clear_fields,
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    # ─── Form fields ──────────────────────────
    def _build_form(self, parent):
        pad_x = 20

        # Row 0 — Student ID | Full Name
        self._create_label(parent, "Student ID", 0, 0, padx=(pad_x, 6))
        self._create_label(parent, "Full Name",  0, 1, padx=(6, pad_x))

        self.entry_student_id = self._create_entry(
            parent, placeholder="Auto-generated", row=1, col=0,
            padx=(pad_x, 6), state="readonly"
        )
        self.entry_full_name = self._create_entry(
            parent, placeholder="e.g. Alice Johnson", row=1, col=1,
            padx=(6, pad_x)
        )

        # Row 1 — Email | Phone
        self._create_label(parent, "Email",        2, 0, padx=(pad_x, 6), pady_top=10)
        self._create_label(parent, "Phone Number", 2, 1, padx=(6, pad_x), pady_top=10)

        self.entry_email = self._create_entry(
            parent, placeholder="alice@example.com", row=3, col=0,
            padx=(pad_x, 6)
        )
        self.entry_phone = self._create_entry(
            parent, placeholder="+1-202-555-0000", row=3, col=1,
            padx=(6, pad_x)
        )

        # Row 2 — Date of Birth | Course
        self._create_label(parent, "Date of Birth", 4, 0, padx=(pad_x, 6), pady_top=10)
        self._create_label(parent, "Course",         4, 1, padx=(6, pad_x), pady_top=10)

        self.entry_dob = self._create_entry(
            parent, placeholder="YYYY-MM-DD", row=5, col=0,
            padx=(pad_x, 6)
        )
        self.combo_course = self._create_combobox(
            parent, values=COURSES, row=5, col=1,
            padx=(6, pad_x)
        )

        # Row 3 — Gender (full-width, radio buttons)
        self._create_label(parent, "Gender", 6, 0, padx=(pad_x, 6), pady_top=10,
                           columnspan=2)

        gender_frame = ctk.CTkFrame(parent, fg_color=BG_CARD)
        gender_frame.grid(row=7, column=0, columnspan=2, sticky="ew",
                          padx=pad_x, pady=(0, 0))

        for i, g in enumerate(GENDER_OPTIONS):
            ctk.CTkRadioButton(
                gender_frame,
                text=g,
                variable=self.gender_var,
                value=g,
                font=(FONT_FAMILY, 12),
                text_color=COLOR_TEXT,
                fg_color=COLOR_PRIMARY,
                border_color=COLOR_BORDER,
            ).grid(row=0, column=i, padx=(0, 20), pady=4, sticky="w")

        # Row 4 — Address (full-width, multiline)
        self._create_label(parent, "Address", 8, 0, padx=(pad_x, 6), pady_top=10,
                           columnspan=2)
        self.textbox_address = self._create_textbox(
            parent, row=9, col=0, padx=pad_x, columnspan=2
        )

        # Row 5 — Status (full-width)
        self._create_label(parent, "Status", 10, 0, padx=(pad_x, 6), pady_top=10,
                           columnspan=2)
        self.combo_status = self._create_combobox(
            parent, values=STATUSES, row=11, col=0,
            padx=pad_x, columnspan=2
        )

        # Spacer at bottom so scrollable area has breathing room
        ctk.CTkFrame(parent, fg_color=BG_CARD, height=12).grid(
            row=12, column=0, columnspan=2
        )

    # ─────────────────────────────────────────
    # RIGHT CARD — Recent Students Table
    # ─────────────────────────────────────────
    def _build_table_card(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Card title
        ctk.CTkLabel(
            card,
            text="Recent Students",
            font=(FONT_FAMILY, 15, "bold"),
            text_color=COLOR_TEXT,
        ).pack(anchor="w", padx=20, pady=(18, 0))

        self._divider(card)

        # Table container
        table_frame = ctk.CTkFrame(card, fg_color=BG_CARD)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self._build_table(table_frame)

    # ─── Table (manual grid) ──────────────────
    def _build_table(self, parent):
        col_weights = [14, 18, 20, 22, 16, 10]
        for i, w in enumerate(col_weights):
            parent.columnconfigure(i, weight=w)

        # ── Header row ────────────────────────
        for col, header in enumerate(TABLE_HEADERS):
            cell = ctk.CTkFrame(parent, fg_color=BG_HEADER_ROW, corner_radius=0)
            cell.grid(row=0, column=col, sticky="nsew", padx=(0, 1), pady=(0, 1))

            ctk.CTkLabel(
                cell,
                text=header,
                font=(FONT_FAMILY, 12, "bold"),
                text_color=COLOR_SECONDARY,
                anchor="w",
            ).pack(anchor="w", padx=12, pady=10)

        # ── Data rows ─────────────────────────
        for row_idx, record in enumerate(DUMMY_RECORDS, start=1):
            bg = BG_ROW if row_idx % 2 == 0 else BG_ALT_ROW

            for col_idx, value in enumerate(record):
                cell = ctk.CTkFrame(parent, fg_color=bg, corner_radius=0)
                cell.grid(row=row_idx, column=col_idx, sticky="nsew",
                          padx=(0, 1), pady=(0, 1))

                if col_idx == 5:   # Status column → pill badge
                    badge = self._build_status_badge(cell, value)
                    badge.pack(anchor="w", padx=12, pady=8)
                else:
                    ctk.CTkLabel(
                        cell,
                        text=value,
                        font=(FONT_FAMILY, 12),
                        text_color=COLOR_TEXT,
                        anchor="w",
                        wraplength=0,
                    ).pack(anchor="w", padx=12, pady=10)

        # Push all rows to the top; let the last row absorb remaining space
        parent.rowconfigure(len(DUMMY_RECORDS) + 1, weight=1)
        spacer = ctk.CTkFrame(parent, fg_color=BG_CARD)
        spacer.grid(row=len(DUMMY_RECORDS) + 1, column=0,
                    columnspan=len(TABLE_HEADERS), sticky="nsew")

    # ─────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────
    def _divider(self, parent):
        line = ctk.CTkFrame(parent, fg_color=COLOR_DIVIDER, height=1)
        line.pack(fill="x", padx=0, pady=(12, 0))

    def _create_label(self, parent, text, row, col, padx=(0, 0),
                      pady_top=4, columnspan=1):
        ctk.CTkLabel(
            parent,
            text=text,
            font=(FONT_FAMILY, 12, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).grid(row=row, column=col, columnspan=columnspan,
               sticky="ew", padx=padx, pady=(pady_top, 2))

    def _create_entry(self, parent, placeholder, row, col,
                      padx=(0, 0), state="normal", columnspan=1):
        fg     = COLOR_READONLY if state == "readonly" else BG_CARD
        text_c = COLOR_SECONDARY if state == "readonly" else COLOR_TEXT

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=(FONT_FAMILY, 12),
            fg_color=fg,
            text_color=text_c,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=7,
            height=36,
            state=state,
        )
        entry.grid(row=row, column=col, columnspan=columnspan,
                   sticky="ew", padx=padx, pady=(0, 0))
        return entry

    def _create_combobox(self, parent, values, row, col,
                         padx=(0, 0), columnspan=1):
        combo = ctk.CTkComboBox(
            parent,
            values=values,
            font=(FONT_FAMILY, 12),
            fg_color=BG_CARD,
            text_color=COLOR_TEXT,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=7,
            button_color=COLOR_BORDER,
            button_hover_color=COLOR_SECONDARY,
            dropdown_fg_color=BG_CARD,
            dropdown_text_color=COLOR_TEXT,
            dropdown_hover_color=BG_HEADER_ROW,
            height=36,
            state="readonly",
        )
        combo.set(values[0])
        combo.grid(row=row, column=col, columnspan=columnspan,
                   sticky="ew", padx=padx, pady=(0, 0))
        return combo

    def _create_textbox(self, parent, row, col, padx=(0, 0), columnspan=2):
        box = ctk.CTkTextbox(
            parent,
            font=(FONT_FAMILY, 12),
            fg_color=BG_CARD,
            text_color=COLOR_TEXT,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=7,
            height=80,
        )
        box.grid(row=row, column=col, columnspan=columnspan,
                 sticky="ew", padx=padx, pady=(0, 0))
        return box

    def _build_status_badge(self, parent, status: str) -> ctk.CTkFrame:
        is_active  = status.strip().lower() == "active"
        bg_color   = BADGE_SUCCESS_BG  if is_active else BADGE_INACTIVE_BG
        text_color = BADGE_SUCCESS_FG  if is_active else BADGE_INACTIVE_FG

        pill = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=20)
        ctk.CTkLabel(
            pill,
            text=status,
            font=(FONT_FAMILY, 11, "bold"),
            text_color=text_color,
        ).pack(padx=10, pady=3)
        return pill

    # ─────────────────────────────────────────
    # CALLBACKS (stubs only)
    # ─────────────────────────────────────────
    def add_student(self):
        pass

    def clear_fields(self):
        pass


# ─────────────────────────────────────────────
# STANDALONE RUNNER (for development / preview)
# ─────────────────────────────────────────────
def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Student Management System")

# Start maximized
    root.after(100, lambda: root.state("zoomed"))

# Minimum size if user restores the window
    root.minsize(1000, 650)

    root.configure(fg_color=BG_PAGE)
    page = StudentManagementPage(root)
    page.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()