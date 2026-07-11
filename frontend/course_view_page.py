"""
College Management System
Page: View Course

CustomTkinter only. Embeddable CTkFrame — same pattern as ViewStudentPage.
Displays only real database fields: course_id, course_name, duration,
description.
"""

import customtkinter as ctk

# ------------------------------------------------------------------
# GLOBAL APPEARANCE
# ------------------------------------------------------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# ------------------------------------------------------------------
# DESIGN SYSTEM CONSTANTS
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
SPACING_LG = 24
SPACING_MD = 24
PADDING_CONTENT = 24

DETAILS_COL_WEIGHT = 7
SUMMARY_COL_WEIGHT = 3

# ------------------------------------------------------------------
# DUMMY DATA — used only if no course_data is passed in
# ------------------------------------------------------------------
DUMMY_COURSE = {
    "course_id": "CRS-0001",
    "course_name": "Computer Science",
    "duration": "4 Years",
    "description": (
        "An introductory course covering the fundamentals of computer "
        "science, including problem solving, algorithms, and an overview "
        "of programming concepts. Designed to build a strong foundation "
        "for further study in the discipline."
    ),
}


class ViewCoursePage(ctk.CTkFrame):
    def __init__(self, parent, course_data=None, back_callback=None):
        super().__init__(parent, fg_color=COLOR_BG)

        self.course_data = course_data if course_data else DUMMY_COURSE
        self.back_callback = back_callback

        self._build_layout()

    # ----------------------------------------------------------------
    # LAYOUT
    # ----------------------------------------------------------------
    def _build_layout(self):
        container = ctk.CTkFrame(self, fg_color=COLOR_BG)
        container.pack(fill="both", expand=True, padx=SPACING_LG, pady=SPACING_LG)

        self._build_header(container)

        body = ctk.CTkFrame(container, fg_color=COLOR_BG)
        body.pack(fill="both", expand=True, pady=(SPACING_MD, 0))
        body.grid_columnconfigure(0, weight=DETAILS_COL_WEIGHT)
        body.grid_columnconfigure(1, weight=SUMMARY_COL_WEIGHT)
        body.grid_rowconfigure(0, weight=1)

        self._build_details_card(body)
        self._build_summary_card(body)

        self._build_bottom_bar(container)

    # ----------------------------------------------------------------
    # SHARED CARD HELPER
    # ----------------------------------------------------------------
    def _create_shadow_card(self, parent, row, column, padx=(0, 0)):
        wrapper = ctk.CTkFrame(parent, fg_color=COLOR_BG)
        wrapper.grid(row=row, column=column, sticky="nsew", padx=padx)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(0, weight=1)

        shadow = ctk.CTkFrame(wrapper, fg_color=COLOR_BORDER, corner_radius=18)
        shadow.grid(row=0, column=0, sticky="nsew")

        card = ctk.CTkFrame(
            shadow, fg_color=COLOR_CARD, corner_radius=16,
            border_width=1, border_color=COLOR_BORDER,
        )
        card.pack(fill="both", expand=True, padx=(0, 3), pady=(0, 3))
        return card

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
            font=ctk.CTkFont(family=FONT_FAMILY, size=26, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        title.pack(anchor="w", pady=(10, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="Complete details of the selected course.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_GRAY,
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    # ----------------------------------------------------------------
    # LEFT SIDE — COURSE INFORMATION CARD (≈70% width)
    # ----------------------------------------------------------------
    def _build_details_card(self, parent):
        card = self._create_shadow_card(parent, row=0, column=0, padx=(0, SPACING_MD))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=PADDING_CONTENT, pady=PADDING_CONTENT)

        heading = ctk.CTkLabel(
            inner, text="Course Information",
            font=ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        heading.pack(anchor="w", pady=(0, 14))

        grid_frame = ctk.CTkFrame(inner, fg_color="transparent")
        grid_frame.pack(fill="x")
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=2)
        grid_frame.grid_columnconfigure(2, weight=1)

        self._add_detail_row(
            grid_frame, "Course ID", self.course_data.get("course_id", ""),
            row=0, column=0, padx=(0, 8),
        )
        self._add_detail_row(
            grid_frame, "Course Name", self.course_data.get("course_name", ""),
            row=0, column=1, padx=(8, 8),
        )
        self._add_detail_row(
            grid_frame, "Duration", self.course_data.get("duration", ""),
            row=0, column=2, padx=(8, 0),
        )

        desc_label = ctk.CTkLabel(
            inner, text="Description",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_GRAY, anchor="w",
        )
        desc_label.pack(anchor="w", pady=(18, 8))

        desc_box = ctk.CTkFrame(inner, fg_color=COLOR_PANEL, corner_radius=CORNER_RADIUS)
        desc_box.pack(fill="both", expand=True)

        desc_value = ctk.CTkLabel(
            desc_box,
            text=self.course_data.get("description", ""),
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_DARK,
            justify="left",
            anchor="nw",
            wraplength=520,
        )
        desc_value.pack(fill="both", expand=True, padx=18, pady=16)

        def _sync_wrap(event):
            desc_value.configure(wraplength=max(200, event.width - 36))

        desc_box.bind("<Configure>", _sync_wrap)

    def _add_detail_row(self, parent, label, value, row, column, padx):
        container = ctk.CTkFrame(parent, fg_color=COLOR_PANEL, corner_radius=CORNER_RADIUS)
        container.grid(row=row, column=column, sticky="nsew", padx=padx, pady=0)

        label_widget = ctk.CTkLabel(
            container, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_GRAY, anchor="w",
        )
        label_widget.pack(anchor="w", padx=16, pady=(14, 8))

        value_widget = ctk.CTkLabel(
            container, text=str(value),
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLOR_TEXT_DARK, anchor="w",
            wraplength=200, justify="left",
        )
        value_widget.pack(anchor="w", padx=16, pady=(0, 14))

    # ----------------------------------------------------------------
    # RIGHT SIDE — SUMMARY CARD, profile style (≈30% width)
    # ----------------------------------------------------------------
    def _build_summary_card(self, parent):
        card = self._create_shadow_card(parent, row=0, column=1)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(expand=True, padx=PADDING_CONTENT)

        icon_circle = ctk.CTkFrame(
            content, width=110, height=110, corner_radius=55, fg_color=COLOR_PANEL,
        )
        icon_circle.pack(pady=(4, 18))
        icon_circle.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            icon_circle, text="📘",
            font=ctk.CTkFont(family=FONT_FAMILY, size=42),
            text_color=COLOR_PRIMARY,
        )
        icon_label.pack(expand=True)

        name_label = ctk.CTkLabel(
            content, text=self.course_data.get("course_name", ""),
            font=ctk.CTkFont(family=FONT_FAMILY, size=19, weight="bold"),
            text_color=COLOR_TEXT_DARK,
            wraplength=220, justify="center",
        )
        name_label.pack(pady=(0, 8))

        id_badge = ctk.CTkLabel(
            content, text=self.course_data.get("course_id", ""),
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_PRIMARY, fg_color=COLOR_PANEL,
            corner_radius=8, width=110, height=30,
        )
        id_badge.pack(pady=(0, 20))

        divider = ctk.CTkFrame(content, fg_color=COLOR_BORDER, height=1, width=220)
        divider.pack(pady=(0, 18))

        self._add_summary_row(content, "Duration", self.course_data.get("duration", ""))

        preview_title = ctk.CTkLabel(
            content, text="Description",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_GRAY,
        )
        preview_title.pack(pady=(16, 6))

        preview_value = ctk.CTkLabel(
            content,
            text=self._preview_text(self.course_data.get("description", "")),
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_DARK,
            wraplength=220, justify="left",
        )
        preview_value.pack(pady=(0, 4))

    def _add_summary_row(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(pady=9)

        label_widget = ctk.CTkLabel(
            row, text=label,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_GRAY,
        )
        label_widget.pack()

        value_widget = ctk.CTkLabel(
            row, text=str(value),
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLOR_TEXT_DARK,
        )
        value_widget.pack(pady=(3, 0))

    @staticmethod
    def _preview_text(text, limit=110):
        text = text or ""
        if len(text) <= limit:
            return text
        trimmed = text[:limit].rsplit(" ", 1)[0]
        return trimmed + "…"

    # ----------------------------------------------------------------
    # BOTTOM BAR — BACK BUTTON
    # ----------------------------------------------------------------
    def _build_bottom_bar(self, parent):
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
        print("[go_back] Navigating back to Course Management page.")
        if self.back_callback:
            self.back_callback()


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("College Management System - View Course")
    root.geometry("1300x800")
    root.configure(fg_color=COLOR_BG)

    page = ViewCoursePage(root, course_data=None, back_callback=None)
    page.pack(fill="both", expand=True)

    root.mainloop()