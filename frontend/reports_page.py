import customtkinter as ctk
from typing import List, Dict
from functools import partial

# Import from your existing backend (no mocks)
from backend.report_crud import (
    get_dashboard_statistics,
    get_student_reports,
    get_teacher_reports,
    get_course_reports,
    get_attendance_reports,
    prepare_student_export,
    prepare_teacher_export,
    prepare_course_export,
    prepare_attendance_export
)

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class ReportsPage(ctk.CTkFrame):
    
    PRIMARY_BLUE = "#4F5BD5"
    HOVER_BLUE = "#3F4ACB"
    BACKGROUND = "#F8F9FC"
    PANEL_BG = "#EEF2FF"
    TEXT_DARK = "#111827"
    TEXT_GRAY = "#6B7280"
    WHITE = "#FFFFFF"
    SUCCESS_GREEN = "#10B981"
    DANGER_RED = "#EF4444"
    WARNING_YELLOW = "#F59E0B"
    
    REPORT_TYPES = ["Student Report", "Teacher Report", "Course Report", "Attendance Report"]
    
    def __init__(self, master):
        super().__init__(master, fg_color=self.BACKGROUND)
        
        self.current_report_type = None
        self.current_report_data = []
        self.summary_labels = {}
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        self._create_main_content()
        self._load_dashboard()
            
    # ========== UI LAYOUT (UNCHANGED) ==========
    
    def _create_main_content(self):
        self._create_top_bar()
        self._create_summary_cards()
        self._create_action_bar()
        self._create_table_container()
        
    def _create_top_bar(self):
        top_bar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=self.WHITE)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_propagate(False)
        
        ctk.CTkLabel(top_bar, text="Reports Management", font=ctk.CTkFont(size=20, weight="bold"), 
                     text_color=self.TEXT_DARK).grid(row=0, column=0, padx=30, pady=20, sticky="w")
        ctk.CTkLabel(top_bar, text="Admin User", font=ctk.CTkFont(size=14), 
                     text_color=self.TEXT_GRAY).grid(row=0, column=1, padx=30, pady=20, sticky="e")
                     
    def _create_summary_cards(self):
        metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        metrics_frame.grid(row=1, column=0, padx=30, pady=(25, 10), sticky="ew")
        
        cards = [
            ("Total Students", "total_students"), 
            ("Total Courses", "total_courses"),
            ("Total Teachers", "total_teachers"), 
            ("Attendance Rate", "attendance_rate")
        ]
                 
        for col_idx, (title, key) in enumerate(cards):
            metrics_frame.grid_columnconfigure(col_idx, weight=1, uniform="metrics")
            
            box = ctk.CTkFrame(metrics_frame, fg_color=self.WHITE, height=90, corner_radius=8)
            box.grid(row=0, column=col_idx, padx=(0 if col_idx == 0 else 10, 0 if col_idx == 3 else 10), sticky="ew")
            box.grid_propagate(False)
            
            ctk.CTkLabel(box, text=title, font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY)\
                .grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")
                
            val_lbl = ctk.CTkLabel(box, text="--", font=ctk.CTkFont(size=22, weight="bold"), text_color=self.TEXT_DARK)
            val_lbl.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
            self.summary_labels[key] = val_lbl

    def _create_action_bar(self):
        action_bar = ctk.CTkFrame(self, fg_color="transparent")
        action_bar.grid(row=2, column=0, padx=30, pady=(15, 15), sticky="ew")
        action_bar.grid_columnconfigure(1, weight=1)
        
        self.report_type_var = ctk.StringVar(value=self.REPORT_TYPES[0])
        ctk.CTkComboBox(action_bar, values=self.REPORT_TYPES, variable=self.report_type_var, 
                        width=160, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG, 
                        button_color=self.PRIMARY_BLUE, state="readonly").grid(row=0, column=0, sticky="w")
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._on_search())
        ctk.CTkEntry(action_bar, placeholder_text="Search...", width=200, height=40, fg_color=self.WHITE, 
                     border_color=self.PANEL_BG, textvariable=self.search_var)\
                     .grid(row=0, column=1, padx=10, sticky="w")
                     
        btn_frame = ctk.CTkFrame(action_bar, fg_color="transparent")
        btn_frame.grid(row=0, column=2, sticky="e")
        
        ctk.CTkButton(btn_frame, text="Generate", fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, 
                      height=40, command=self._generate_report).grid(row=0, column=0, padx=(0, 8))
                      
        self.btn_export_pdf = ctk.CTkButton(btn_frame, text="Export PDF", fg_color="#F3F4F6", text_color=self.TEXT_DARK, 
                                            hover_color="#E5E7EB", height=40, state="disabled", 
                                            command=partial(self._export, "pdf"))
        self.btn_export_pdf.grid(row=0, column=1, padx=(0, 8))
        
        self.btn_export_excel = ctk.CTkButton(btn_frame, text="Export Excel", fg_color="#F3F4F6", text_color=self.TEXT_DARK, 
                                              hover_color="#E5E7EB", height=40, state="disabled", 
                                              command=partial(self._export, "excel"))
        self.btn_export_excel.grid(row=0, column=2)

    def _create_table_container(self):
        table_container = ctk.CTkFrame(self, fg_color=self.WHITE, corner_radius=8)
        table_container.grid(row=3, column=0, padx=30, pady=(0, 30), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)
        
        self.header_frame = ctk.CTkFrame(table_container, fg_color=self.PANEL_BG, height=45, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_propagate(False)
        
        self.scroll_frame = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

    # ========== BACKEND INTEGRATION ==========

    def _load_dashboard(self):
        try:
            stats = get_dashboard_statistics()
            for key, val in stats.items():
                if key in self.summary_labels:
                    self.summary_labels[key].configure(text=str(val))
        except Exception as e:
            print(f"Dashboard Error: {e}")

    def _generate_report(self):
        self.current_report_type = self.report_type_var.get()
        try:
            if self.current_report_type == "Student Report":
                self.current_report_data = get_student_reports()
            elif self.current_report_type == "Teacher Report":
                self.current_report_data = get_teacher_reports()
            elif self.current_report_type == "Course Report":
                self.current_report_data = get_course_reports()
            elif self.current_report_type == "Attendance Report":
                self.current_report_data = get_attendance_reports()
                
            self._populate_table(self.current_report_data)
            
            self.btn_export_pdf.configure(state="normal")
            self.btn_export_excel.configure(state="normal")
        except Exception as e:
            print(f"Generation Error: {e}")

    def _on_search(self):
        search_term = self.search_var.get().strip().lower()
        if not search_term or not self.current_report_data:
            self._populate_table(self.current_report_data)
            return
            
        results = [
            record for record in self.current_report_data 
            if any(search_term in str(val).lower() for val in record.values())
        ]
        self._populate_table(results)

    def _get_table_configuration(self):
        if self.current_report_type == "Student Report":
            return ["ID", "Name", "Course", "Status", "Actions"], ["id", "name", "course", "status"]
        elif self.current_report_type == "Teacher Report":
            return ["ID", "Name", "Department", "Status", "Actions"], ["id", "name", "department", "status"]
        elif self.current_report_type == "Course Report":
            return ["Course", "Instructor", "Students", "Status", "Actions"], ["name", "instructor", "students", "status"]
        elif self.current_report_type == "Attendance Report":
            return ["Student", "Date", "Course", "Status", "Actions"], ["student", "date", "course", "status"]
        return [], []

    # ========== TABLE RENDERING ==========

    def _populate_table(self, data: List[Dict]):
        for widget in self.header_frame.winfo_children() + self.scroll_frame.winfo_children():
            widget.destroy()
            
        if not data or not self.current_report_type:
            empty_lbl = ctk.CTkLabel(self.scroll_frame, text="No records available to display.", 
                                     font=ctk.CTkFont(size=14, slant="italic"), text_color=self.TEXT_GRAY)
            empty_lbl.pack(pady=60)
            return
            
        headers, data_keys = self._get_table_configuration()
        
        self.header_frame.grid_columnconfigure(list(range(len(headers))), weight=1, uniform="header")
        self.scroll_frame.grid_columnconfigure(list(range(len(headers))), weight=1, uniform="col")
        
        for idx, header in enumerate(headers):
            ctk.CTkLabel(self.header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), 
                         text_color=self.TEXT_DARK).grid(row=0, column=idx, padx=20, pady=10, sticky="w")
                         
        for row_idx, record in enumerate(data):
            for col_idx, key in enumerate(data_keys):
                val = str(record.get(key, "N/A"))
                
                if key == "status":
                    self._create_status_badge(row_idx, col_idx, val)
                else:
                    is_main_col = (col_idx == 1 or (self.current_report_type == "Course Report" and col_idx == 0))
                    font_weight = "bold" if is_main_col else "normal"
                    text_color = self.TEXT_DARK if is_main_col else self.TEXT_GRAY
                    
                    ctk.CTkLabel(self.scroll_frame, text=val, font=ctk.CTkFont(size=13, weight=font_weight), 
                                 text_color=text_color).grid(row=row_idx, column=col_idx, padx=20, pady=12, sticky="w")
                                 
            btn_view = ctk.CTkButton(self.scroll_frame, text="View", width=60, height=26, fg_color=self.PANEL_BG, 
                                     text_color=self.PRIMARY_BLUE, hover_color="#E0E7FF", 
                                     command=partial(self._show_view_dialog, record))
            btn_view.grid(row=row_idx, column=len(data_keys), padx=20, pady=12, sticky="w")

    def _create_status_badge(self, row_idx, col_idx, status):
        status_lower = status.lower()
        if status_lower in ["active", "present", "completed"]:
            bg = self.SUCCESS_GREEN
        elif status_lower in ["inactive"]:
            bg = self.TEXT_GRAY
        elif status_lower in ["absent"]:
            bg = self.DANGER_RED
        elif status_lower in ["late", "pending"]:
            bg = self.WARNING_YELLOW
        else:
            bg = self.PANEL_BG
            
        badge = ctk.CTkFrame(self.scroll_frame, fg_color=bg, corner_radius=12, width=80, height=26)
        badge.grid(row=row_idx, column=col_idx, padx=20, pady=12, sticky="w")
        badge.grid_propagate(False)
        
        ctk.CTkLabel(badge, text=status, font=ctk.CTkFont(size=11, weight="bold"), text_color=self.WHITE)\
            .place(relx=0.5, rely=0.5, anchor="center")

    # ========== EXPORT & DIALOGS ==========

    def _export(self, fmt: str):
        if not self.current_report_data:
            return
        try:
            if self.current_report_type == "Student Report":
                prepare_student_export(self.current_report_data, format=fmt)
            elif self.current_report_type == "Teacher Report":
                prepare_teacher_export(self.current_report_data, format=fmt)
            elif self.current_report_type == "Course Report":
                prepare_course_export(self.current_report_data, format=fmt)
            elif self.current_report_type == "Attendance Report":
                prepare_attendance_export(self.current_report_data, format=fmt)
                
            self._show_message_dialog("Success", f"Report exported as {fmt.upper()} successfully.", self.SUCCESS_GREEN)
        except Exception as e:
            self._show_message_dialog("Export Error", f"Failed to export.\n{e}", self.DANGER_RED)

    def _show_message_dialog(self, title: str, message: str, color: str):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.resizable(False, False)
        
        ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=13), text_color=color).pack(padx=20, pady=(30, 20))
        ctk.CTkButton(dialog, text="OK", fg_color=self.PRIMARY_BLUE, text_color=self.WHITE, width=100, 
                      command=dialog.destroy).pack(pady=(0, 20))
        
        self._center_modal(dialog, 350, 150)

    def _show_view_dialog(self, record: Dict):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Report Details")
        dialog.resizable(False, False)
        
        frame = ctk.CTkScrollableFrame(dialog, fg_color=self.BACKGROUND, width=400, height=250)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame.grid_columnconfigure(1, weight=1)
        
        for row_idx, (key, val) in enumerate(record.items()):
            formatted_key = f"{key.replace('_', ' ').title()}:"
            ctk.CTkLabel(frame, text=formatted_key, font=ctk.CTkFont(weight="bold", size=13), text_color=self.TEXT_DARK)\
                .grid(row=row_idx, column=0, sticky="e", padx=(10, 15), pady=8)
                
            ctk.CTkLabel(frame, text=str(val), font=ctk.CTkFont(size=13), text_color=self.TEXT_GRAY)\
                .grid(row=row_idx, column=1, sticky="w", padx=(0, 10), pady=8)
                
        ctk.CTkButton(dialog, text="Close", fg_color=self.PRIMARY_BLUE, text_color=self.WHITE, width=120, 
                      command=dialog.destroy).pack(pady=(0, 15))
                      
        self._center_modal(dialog, 450, 350)

    def _center_modal(self, dialog, width, height):
        dialog.geometry(f"{width}x{height}")
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (width // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()