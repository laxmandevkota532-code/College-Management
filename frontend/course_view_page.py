"""
College Management System
Page: View Course

Mirrors the exact design system, layout, and structure of the existing
ViewStudentPage — same header, same back button, same two-column layout,
same white cards, same bottom Back button. Course fields replace student
fields.

No database. No TreeView. No ttk/tkinter widgets — CustomTkinter only.
"""

import customtkinter as ctk

# ------------------------------------------------------------------
# GLOBAL APPEARANCE
# ------------------------------------------------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ------------------------------------------------------------------
# DESIGN SYSTEM CONSTANTS (same as ViewStudentPage)
# ------------------------------------------------------------------
COLOR_BG = "#F8F9FC"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY = "#4F5BD5"
COLOR_PRIMARY_HOVER = "#3F4ACB"
COLOR_PANEL = "#EEF2FF"
COLOR_TEXT_DARK = "#111827"
COLOR_TEXT_GRAY = "#6B7280"
COLOR_BORDER = "#E5E7EB"
COLOR_SUCCESS = "#16A34A"
COLOR_INACTIVE = "#6B7280"

FONT_FAMILY = "Segoe UI"

CORNER_RADIUS = 12
BUTTON_HEIGHT = 45
SPACING_LG = 30
SPACING_MD = 24

# ------------------------------------------------------------------
# DUMMY DATA — used if no course_data is passed in
# ------------------------------------------------------------------
DUMMY_COURSE = {
    "course_code": "CS101",
    "course_name": "Computer Science",
    "department": "Computer Science",
    "semester": "Semester 1",
    "credit_hours": 4,
    "teacher": "Dr. Ayesha Khan",
    "status": "Active",
    "description": (
        "An introductory course covering the fundamentals of computer "
        "science, including problem solving, algorithms, and an overview "
        "of programming concepts. Designed to build a strong foundation "
        "for further study in the discipline."
    ),
}


class ViewCoursePage(ctk.CTk):
    def __init__(self, course_data=None, back_callback=None):
        super().__init__()

        self.course_data = course_data if course_data else DUMMY_COURSE
        self.back_callback = back_callback

        self.title("College Management System - View Course")
        self.geometry("1300x800")
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

        self._build_details_card(body)
        self._build_summary_card(body)

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
            text="View Course",
            font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        title.pack(anchor="w", pady=(12, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="Complete details of the selected course.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            text_color=COLOR_TEXT_GRAY,
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    # ----------------------------------------------------------------
    # LEFT SIDE — COURSE DETAILS CARD
    # ----------------------------------------------------------------
    def _build_details_card(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_MD))

        heading = ctk.CTkLabel(
            card, text="Course Information",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        heading.pack(anchor="w", padx=24, pady=(24, 16))

        fields = [
            ("Course Code", self.course_data.get("course_code", "")),
            ("Course Name", self.course_data.get("course_name", "")),
            ("Department", self.course_data.get("department", "")),
            ("Semester", self.course_data.get("semester", "")),
            ("Credit Hours", str(self.course_data.get("credit_hours", ""))),
            ("Teacher", self.course_data.get("teacher", "")),
            ("Status", self.course_data.get("status", "")),
        ]

        for label, value in fields:
            self._add_detail_row(card, label, value)

        # Description block
        desc_label = ctk.CTkLabel(
            card, text="Description",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_GRAY, anchor="w",
        )
        desc_label.pack(anchor="w", padx=24, pady=(14, 6))

        desc_box = ctk.CTkFrame(card, fg_color=COLOR_PANEL, corner_radius=CORNER_RADIUS)
        desc_box.pack(fill="x", padx=24, pady=(0, 24))

        desc_value = ctk.CTkLabel(
            desc_box,
            text=self.course_data.get("description", ""),
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_DARK,
            justify="left",
            anchor="w",
            wraplength=560,
        )
        desc_value.pack(fill="x", padx=16, pady=14)

    def _add_detail_row(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=8)

        label_widget = ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_GRAY, anchor="w", width=140,
        )
        label_widget.pack(side="left")

        value_widget = ctk.CTkLabel(
            row, text=value,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        value_widget.pack(side="left", padx=(6, 0))

        divider = ctk.CTkFrame(parent, fg_color=COLOR_BORDER, height=1)
        divider.pack(fill="x", padx=24, pady=(4, 0))

    # ----------------------------------------------------------------
    # RIGHT SIDE — SUMMARY CARD
    # ----------------------------------------------------------------
    def _build_summary_card(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=1, sticky="nsew")

        # Icon placeholder (mirrors avatar circle used on ViewStudentPage)
        icon_circle = ctk.CTkFrame(
            card, width=90, height=90, corner_radius=45, fg_color=COLOR_PANEL,
        )
        icon_circle.pack(pady=(32, 16))
        icon_circle.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            icon_circle, text="📘",
            font=ctk.CTkFont(family=FONT_FAMILY, size=32),
            text_color=COLOR_PRIMARY,
        )
        icon_label.pack(expand=True)

        name_label = ctk.CTkLabel(
            card, text=self.course_data.get("course_name", ""),
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        name_label.pack(pady=(0, 4))

        code_badge = ctk.CTkLabel(
            card, text=self.course_data.get("course_code", ""),
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_PRIMARY, fg_color=COLOR_PANEL,
            corner_radius=8, width=90, height=28,
        )
        code_badge.pack(pady=(0, 16))

        divider = ctk.CTkFrame(card, fg_color=COLOR_BORDER, height=1)
        divider.pack(fill="x", padx=24, pady=(0, 16))

        self._add_summary_row(card, "Department", self.course_data.get("department", ""))
        self._add_summary_row(card, "Teacher", self.course_data.get("teacher", ""))

        # Status badge
        status = self.course_data.get("status", "")
        status_color = COLOR_SUCCESS if status.lower() == "active" else COLOR_INACTIVE

        status_row = ctk.CTkFrame(card, fg_color="transparent")
        status_row.pack(fill="x", padx=24, pady=10)

        status_title = ctk.CTkLabel(
            status_row, text="Status",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_GRAY, anchor="w",
        )
        status_title.pack(anchor="w")

        status_badge = ctk.CTkLabel(
            status_row, text=f"●  {status}",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=status_color, fg_color=COLOR_PANEL,
            corner_radius=8, width=110, height=30,
        )
        status_badge.pack(anchor="w", pady=(6, 0))

        self._add_summary_row(card, "Semester", self.course_data.get("semester", ""))
        self._add_summary_row(card, "Credits", str(self.course_data.get("credit_hours", "")))

    def _add_summary_row(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=10)

        label_widget = ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_GRAY, anchor="w",
        )
        label_widget.pack(anchor="w")

        value_widget = ctk.CTkLabel(
            row, text=value,
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
        )
        value_widget.pack(anchor="w", pady=(2, 0))

    # ----------------------------------------------------------------
    # BOTTOM BAR — BACK BUTTON
    # ----------------------------------------------------------------
    def _build_bottom_bar(self, parent):
        # Divider to visually separate content cards from the action bar
        top_divider = ctk.CTkFrame(parent, fg_color=COLOR_BORDER, height=1)
        top_divider.pack(fill="x", pady=(SPACING_MD, 0))

        bottom_bar = ctk.CTkFrame(parent, fg_color=COLOR_BG)
        bottom_bar.pack(fill="x", pady=(SPACING_MD, 0))
        bottom_bar.grid_columnconfigure(0, weight=1)
        bottom_bar.grid_columnconfigure(1, weight=0)

        # Right-aligned action area, matching the right-card edge above it
        action_area = ctk.CTkFrame(bottom_bar, fg_color="transparent")
        action_area.grid(row=0, column=1, sticky="e")

        back_btn = ctk.CTkButton(
            action_area,
            text="←  Back",
            width=140,
            height=BUTTON_HEIGHT,
            corner_radius=CORNER_RADIUS,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            command=self.go_back,
        )
        back_btn.pack(side="right")

    # ----------------------------------------------------------------
    # FUNCTIONS
    # ----------------------------------------------------------------
    def go_back(self):
        print("[go_back] Navigating back to Course Management page.")
        if self.back_callback:
            self.back_callback()
        else:
            self.destroy()


if __name__ == "__main__":
    # Standalone preview with dummy data
    app = ViewCoursePage(course_data=None, back_callback=None)
    app.mainloop()