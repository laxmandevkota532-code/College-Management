import customtkinter as ctk

# ------------------------------------------------------------------
# DESIGN SYSTEM CONSTANTS (same as ViewStudentPage / ViewCoursePage)
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
# DUMMY DATA — used if no teacher_data is passed in
# ------------------------------------------------------------------
DUMMY_TEACHER = {
    "teacher_id": "T001",
    "teacher_name": "Hari Sharma",
    "department": "Computer Science",
    "email": "hari@gmail.com",
    "phone": "9800000000",
    "qualification": "MSc Computer Science",
    "experience": "5 Years",
    "status": "Active",
    "description": "Senior Computer Science Teacher"
}


class ViewTeacherPage(ctk.CTkFrame):
    """
    ViewTeacherPage: A frame-based UI for displaying teacher details.
    
    Integrates with backend.teacher_crud for database operations.
    Displays complete teacher information in read-only format.
    """

    def __init__(self, parent, teacher_data=None, back_callback=None):
        """
        Initialize the ViewTeacherPage frame.
        
        Args:
            parent: Parent widget.
            teacher_data: Dictionary containing teacher information.
            back_callback: Callback function to execute when Back button is clicked.
        """
        super().__init__(parent, fg_color=COLOR_BG)

        self.teacher_data = teacher_data if teacher_data else DUMMY_TEACHER
        self.back_callback = back_callback

        self._build_layout()

    # ----------------------------------------------------------------
    # LAYOUT
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

        self._build_details_card(body)
        self._build_summary_card(body)

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
            text="View Teacher",
            font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        title.pack(anchor="w", pady=(12, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="Complete details of the selected teacher.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14),
            text_color=COLOR_TEXT_GRAY,
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    # ----------------------------------------------------------------
    # LEFT SIDE — TEACHER DETAILS CARD (READ-ONLY)
    # ----------------------------------------------------------------
    def _build_details_card(self, parent):
        """Build the detailed teacher information card."""
        card = ctk.CTkFrame(
            parent, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING_MD))

        heading = ctk.CTkLabel(
            card, text="Teacher Information",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        heading.pack(anchor="w", padx=24, pady=(24, 16))

        fields = [
            ("Teacher ID", self.teacher_data.get("teacher_id", "N/A")),
            ("Teacher Name", self.teacher_data.get("teacher_name", "N/A")),
            ("Email Address", self.teacher_data.get("email", "N/A")),
            ("Phone Number", self.teacher_data.get("phone", "N/A")),
            ("Department", self.teacher_data.get("department", "N/A")),
            ("Qualification", self.teacher_data.get("qualification", "N/A")),
            ("Experience", self.teacher_data.get("experience", "N/A")),
            ("Status", self.teacher_data.get("status", "N/A")),
            ("Description", self.teacher_data.get("description", "N/A")),
        ]

        for label, value in fields:
            self._add_detail_row(card, label, value)

    def _add_detail_row(self, parent, label, value):
        """
        Add a single detail row to the card.
        
        Args:
            parent: Parent widget.
            label: Field label text.
            value: Field value text.
        """
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
    # RIGHT SIDE — TEACHER SUMMARY CARD
    # ----------------------------------------------------------------
    def _build_summary_card(self, parent):
        """Build the teacher summary card with avatar and key information."""
        card = ctk.CTkFrame(
            parent, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        card.grid(row=0, column=1, sticky="nsew")

        heading = ctk.CTkLabel(
            card, text="Teacher Summary",
            font=ctk.CTkFont(family=FONT_FAMILY, size=17, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        heading.pack(anchor="w", padx=24, pady=(24, 8))

        # Avatar placeholder
        avatar_circle = ctk.CTkFrame(
            card, width=90, height=90, corner_radius=45, fg_color=COLOR_PANEL,
        )
        avatar_circle.pack(pady=(16, 16))
        avatar_circle.pack_propagate(False)

        avatar_label = ctk.CTkLabel(
            avatar_circle, text="👨‍🏫",
            font=ctk.CTkFont(family=FONT_FAMILY, size=32),
            text_color=COLOR_PRIMARY,
        )
        avatar_label.pack(expand=True)

        name_label = ctk.CTkLabel(
            card, text=self.teacher_data.get("teacher_name", "N/A"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        name_label.pack(pady=(0, 4))

        id_badge = ctk.CTkLabel(
            card, text=self.teacher_data.get("teacher_id", "N/A"),
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_PRIMARY, fg_color=COLOR_PANEL,
            corner_radius=8, width=90, height=28,
        )
        id_badge.pack(pady=(0, 16))

        divider = ctk.CTkFrame(card, fg_color=COLOR_BORDER, height=1)
        divider.pack(fill="x", padx=24, pady=(0, 16))

        self._add_summary_row(card, "Department", self.teacher_data.get("department", "N/A"))
        self._add_summary_row(card, "Qualification", self.teacher_data.get("qualification", "N/A"))
        self._add_summary_row(card, "Experience", self.teacher_data.get("experience", "N/A"))

        # Status badge
        status = self.teacher_data.get("status", "N/A")
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

    def _add_summary_row(self, parent, label, value):
        """
        Add a single summary row to the summary card.
        
        Args:
            parent: Parent widget.
            label: Field label text.
            value: Field value text.
        """
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
    # BOTTOM BAR — SINGLE BACK BUTTON ONLY
    # ----------------------------------------------------------------
    def _build_bottom_bar(self, parent):
        """Build the bottom button bar with back button."""
        top_divider = ctk.CTkFrame(parent, fg_color=COLOR_BORDER, height=1)
        top_divider.pack(fill="x", pady=(SPACING_MD, 0))

        bottom_bar = ctk.CTkFrame(parent, fg_color=COLOR_BG)
        bottom_bar.pack(fill="x", pady=(SPACING_MD, 0))
        bottom_bar.grid_columnconfigure(0, weight=1)
        bottom_bar.grid_columnconfigure(1, weight=0)

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
        """Navigate back to the previous page."""
        if self.back_callback:
            self.back_callback()


if __name__ == "__main__":
    # Standalone preview for testing
    root = ctk.CTk()
    root.geometry("1300x800")
    root.title("College Management System - View Teacher")
    root.configure(fg_color=COLOR_BG)

    page = ViewTeacherPage(
        root,
        teacher_data=DUMMY_TEACHER
    )

    page.pack(fill="both", expand=True)

    root.mainloop()