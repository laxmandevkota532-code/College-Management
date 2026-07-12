import customtkinter as ctk
import sqlite3
from datetime import datetime
from CTkMessagebox import CTkMessagebox

from database.database import get_connection
from backend.course_crud import get_all_courses
from backend.attendance_crud import (
    save_attendance,
    attendance_exists,
    update_attendance,
    get_all_attendance,
    get_attendance_by_date,
    get_students_by_course,
    search_attendance,
    delete_attendance,
    get_attendance_summary,
)


class AttendancePage(ctk.CTkFrame):
    """Attendance management page backed by the SQLite attendance table."""

    STATUS_OPTIONS = ["Present", "Absent", "Late"]

    STATUS_COLORS = {
        "Present": {"bg": "#DCFCE7", "txt": "#15803D"},
        "Absent": {"bg": "#FEE2E2", "txt": "#B91C1C"},
        "Late": {"bg": "#FEF3C7", "txt": "#B45309"},
    }

    def __init__(self, master):
        super().__init__(master, fg_color="#F8F9FC")

        # Configure page grid layout as required
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Column widths shared between header and table rows
        self.column_widths = [120, 200, 220, 120, 120, 100]

        self.create_header()
        self.create_summary_cards()
        self.create_controls()
        self.create_attendance_table()

        self.load_course_options()
        self.refresh_table()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def create_header(self):
        """Builds the page title header."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=30, pady=(30, 20), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Attendance Management",
            font=ctk.CTkFont(family="Arial", size=26, weight="bold"),
            text_color="#1E293B"
        )
        title.grid(row=0, column=0, sticky="w")

    def create_summary_cards(self):
        """Builds the summary metric cards. Value labels are stored for later refreshing."""
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        metrics = [
            {"key": "total", "title": "Total Records", "color": "#4F46E5"},
            {"key": "present", "title": "Present", "color": "#10B981"},
            {"key": "absent", "title": "Absent", "color": "#EF4444"},
            {"key": "late", "title": "Late", "color": "#F59E0B"}
        ]

        self.summary_value_labels = {}

        for idx, metric in enumerate(metrics):
            card = ctk.CTkFrame(cards_frame, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#E2E8F0")
            card.grid(row=0, column=idx, padx=(0 if idx == 0 else 10, 0 if idx == 3 else 10), sticky="nsew")
            card.grid_columnconfigure(0, weight=1)

            lbl_title = ctk.CTkLabel(card, text=metric["title"], font=ctk.CTkFont(family="Arial", size=13), text_color="#64748B")
            lbl_title.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

            lbl_val = ctk.CTkLabel(card, text="0", font=ctk.CTkFont(family="Arial", size=22, weight="bold"), text_color=metric["color"])
            lbl_val.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")

            self.summary_value_labels[metric["key"]] = lbl_val

    def create_controls(self):
        """Builds the search bar, course dropdown, date field, and mark attendance button."""
        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=2, column=0, padx=30, pady=20, sticky="ew")
        controls_frame.grid_columnconfigure(0, weight=1)

        self.search_bar = ctk.CTkEntry(
            controls_frame,
            placeholder_text="Search student by name or ID...",
            width=300,
            height=38,
            fg_color="#FFFFFF",
            border_color="#CBD5E1",
            text_color="#1E293B"
        )
        self.search_bar.grid(row=0, column=0, sticky="w")
        self.search_bar.bind("<KeyRelease>", lambda event: self.refresh_table())

        right_controls = ctk.CTkFrame(controls_frame, fg_color="transparent")
        right_controls.grid(row=0, column=1, sticky="e")

        self.course_dropdown = ctk.CTkComboBox(
            right_controls,
            values=["All Courses"],
            width=180,
            height=38,
            fg_color="#FFFFFF",
            border_color="#CBD5E1",
            text_color="#1E293B",
            command=lambda choice: self.refresh_table()
        )
        self.course_dropdown.set("All Courses")
        self.course_dropdown.grid(row=0, column=0, padx=10)

        self.date_field = ctk.CTkEntry(
            right_controls,
            width=120,
            height=38,
            fg_color="#FFFFFF",
            border_color="#CBD5E1",
            text_color="#1E293B"
        )
        self.date_field.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.date_field.grid(row=0, column=1, padx=10)
        self.date_field.bind("<KeyRelease>", lambda event: self.refresh_table())

        self.mark_attendance_btn = ctk.CTkButton(
            right_controls,
            text="Mark Attendance",
            height=38,
            fg_color="#4F46E5",
            hover_color="#4338CA",
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
            command=self.open_mark_attendance_dialog
        )
        self.mark_attendance_btn.grid(row=0, column=2, padx=(10, 0))

    def create_attendance_table(self):
        """Builds the table container, header row, and scrollable body."""
        table_container = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#E2E8F0")
        table_container.grid(row=3, column=0, padx=30, pady=(0, 30), sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(1, weight=1)

        headers_frame = ctk.CTkFrame(table_container, fg_color="#F1F5F9", height=40, corner_radius=0)
        headers_frame.grid(row=0, column=0, sticky="ew")
        headers_frame.grid_propagate(False)

        headers = ["Student ID", "Name", "Course", "Date", "Status", "Actions"]

        for idx, header in enumerate(headers):
            lbl = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
                text_color="#475569"
            )
            lbl.grid(row=0, column=idx, padx=15, pady=8, sticky="w")

        for idx, width in enumerate(self.column_widths):
            headers_frame.grid_columnconfigure(idx, minsize=width)

        self.scrollable_table = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        self.scrollable_table.grid(row=1, column=0, sticky="nsew")

        for idx, width in enumerate(self.column_widths):
            self.scrollable_table.grid_columnconfigure(idx, minsize=width)

    # ------------------------------------------------------------------
    # Course dropdown
    # ------------------------------------------------------------------

    def load_course_options(self):
        """Load course names dynamically from the Course table and populate the dropdown."""
        try:
            courses = get_all_courses()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to load courses.\n{e}", icon="cancel")
            courses = []

        course_names = self._extract_course_names(courses)
        values = ["All Courses"] + course_names

        self.course_dropdown.configure(values=values)
        self.course_dropdown.set("All Courses")

    @staticmethod
    def _extract_course_names(courses):
        """Extract a clean list of course names from course_crud records.

        Supports differing column naming between projects by checking a
        small set of likely keys.

        Args:
            courses: A list of course dictionaries returned by get_all_courses().

        Returns:
            A list of course name strings.
        """
        possible_keys = ["course_name", "course", "name", "title"]
        names = []

        for course in courses:
            value = None
            for key in possible_keys:
                if key in course and course[key]:
                    value = course[key]
                    break
            if value:
                names.append(value)

        return names

    # ------------------------------------------------------------------
    # Filtering and refreshing
    # ------------------------------------------------------------------

    def refresh_table(self):
        """Reload attendance records using the active filters and refresh the summary cards.

        This is the single entry point that should be called after any
        Save, Update, Delete, Search, Course change, or Date change so the
        table and cards always reflect the current database state.
        """
        records = self.get_filtered_records()
        self.populate_table_data(records)
        self.refresh_summary_cards()

    def get_filtered_records(self):
        """Fetch attendance records applying the search, course, and date filters together.

        Returns:
            A list of attendance record dictionaries matching all active filters.
        """
        keyword = self.search_bar.get().strip()
        course = self.course_dropdown.get().strip()
        date_value = self.date_field.get().strip()

        course_filter = course if course and course != "All Courses" else None
        date_filter = date_value if self._is_valid_date(date_value) else None

        try:
            if keyword:
                records = search_attendance(keyword)
            elif date_filter:
                records = get_attendance_by_date(date_filter)
            else:
                records = get_all_attendance()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to load attendance records.\n{e}", icon="cancel")
            return []

        if course_filter:
            records = [r for r in records if r.get("course") == course_filter]

        # search_attendance() does not filter by date, so re-apply it here
        # whenever both a keyword and a date filter are active together.
        if date_filter and keyword:
            records = [r for r in records if r.get("attendance_date") == date_filter]

        return records

    def refresh_summary_cards(self):
        """Refresh the summary cards with database-calculated attendance counts."""
        try:
            summary = get_attendance_summary()
            all_records = get_all_attendance()
            late_count = sum(1 for r in all_records if r.get("status") == "Late")

            self.summary_value_labels["total"].configure(text=str(summary.get("total", 0)))
            self.summary_value_labels["present"].configure(text=str(summary.get("present", 0)))
            self.summary_value_labels["absent"].configure(text=str(summary.get("absent", 0)))
            self.summary_value_labels["late"].configure(text=str(late_count))
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to load attendance summary.\n{e}", icon="cancel")

    # ------------------------------------------------------------------
    # Table rendering
    # ------------------------------------------------------------------

    def populate_table_data(self, records):
        """Render attendance records into the scrollable table, clearing existing rows first.

        Args:
            records: A list of attendance record dictionaries to display.
        """
        for widget in self.scrollable_table.winfo_children():
            widget.destroy()

        for row_idx, record in enumerate(records):
            self._render_row(row_idx, record)

    def _render_row(self, row_idx, record):
        """Render a single attendance record as a table row.

        Args:
            row_idx: The row index used for grid placement and striping.
            record: The attendance record dictionary to display.
        """
        row_bg = "#FFFFFF" if row_idx % 2 == 0 else "#F8FAFC"

        row_frame = ctk.CTkFrame(self.scrollable_table, fg_color=row_bg, corner_radius=0, height=45)
        row_frame.grid(row=row_idx, column=0, columnspan=6, sticky="ew")
        row_frame.grid_propagate(False)

        for idx, width in enumerate(self.column_widths):
            row_frame.grid_columnconfigure(idx, minsize=width)

        ctk.CTkLabel(row_frame, text=record.get("student_id", ""), font=ctk.CTkFont(family="Arial", size=13), text_color="#1E293B").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        ctk.CTkLabel(row_frame, text=record.get("fullname", ""), font=ctk.CTkFont(family="Arial", size=13, weight="bold"), text_color="#1E293B").grid(row=0, column=1, padx=15, pady=10, sticky="w")
        ctk.CTkLabel(row_frame, text=record.get("course", ""), font=ctk.CTkFont(family="Arial", size=13), text_color="#475569").grid(row=0, column=2, padx=15, pady=10, sticky="w")
        ctk.CTkLabel(row_frame, text=record.get("attendance_date", ""), font=ctk.CTkFont(family="Arial", size=13), text_color="#475569").grid(row=0, column=3, padx=15, pady=10, sticky="w")

        status_text = record.get("status", "")
        colors = self.STATUS_COLORS.get(status_text, {"bg": "#E2E8F0", "txt": "#475569"})

        status_badge = ctk.CTkLabel(
            row_frame,
            text=status_text,
            font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
            fg_color=colors["bg"],
            text_color=colors["txt"],
            corner_radius=6,
            width=75,
            height=24
        )
        status_badge.grid(row=0, column=4, padx=15, pady=10, sticky="w")

        action_panel = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_panel.grid(row=0, column=5, padx=15, pady=10, sticky="w")

        edit_btn = ctk.CTkButton(
            action_panel,
            text="Edit",
            width=42,
            height=26,
            fg_color="#F1F5F9",
            hover_color="#E2E8F0",
            text_color="#475569",
            font=ctk.CTkFont(family="Arial", size=12),
            command=lambda r=record: self.edit_attendance_handler(r)
        )
        edit_btn.grid(row=0, column=0, padx=(0, 4))

        delete_btn = ctk.CTkButton(
            action_panel,
            text="Del",
            width=42,
            height=26,
            fg_color="#FEE2E2",
            hover_color="#FCA5A5",
            text_color="#B91C1C",
            font=ctk.CTkFont(family="Arial", size=12),
            command=lambda r=record: self.delete_attendance_handler(r)
        )
        delete_btn.grid(row=0, column=1)

    # ------------------------------------------------------------------
    # Record actions
    # ------------------------------------------------------------------

    def edit_attendance_handler(self, record):
        """Open a small dialog to change the status of an existing attendance record.

        Args:
            record: The attendance record dictionary to edit.
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Attendance Status")
        dialog.geometry("360x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.attributes('-topmost', True)

        info_lbl = ctk.CTkLabel(
            dialog,
            text=f"{record.get('fullname', '')} ({record.get('student_id', '')})\n{record.get('attendance_date', '')}",
            font=ctk.CTkFont(family="Arial", size=13)
        )
        info_lbl.pack(pady=(20, 10))

        status_var = ctk.StringVar(value=record.get("status", "Present"))
        status_dropdown = ctk.CTkComboBox(dialog, values=self.STATUS_OPTIONS, variable=status_var, width=200)
        status_dropdown.pack(pady=10)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        def confirm_edit():
            new_status = status_var.get()

            if not self._is_valid_status(new_status):
                CTkMessagebox(title="Validation Error", message="Please select a valid status.", icon="warning")
                return

            try:
                success = update_attendance({
                    "student_id": record.get("student_id"),
                    "attendance_date": record.get("attendance_date"),
                    "status": new_status
                })
                dialog.destroy()
                if success:
                    CTkMessagebox(title="Success", message="Attendance status updated successfully.", icon="check")
                    self.refresh_table()
                else:
                    CTkMessagebox(title="Error", message="Failed to update attendance status.", icon="cancel")
            except Exception as e:
                dialog.destroy()
                CTkMessagebox(title="Error", message=f"Failed to update attendance status.\n{e}", icon="cancel")

        def cancel_edit():
            dialog.destroy()

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", width=100, fg_color="#F1F5F9", text_color="#475569", hover_color="#E2E8F0", command=cancel_edit)
        cancel_btn.grid(row=0, column=0, padx=10)

        save_btn = ctk.CTkButton(btn_frame, text="Save", width=100, fg_color="#4F46E5", hover_color="#4338CA", command=confirm_edit)
        save_btn.grid(row=0, column=1, padx=10)

    def delete_attendance_handler(self, record):
        """Show a confirmation dialog and delete the attendance record if confirmed.

        Deletes using the numeric primary key when available. Falls back to
        deleting by student_id + attendance_date if no numeric ID exists on
        the record.

        Args:
            record: The attendance record dictionary to delete.
        """
        confirm_box = CTkMessagebox(
            title="Delete Attendance",
            message=(
                "Are you sure you want to delete this attendance record?\n\n"
                f"Student ID: {record.get('student_id', '')}\n"
                f"Name: {record.get('fullname', '')}\n"
                f"Date: {record.get('attendance_date', '')}"
            ),
            icon="warning",
            option_1="No",
            option_2="Yes",
        )

        if confirm_box.get() != "Yes":
            return

        try:
            success = self._delete_record(record)
            if success:
                CTkMessagebox(title="Success", message="Attendance record deleted successfully.", icon="check")
                self.refresh_table()
            else:
                CTkMessagebox(title="Error", message="Failed to delete attendance record.", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to delete attendance record.\n{e}", icon="cancel")

    def _delete_record(self, record):
        """Delete a record by primary key, falling back to student_id + attendance_date.

        Args:
            record: The attendance record dictionary to delete.

        Returns:
            True if a row was deleted, False otherwise.
        """
        record_id = record.get("id")

        if record_id is not None:
            return delete_attendance(record_id)

        student_id = record.get("student_id")
        attendance_date = record.get("attendance_date")

        if not student_id or not attendance_date:
            return False

        query = "DELETE FROM attendance WHERE student_id = ? AND attendance_date = ?"
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (student_id, attendance_date))
            conn.commit()
            deleted = cursor.rowcount > 0
            conn.close()
            return deleted
        except sqlite3.Error:
            return False

    # ------------------------------------------------------------------
    # Mark attendance workflow
    # ------------------------------------------------------------------

    def open_mark_attendance_dialog(self):
        """Open a dialog to mark attendance for every student in the selected course.

        Existing attendance for the selected date is pre-loaded so users can
        review and edit current statuses instead of always starting from
        "Present".
        """
        course = self.course_dropdown.get().strip()
        target_date = self.date_field.get().strip()

        if not course or course == "All Courses":
            CTkMessagebox(title="Validation Error", message="Please select a specific course before marking attendance.", icon="warning")
            return

        if not self._is_valid_date(target_date):
            CTkMessagebox(title="Validation Error", message="Please enter a valid date in YYYY-MM-DD format.", icon="warning")
            return

        try:
            students = get_students_by_course(course)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to load students for this course.\n{e}", icon="cancel")
            return

        if not students:
            CTkMessagebox(title="No Students Found", message=f"No students found for course: {course}", icon="warning")
            return

        existing_status_by_student = self._get_existing_statuses(target_date)
        self._show_mark_attendance_dialog(course, target_date, students, existing_status_by_student)

    def _get_existing_statuses(self, target_date):
        """Fetch existing attendance statuses for a given date, keyed by student_id.

        Args:
            target_date: The attendance date to look up.

        Returns:
            A dictionary mapping student_id to their existing status string.
        """
        try:
            existing_records = get_attendance_by_date(target_date)
        except Exception:
            existing_records = []

        return {r.get("student_id"): r.get("status") for r in existing_records}

    def _show_mark_attendance_dialog(self, course, target_date, students, existing_status_by_student):
        """Build and display the Mark Attendance dialog window.

        Args:
            course: The selected course name.
            target_date: The selected attendance date.
            students: List of student dictionaries for the course.
            existing_status_by_student: Dict mapping student_id to existing status.
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title("Mark Attendance")
        dialog.geometry("480x480")
        dialog.grab_set()
        dialog.attributes('-topmost', True)

        header_lbl = ctk.CTkLabel(
            dialog,
            text=f"{course}  •  {target_date}",
            font=ctk.CTkFont(family="Arial", size=15, weight="bold"),
            text_color="#1E293B"
        )
        header_lbl.pack(pady=(15, 10))

        scroll_area = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scroll_area.pack(fill="both", expand=True, padx=15, pady=5)

        status_entries = {}

        for student in students:
            student_id = student.get("student_id")
            default_status = existing_status_by_student.get(student_id, "Present")

            row = ctk.CTkFrame(scroll_area, fg_color="transparent")
            row.pack(fill="x", pady=5)

            name_lbl = ctk.CTkLabel(
                row,
                text=f"{student.get('fullname', '')} ({student_id})",
                font=ctk.CTkFont(family="Arial", size=13),
                anchor="w"
            )
            name_lbl.pack(side="left", fill="x", expand=True)

            status_var = ctk.StringVar(value=default_status)
            status_dropdown = ctk.CTkComboBox(row, values=self.STATUS_OPTIONS, variable=status_var, width=130)
            status_dropdown.pack(side="right")

            status_entries[student_id] = {"var": status_var, "student": student}

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", width=120, fg_color="#F1F5F9", text_color="#475569", hover_color="#E2E8F0", command=dialog.destroy)
        cancel_btn.grid(row=0, column=0, padx=10)

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Attendance",
            width=160,
            fg_color="#4F46E5",
            hover_color="#4338CA",
            command=lambda: self._confirm_mark_attendance(dialog, course, target_date, status_entries, existing_status_by_student)
        )
        save_btn.grid(row=0, column=1, padx=10)

    def _confirm_mark_attendance(self, dialog, course, target_date, status_entries, existing_status_by_student):
        """Validate and persist all attendance entries from the Mark Attendance dialog.

        All inserts/updates are performed inside a single database
        transaction so either every record is saved or none are.

        Args:
            dialog: The dialog window to close once processing is complete.
            course: The selected course name.
            target_date: The selected attendance date.
            status_entries: Dict mapping student_id to {"var", "student"}.
            existing_status_by_student: Dict mapping student_id to existing status.
        """
        attendance_records = []

        for student_id, entry in status_entries.items():
            student = entry["student"]
            status_value = entry["var"].get().strip()
            fullname = student.get("fullname", "").strip() if student.get("fullname") else ""

            error = self._validate_attendance_entry(course, target_date, student_id, fullname, status_value)
            if error:
                CTkMessagebox(title="Validation Error", message=error, icon="warning")
                return

            attendance_records.append({
                "student_id": student_id,
                "fullname": fullname,
                "course": course,
                "attendance_date": target_date,
                "status": status_value,
                "is_update": student_id in existing_status_by_student
            })

        try:
            saved_count = self._bulk_save_attendance(attendance_records)
            dialog.destroy()
            CTkMessagebox(title="Success", message=f"Attendance saved for {saved_count} student(s).", icon="check")
            self.refresh_table()
        except Exception as e:
            dialog.destroy()
            CTkMessagebox(title="Error", message=f"Failed to save attendance. No changes were made.\n{e}", icon="cancel")

    def _bulk_save_attendance(self, attendance_records):
        """Insert/update multiple attendance records inside a single transaction.

        Commits once after every record succeeds. Rolls back all changes if
        any record fails, so partial attendance batches are never saved.

        Args:
            attendance_records: List of dicts with student_id, fullname,
                course, attendance_date, status, and is_update.

        Returns:
            The number of records successfully processed.

        Raises:
            sqlite3.Error: If any database operation fails, after rollback.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()

            for record in attendance_records:
                if record["is_update"]:
                    cursor.execute(
                        "UPDATE attendance SET status = ? WHERE student_id = ? AND attendance_date = ?",
                        (record["status"], record["student_id"], record["attendance_date"])
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO attendance (student_id, fullname, course, attendance_date, status)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (record["student_id"], record["fullname"], record["course"], record["attendance_date"], record["status"])
                    )

            conn.commit()
            return len(attendance_records)
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_attendance_entry(self, course, attendance_date, student_id, fullname, status):
        """Validate a single attendance entry before it is saved.

        Args:
            course: The selected course name.
            attendance_date: The selected attendance date.
            student_id: The student's ID.
            fullname: The student's full name.
            status: The selected attendance status.

        Returns:
            An error message string if invalid, otherwise None.
        """
        if not course or course == "All Courses":
            return "Please select a valid course."

        if not self._is_valid_date(attendance_date):
            return "Please enter a valid date in YYYY-MM-DD format."

        if not student_id:
            return "Student ID is missing for one or more students."

        if not fullname:
            return "Full name is missing for one or more students."

        if not self._is_valid_status(status):
            return f"Invalid status. Must be one of: {', '.join(self.STATUS_OPTIONS)}."

        return None

    @classmethod
    def _is_valid_status(cls, status):
        """Check whether a status value is one of the allowed options.

        Args:
            status: The status string to validate.

        Returns:
            True if valid, False otherwise.
        """
        return status in cls.STATUS_OPTIONS

    @staticmethod
    def _is_valid_date(date_text):
        """Validate that a string matches the YYYY-MM-DD date format.

        Args:
            date_text: The date string to validate.

        Returns:
            True if valid, False otherwise.
        """
        if not date_text:
            return False
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x700")
    page = AttendancePage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()