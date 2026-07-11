import customtkinter as ctk
from tkinter import messagebox

from backend.course_crud import (
    get_all_courses,
    delete_course
)

# Set appearance mode and default color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class CoursesPage(ctk.CTkFrame):
    def __init__(self, master, open_add_course_callback=None, open_view_course_callback=None):
        super().__init__(master, fg_color="#F8F9FC")

        # Navigation Callback Injection
        self.open_add_course_callback = open_add_course_callback
        self.open_view_course_callback = open_view_course_callback

        # --- Color Palette ---
        self.PRIMARY_BLUE = "#4F5BD5"
        self.HOVER_BLUE = "#3F4ACB"
        self.BACKGROUND = "#F8F9FC"
        self.PANEL_BG = "#EEF2FF"
        self.TEXT_DARK = "#111827"
        self.TEXT_GRAY = "#6B7280"
        self.WHITE = "#FFFFFF"
        self.SUCCESS_GREEN = "#10B981"
        self.DANGER_RED = "#EF4444"

        # Responsive Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_main_content()

    def create_main_content(self):
        """Builds responsive layout area panel structures."""
        main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=self.BACKGROUND)
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)

        # Top Bar Container Setup Row
        top_bar = ctk.CTkFrame(main_container, height=70, corner_radius=0, fg_color=self.WHITE)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_propagate(False)
        
        page_title = ctk.CTkLabel(top_bar, text="Courses Management", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.TEXT_DARK)
        page_title.grid(row=0, column=0, padx=30, pady=20, sticky="w")
        
        user_profile = ctk.CTkLabel(top_bar, text="Admin User", font=ctk.CTkFont(size=14), text_color=self.TEXT_GRAY)
        user_profile.grid(row=0, column=1, padx=30, pady=20, sticky="e")

        # Top Action Bar Layout Container Subsystem
        action_bar = ctk.CTkFrame(main_container, fg_color="transparent")
        action_bar.grid(row=1, column=0, padx=30, pady=(25, 15), sticky="ew")
        action_bar.grid_columnconfigure(0, weight=1)

        search_entry = ctk.CTkEntry(action_bar, placeholder_text="Search Course...", width=300, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, text_color=self.TEXT_DARK)
        search_entry.grid(row=0, column=0, sticky="w")

        add_btn = ctk.CTkButton(
            action_bar, text="+ Add Course", font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE,
            height=40, corner_radius=6,
            command=self.open_add_course
        )
        add_btn.grid(row=0, column=1, sticky="e")

        # Central Layout Data Matrix Display Segment System Box Layer
        table_container = ctk.CTkFrame(main_container, fg_color=self.WHITE, corner_radius=8)
        table_container.grid(row=2, column=0, padx=30, pady=(0, 30), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        # Matrix Headers Configuration
        headers = ["Course ID", "Course Name", "Duration", "Description", "Actions"]
        columns_width = [110, 160, 120, 220, 160]

        header_frame = ctk.CTkFrame(table_container, fg_color=self.PANEL_BG, height=45, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        
        for idx, header in enumerate(headers):
            header_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])
            lbl = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            lbl.grid(row=0, column=idx, padx=15, pady=10, sticky="ew")

        # Scrollable Frame Construction Injection
        self.scroll_frame = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        
        for idx in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])

        self.populate_table_data()

    def populate_table_data(self):
        """Loads courses from the database and renders them into the table."""

        # Clear any existing rows before re-rendering (needed for refresh after delete)
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        courses = get_all_courses()

        for row_idx, course in enumerate(courses):

            id_lbl = ctk.CTkLabel(self.scroll_frame, text=course["course_id"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            id_lbl.grid(row=row_idx, column=0, padx=15, pady=12, sticky="ew")

            name_lbl = ctk.CTkLabel(self.scroll_frame, text=course["course_name"], font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            name_lbl.grid(row=row_idx, column=1, padx=15, pady=12, sticky="ew")

            duration_lbl = ctk.CTkLabel(self.scroll_frame, text=course["duration"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            duration_lbl.grid(row=row_idx, column=2, padx=15, pady=12, sticky="ew")

            description_lbl = ctk.CTkLabel(self.scroll_frame, text=course["description"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            description_lbl.grid(row=row_idx, column=3, padx=15, pady=12, sticky="ew")

            # Action Frame Layout Container Row Grid Integration Line Logic
            action_panel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            action_panel.grid(row=row_idx, column=4, padx=15, pady=12, sticky="ew")

            view_btn = ctk.CTkButton(
                action_panel, text="View", font=ctk.CTkFont(size=11),
                fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE,
                width=42, height=24, corner_radius=4,
                command=lambda c=course: self.open_view_course(c)
            )
            view_btn.grid(row=0, column=0, padx=2)

            delete_btn = ctk.CTkButton(
                action_panel, text="Delete", font=ctk.CTkFont(size=11),
                fg_color="#FEE2E2", hover_color="#FCA5A5", text_color=self.DANGER_RED,
                width=46, height=24, corner_radius=4,
                command=lambda c=course: self.handle_delete_course(c)
            )
            delete_btn.grid(row=0, column=1, padx=2)

    def handle_delete_course(self, course):
        """Confirms, deletes the course from the database, then refreshes the table."""
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {course['course_name']} ({course['course_id']})?"
        )
        if not confirm:
            return

        delete_course(course["course_id"])
        self.populate_table_data()

    def open_add_course(self):
        """Triggers Add Course page navigation via parent dashboard callback injection."""
        if self.open_add_course_callback:
            self.open_add_course_callback()

    def open_view_course(self, course):
        """Triggers View Course page with course data via parent dashboard callback injection."""
        if self.open_view_course_callback:
            self.open_view_course_callback(course)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x700")
    page = CoursesPage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()