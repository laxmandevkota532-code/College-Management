import customtkinter as ctk
from tkinter import Canvas
import tkinter as tk


class ViewStudentPage(ctk.CTkFrame):
    """
    View Student Page - Displays student information in read-only format.
    
    Features:
    - Header with back button
    - Main content area with student details
    - Right panel with profile summary
    - Bottom action buttons
    """
    
    # Design Constants
    PRIMARY_BLUE = "#4F5BD5"
    HOVER_BLUE = "#3F4ACB"
    BACKGROUND = "#F8F9FC"
    WHITE = "#FFFFFF"
    TEXT_DARK = "#111827"
    TEXT_GRAY = "#6B7280"
    BORDER = "#E5E7EB"
    
    # Dummy student data
    DUMMY_STUDENT = {
        "id": "STU001",
        "name": "Rajesh Kumar",
        "gender": "Male",
        "dob": "2003-05-15",
        "course": "Computer Science",
        "phone": "+977-9841234567",
        "email": "rajesh.kumar@example.com",
        "address": "Kathmandu, Nepal",
        "status": "Active",
        "admission_date": "2023-08-01"
    }
    
    def __init__(self, master, student_data=None, back_callback=None):
        super().__init__(master, fg_color=self.BACKGROUND)
        
        self.student_data = student_data or self.DUMMY_STUDENT
        self.back_callback = back_callback
        
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        self.grid_columnconfigure(0, weight=1)
        
        self._create_header()
        self._create_main_content()
        self._create_bottom_buttons()
    
    def _create_header(self):
        """Create top header with back button and title."""
        header_frame = ctk.CTkFrame(self, fg_color=self.WHITE, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back",
            text_color=self.PRIMARY_BLUE,
            fg_color="transparent",
            hover_color=self.BACKGROUND,
            font=ctk.CTkFont("Segoe UI", 13, "bold"),
            cursor="hand2",
            command=self.go_back
        )
        back_btn.grid(row=0, column=0, sticky="w", padx=24, pady=16)
        
        # Title and subtitle container
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.grid(row=0, column=1, sticky="w", padx=24, pady=16)
        
        title_label = ctk.CTkLabel(
            title_container,
            text="View Student",
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 28, "bold")
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Student information",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 12)
        )
        subtitle_label.pack(anchor="w", pady=(4, 0))
        
        # Border line
        border_frame = ctk.CTkFrame(header_frame, fg_color=self.BORDER, height=1)
        border_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
    
    def _create_main_content(self):
        """Create main content area with student details and profile card."""
        content_frame = ctk.CTkFrame(self, fg_color=self.BACKGROUND)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=24, pady=24)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=0)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Student details card
        self._create_student_details_card(content_frame)
        
        # Right side - Profile summary card
        self._create_profile_summary_card(content_frame)
    
    def _create_student_details_card(self, parent):
        """Create large white card with student details."""
        details_card = ctk.CTkFrame(
            parent,
            fg_color=self.WHITE,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER
        )
        details_card.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        details_card.grid_columnconfigure(0, weight=1)
        
        # Scrollable container for details
        scrollable_frame = ctk.CTkScrollableFrame(
            details_card,
            fg_color=self.WHITE,
            corner_radius=12
        )
        scrollable_frame.pack(fill="both", expand=True, padx=24, pady=24)
        scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Field data
        fields = [
            ("Student ID", self.student_data.get("id", "N/A")),
            ("Full Name", self.student_data.get("name", "N/A")),
            ("Gender", self.student_data.get("gender", "N/A")),
            ("Date of Birth", self.student_data.get("dob", "N/A")),
            ("Course", self.student_data.get("course", "N/A")),
            ("Phone Number", self.student_data.get("phone", "N/A")),
            ("Email Address", self.student_data.get("email", "N/A")),
            ("Address", self.student_data.get("address", "N/A")),
            ("Status", self.student_data.get("status", "N/A")),
            ("Admission Date", self.student_data.get("admission_date", "N/A")),
        ]
        
        for idx, (label_text, value) in enumerate(fields):
            # Label
            label = ctk.CTkLabel(
                scrollable_frame,
                text=label_text,
                text_color=self.TEXT_GRAY,
                font=ctk.CTkFont("Segoe UI", 11, "bold")
            )
            label.grid(row=idx, column=0, sticky="w", pady=(12, 4))
            
            # Value (read-only display)
            value_frame = ctk.CTkFrame(
                scrollable_frame,
                fg_color=self.BACKGROUND,
                corner_radius=8,
                border_width=1,
                border_color=self.BORDER
            )
            value_frame.grid(row=idx, column=0, sticky="ew", pady=(0, 16))
            value_frame.grid_columnconfigure(0, weight=1)
            
            value_label = ctk.CTkLabel(
                value_frame,
                text=str(value),
                text_color=self.TEXT_DARK,
                font=ctk.CTkFont("Segoe UI", 12),
                wraplength=300
            )
            value_label.pack(anchor="w", padx=12, pady=10)
    
    def _create_profile_summary_card(self, parent):
        """Create right side profile summary card."""
        profile_card = ctk.CTkFrame(
            parent,
            fg_color=self.WHITE,
            corner_radius=12,
            border_width=1,
            border_color=self.BORDER,
            width=240
        )
        profile_card.grid(row=0, column=1, sticky="n")
        profile_card.grid_propagate(False)
        profile_card.grid_columnconfigure(0, weight=1)
        
        # Avatar placeholder
        avatar_frame = ctk.CTkFrame(
            profile_card,
            fg_color=self.PRIMARY_BLUE,
            corner_radius=12,
            width=160,
            height=160
        )
        avatar_frame.pack(padx=16, pady=16)
        avatar_frame.grid_propagate(False)
        
        # Avatar placeholder text
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="📷",
            text_color=self.WHITE,
            font=ctk.CTkFont("Segoe UI", 48)
        )
        avatar_label.pack(expand=True)
        
        # Student name
        name_label = ctk.CTkLabel(
            profile_card,
            text=self.student_data.get("name", "Student Name"),
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            wraplength=200
        )
        name_label.pack(padx=16, pady=(0, 4))
        
        # Student ID
        id_label = ctk.CTkLabel(
            profile_card,
            text=f"ID: {self.student_data.get('id', 'N/A')}",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 10)
        )
        id_label.pack(padx=16, pady=(0, 12))
        
        # Divider
        divider = ctk.CTkFrame(profile_card, fg_color=self.BORDER, height=1)
        divider.pack(fill="x", padx=16, pady=(0, 12))
        
        # Course section
        course_label = ctk.CTkLabel(
            profile_card,
            text="Course",
            text_color=self.TEXT_GRAY,
            font=ctk.CTkFont("Segoe UI", 10, "bold")
        )
        course_label.pack(anchor="w", padx=16, pady=(0, 4))
        
        course_value = ctk.CTkLabel(
            profile_card,
            text=self.student_data.get("course", "N/A"),
            text_color=self.TEXT_DARK,
            font=ctk.CTkFont("Segoe UI", 11),
            wraplength=200
        )
        course_value.pack(anchor="w", padx=16, pady=(0, 16))
        
        # Status badge
        status = self.student_data.get("status", "Active")
        status_color = self.PRIMARY_BLUE if status == "Active" else "#EF4444"
        
        status_frame = ctk.CTkFrame(
            profile_card,
            fg_color=status_color,
            corner_radius=6
        )
        status_frame.pack(padx=16, pady=(0, 16), fill="x")
        
        status_label = ctk.CTkLabel(
            status_frame,
            text=f"Status: {status}",
            text_color=self.WHITE,
            font=ctk.CTkFont("Segoe UI", 10, "bold")
        )
        status_label.pack(padx=12, pady=8)
    
    def _create_bottom_buttons(self):
        """Create bottom action buttons."""
        button_frame = ctk.CTkFrame(self, fg_color=self.BACKGROUND)
        button_frame.grid(row=2, column=0, sticky="ew", padx=24, pady=24)
        
        # Back button
        back_btn = ctk.CTkButton(
            button_frame,
            text="Back",
            text_color=self.TEXT_DARK,
            fg_color=self.BORDER,
            hover_color="#D1D5DB",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            corner_radius=8,
            cursor="hand2",
            command=self.go_back
        )
        back_btn.pack(side="left")
    
    def go_back(self):
        """Navigate back to Student Management page."""
        if self.back_callback:
            self.back_callback()


if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.geometry("1200x700")
    root.title("View Student Page")
    
    # Dummy student data for testing
    test_student = {
        "id": "STU001",
        "name": "Aarav Sharma",
        "gender": "Male",
        "dob": "2003-05-15",
        "course": "CSIT",
        "phone": "9801234567",
        "email": "aarav.sharma@email.com",
        "address": "Kathmandu, Nepal",
        "status": "Active",
        "admission_date": "2023-08-01"
    }
    
    # Back callback function
    def go_back():
        print("Back to Student Management")
        root.quit()
    
    # Create and pack the page
    view_page = ViewStudentPage(root, student_data=test_student, back_callback=go_back)
    view_page.pack(fill="both", expand=True)
    
    root.mainloop()