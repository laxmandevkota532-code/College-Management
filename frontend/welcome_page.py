import customtkinter as ctk


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class WelcomePage(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.after(100, lambda: self.state("zoomed"))
        self.configure(fg_color="#F8F9FC")

        # Main Container
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#F8F9FC",
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)

        self.create_top_bar()
        self.create_content()

    # -----------------------------
    # Top Bar
    # -----------------------------
    def create_top_bar(self):

        top_bar = ctk.CTkFrame(
            self.main_frame,
            height=70,
            fg_color="#4F5BD5",
            corner_radius=0
        )
        top_bar.pack(fill="x")

        top_bar_label = ctk.CTkLabel(
            top_bar,
            text="College Management System",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        top_bar_label.pack(side="left", padx=30, pady=0)

    # -----------------------------
    # Main Content
    # -----------------------------
    def create_content(self):

        content = ctk.CTkFrame(
            self.main_frame,
            fg_color="#F8F9FC"
        )
        content.pack(fill="both", expand=True, padx=40, pady=30)

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)

        # LEFT SECTION
        left_frame = ctk.CTkFrame(
            content,
            fg_color="#F8F9FC"
        )
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 20))

        # Logo
        logo_label = ctk.CTkLabel(
            left_frame,
            text="🎓 College Management System",
            font=("Segoe UI", 28, "bold"),
            text_color="#111827"
        )
        logo_label.pack(anchor="w", pady=(40, 60))

        # Welcome Title
        title = ctk.CTkLabel(
            left_frame,
            text="Welcome to\nCollege Management",
            font=("Segoe UI", 72, "bold"),
            text_color="#111827",
            justify="left"
        )
        title.pack(anchor="w")

        # Description
        desc = ctk.CTkLabel(
            left_frame,
            text="Manage students, faculty, academic programs,\n"
                 "and campus records through one modern platform.",
            font=("Segoe UI", 24),
            justify="left",
            text_color="#6B7280"
        )
        desc.pack(anchor="w", pady=(25, 50))

        # Get Started Button
        get_started_btn = ctk.CTkButton(
            left_frame,
            text="Get Started",
            width=260,
            height=65,
            corner_radius=15,
            fg_color="#4F5BD5",
            hover_color="#3F4ACB",
            font=("Segoe UI", 22, "bold"),
            command=self.open_login
        )
        get_started_btn.pack(anchor="w")

        # RIGHT SECTION
        right_frame = ctk.CTkFrame(
            content,
            fg_color="#EEF2FF",
            corner_radius=30
        )
        right_frame.grid(row=0, column=1, sticky="nsew")

        preview_title = ctk.CTkLabel(
            right_frame,
            text="Dashboard Preview",
            font=("Segoe UI", 30, "bold"),
            text_color="#111827"
        )
        preview_title.pack(pady=(40, 20))

        # Statistics Area
        stats_frame = ctk.CTkFrame(
            right_frame,
            fg_color="transparent"
        )
        stats_frame.pack(fill="x", padx=30)

        stats_frame.grid_columnconfigure((0, 1), weight=1)

        self.create_stat_card(
            stats_frame,
            "1250",
            "Enrolled Students",
            0,
            0
        )

        self.create_stat_card(
            stats_frame,
            "24",
            "Academic Programs",
            0,
            1
        )

        self.create_stat_card(
            stats_frame,
            "45",
            "Faculty Members",
            1,
            0
        )

        self.create_stat_card(
            stats_frame,
            "92%",
            "Attendance Rate",
            1,
            1
        )

    # -----------------------------
    # Stat Card
    # -----------------------------
    def create_stat_card(self, parent, value, title, row, col):

        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=20,
            height=120
        )

        card.grid(
            row=row,
            column=col,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color="#4F5BD5"
        )
        value_label.pack(pady=(25, 5))

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16),
            text_color="#6B7280"
        )
        title_label.pack()

    def open_login(self):
        print("Open Login Page")
        from frontend.login import LoginPage
        self.destroy()
        root = ctk.CTk()
        LoginPage(root)
        root.mainloop()


if __name__ == "__main__":
    app = WelcomePage()
    app.mainloop()