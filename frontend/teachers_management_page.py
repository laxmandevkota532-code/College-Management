import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from backend.teacher_crud import get_all_teachers, search_teachers, delete_teacher

# Set appearance mode and default color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class TeachersPage(ctk.CTkFrame):
    def __init__(self, master, open_add_teacher_callback=None, open_view_teacher_callback=None, open_edit_teacher_callback=None):
        super().__init__(master, fg_color="#F8F9FC")

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

        # Callbacks
        self.open_add_teacher_callback = open_add_teacher_callback
        self.open_view_teacher_callback = open_view_teacher_callback
        self.open_edit_teacher_callback = open_edit_teacher_callback

        # Responsive Layout Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_main_content()
        self.load_teachers()

    def create_main_content(self):
        """Builds responsive layout area panel structures for main content."""
        # Top Action Bar Layout Container
        action_bar = ctk.CTkFrame(self, fg_color="transparent")
        action_bar.grid(row=0, column=0, padx=30, pady=(25, 15), sticky="ew")
        action_bar.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(action_bar, placeholder_text="Search Teacher...", width=300, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, text_color=self.TEXT_DARK)
        self.search_entry.grid(row=0, column=0, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        self.add_btn = ctk.CTkButton(action_bar, text="+ Add Teacher", font=ctk.CTkFont(size=14, weight="bold"), fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE, height=40, corner_radius=6)
        self.add_btn.grid(row=0, column=1, sticky="e")
        if self.open_add_teacher_callback:
            self.add_btn.configure(command=self.open_add_teacher_callback)

        # Central Layout Data Matrix Display Segment
        self.table_container = ctk.CTkFrame(self, fg_color=self.WHITE, corner_radius=8)
        self.table_container.grid(row=1, column=0, padx=30, pady=(0, 30), sticky="nsew")
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(1, weight=1)

        # Matrix Headers Configuration
        # NOTE: Actions column width reduced from 160 -> 110 since Edit button was removed.
        headers = ["Teacher ID", "Teacher Name", "Department", "Phone", "Email", "Experience", "Status", "Actions"]
        columns_width = [100, 150, 140, 110, 160, 100, 100, 110]

        self.header_frame = ctk.CTkFrame(self.table_container, fg_color=self.PANEL_BG, height=45, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_propagate(False)

        for idx, header in enumerate(headers):
            self.header_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])
            lbl = ctk.CTkLabel(self.header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            lbl.grid(row=0, column=idx, padx=15, pady=10, sticky="ew")

        # Scrollable Frame Construction Injection
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        for idx in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(idx, weight=1, minsize=columns_width[idx])

    def load_teachers(self):
        """Load all teachers from the database and populate the table."""
        teachers = get_all_teachers()
        self.populate_table_data(teachers)

    def on_search_change(self, event):
        """Handle search box input and filter teachers accordingly."""
        search_term = self.search_entry.get()
        teachers = search_teachers(search_term)
        self.populate_table_data(teachers)

    def populate_table_data(self, teachers):
        """Renders teacher data iteratively, clearing existing widgets first."""
        # Clear existing widgets to prevent duplicates
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for row_idx, teacher in enumerate(teachers):

            id_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["teacher_id"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            id_lbl.grid(row=row_idx, column=0, padx=15, pady=12, sticky="ew")

            name_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["teacher_name"], font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT_DARK, anchor="w")
            name_lbl.grid(row=row_idx, column=1, padx=15, pady=12, sticky="ew")

            dept_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["department"], font=ctk.CTkFont(size=13), text_color=self.TEXT_DARK, anchor="w")
            dept_lbl.grid(row=row_idx, column=2, padx=15, pady=12, sticky="ew")

            phone_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["phone"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            phone_lbl.grid(row=row_idx, column=3, padx=15, pady=12, sticky="ew")

            email_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["email"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            email_lbl.grid(row=row_idx, column=4, padx=15, pady=12, sticky="ew")

            exp_lbl = ctk.CTkLabel(self.scroll_frame, text=teacher["experience"], font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY, anchor="w")
            exp_lbl.grid(row=row_idx, column=5, padx=15, pady=12, sticky="ew")

            # Status pill design geometry badge injection
            status_text = teacher["status"]
            badge_color = self.SUCCESS_GREEN if status_text == "Active" else self.DANGER_RED

            status_badge = ctk.CTkFrame(self.scroll_frame, fg_color=badge_color, corner_radius=12, width=75, height=24)
            status_badge.grid(row=row_idx, column=6, padx=15, pady=12, sticky="w")
            status_badge.grid_propagate(False)

            status_lbl = ctk.CTkLabel(status_badge, text=status_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=self.WHITE)
            status_lbl.place(relx=0.5, rely=0.5, anchor="center")

            # Action Frame Layout Container Row Grid Integration
            # Edit button removed - only View and Delete remain.
            action_panel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            action_panel.grid(row=row_idx, column=7, padx=15, pady=12, sticky="ew")

            view_btn = ctk.CTkButton(action_panel, text="View", font=ctk.CTkFont(size=11), fg_color=self.PANEL_BG, hover_color="#E0E7FF", text_color=self.PRIMARY_BLUE, width=42, height=24, corner_radius=4)
            view_btn.grid(row=0, column=0, padx=2)
            if self.open_view_teacher_callback:
                view_btn.configure(command=lambda t=teacher: self.open_view_teacher_callback(t))

            delete_btn = ctk.CTkButton(action_panel, text="Delete", font=ctk.CTkFont(size=11), fg_color="#FEE2E2", hover_color="#FCA5A5", text_color=self.DANGER_RED, width=46, height=24, corner_radius=4)
            delete_btn.grid(row=0, column=1, padx=2)
            delete_btn.configure(command=lambda t=teacher: self.delete_teacher_handler(t))

    def delete_teacher_handler(self, teacher):
        """Handle teacher deletion with a CTkMessagebox confirmation dialog."""
        confirm_box = CTkMessagebox(
            title="Delete Teacher",
            message=(
                "Are you sure you want to delete this teacher?\n\n"
                f"Teacher ID: {teacher['teacher_id']}\n"
                f"Teacher Name: {teacher['teacher_name']}"
            ),
            icon="warning",
            option_1="No",
            option_2="Yes",
        )

        response = confirm_box.get()

        if response == "Yes":
            try:
                result = delete_teacher(teacher["teacher_id"])
                # Treat an explicit False return as failure; None/True/other truthy as success.
                if result is False:
                    raise Exception("Delete operation returned failure.")

                CTkMessagebox(
                    title="Success",
                    message="Teacher deleted successfully.",
                    icon="check",
                    option_1="OK",
                )
                self.load_teachers()
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Failed to delete teacher.\n{e}",
                    icon="cancel",
                    option_1="OK",
                )
        # If "No", simply do nothing - dialog is already closed.


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x700")
    page = TeachersPage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()