import sqlite3
from typing import List, Dict, Optional, Any

from database.database import get_connection


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert a sqlite3.Row object into a plain dictionary.

    Args:
        row: A sqlite3.Row instance returned from a query.

    Returns:
        A dictionary representation of the row.
    """
    return dict(row) if row is not None else {}


def _rows_to_dicts(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    """Convert a list of sqlite3.Row objects into a list of dictionaries.

    Args:
        rows: A list of sqlite3.Row instances returned from a query.

    Returns:
        A list of dictionaries representing each row.
    """
    return [dict(row) for row in rows]


def save_attendance(attendance_data: Dict[str, Any]) -> bool:
    """Insert a new attendance record into the database.

    Args:
        attendance_data: Dictionary containing the attendance fields:
            student_id, fullname, course, attendance_date, status.

    Returns:
        True if the record was inserted successfully, False otherwise.
    """
    query = """
        INSERT INTO attendance (student_id, fullname, course, attendance_date, status)
        VALUES (?, ?, ?, ?, ?)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            query,
            (
                attendance_data.get("student_id"),
                attendance_data.get("fullname"),
                attendance_data.get("course"),
                attendance_data.get("attendance_date"),
                attendance_data.get("status"),
            ),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error saving attendance: {e}")
        return False


def attendance_exists(student_id: str, attendance_date: str) -> bool:
    """Check whether an attendance record already exists for a student on a given date.

    Args:
        student_id: The ID of the student.
        attendance_date: The date to check for (expected format: YYYY-MM-DD).

    Returns:
        True if a matching attendance record exists, False otherwise.
    """
    query = """
        SELECT 1 FROM attendance
        WHERE student_id = ? AND attendance_date = ?
        LIMIT 1
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (student_id, attendance_date))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error checking attendance existence: {e}")
        return False


def update_attendance(attendance_data: Dict[str, Any]) -> bool:
    """Update the status of an existing attendance record.

    Matches the record using student_id and attendance_date, and updates
    only the status field.

    Args:
        attendance_data: Dictionary containing at least student_id,
            attendance_date, and status.

    Returns:
        True if a record was updated, False otherwise.
    """
    query = """
        UPDATE attendance
        SET status = ?
        WHERE student_id = ? AND attendance_date = ?
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            query,
            (
                attendance_data.get("status"),
                attendance_data.get("student_id"),
                attendance_data.get("attendance_date"),
            ),
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error updating attendance: {e}")
        return False


def get_all_attendance() -> List[Dict[str, Any]]:
    """Retrieve every attendance record from the database.

    Returns:
        A list of dictionaries, each representing an attendance record,
        ordered by attendance_date descending and student_id ascending.
    """
    query = """
        SELECT * FROM attendance
        ORDER BY attendance_date DESC, student_id ASC
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return _rows_to_dicts(rows)
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error fetching all attendance: {e}")
        return []


def get_attendance_by_date(attendance_date: str) -> List[Dict[str, Any]]:
    """Retrieve attendance records for a specific date.

    Args:
        attendance_date: The date to filter by (expected format: YYYY-MM-DD).

    Returns:
        A list of dictionaries representing attendance records for the
        given date, ordered by student_id ascending.
    """
    query = """
        SELECT * FROM attendance
        WHERE attendance_date = ?
        ORDER BY student_id ASC
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (attendance_date,))
        rows = cursor.fetchall()
        conn.close()
        return _rows_to_dicts(rows)
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error fetching attendance by date: {e}")
        return []


def get_students_by_course(course: str) -> List[Dict[str, Any]]:
    """Retrieve students enrolled in a specific course.

    Args:
        course: The course name to filter students by.

    Returns:
        A list of dictionaries containing student_id, fullname, and course,
        ordered by student_id ascending.
    """
    query = """
        SELECT student_id, fullname, course
        FROM students
        WHERE course = ?
        ORDER BY student_id ASC
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (course,))
        rows = cursor.fetchall()
        conn.close()
        return _rows_to_dicts(rows)
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error fetching students by course: {e}")
        return []


def search_attendance(keyword: str) -> List[Dict[str, Any]]:
    """Search attendance records by keyword across multiple fields.

    Performs a case-insensitive LIKE search on student_id, fullname,
    course, attendance_date, and status.

    Args:
        keyword: The search term entered by the user.

    Returns:
        A list of dictionaries representing matching attendance records,
        ordered by attendance_date descending and student_id ascending.
    """
    query = """
        SELECT * FROM attendance
        WHERE student_id LIKE ?
           OR fullname LIKE ?
           OR course LIKE ?
           OR attendance_date LIKE ?
           OR status LIKE ?
        ORDER BY attendance_date DESC, student_id ASC
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        search_term = f"%{keyword}%"
        cursor.execute(
            query,
            (search_term, search_term, search_term, search_term, search_term),
        )
        rows = cursor.fetchall()
        conn.close()
        return _rows_to_dicts(rows)
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error searching attendance: {e}")
        return []


def delete_attendance(record_id: int) -> bool:
    """Delete a single attendance record by its integer ID.

    Args:
        record_id: The primary key ID of the attendance record to delete.

    Returns:
        True if the record was deleted successfully, False otherwise.
    """
    query = "DELETE FROM attendance WHERE id = ?"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (record_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error deleting attendance: {e}")
        return False


def get_attendance_summary() -> Dict[str, Any]:
    """Calculate a summary of attendance statistics.

    Uses SQL COUNT() queries to determine the total number of records,
    the number of present records, and the number of absent records,
    then safely calculates the attendance percentage.

    Returns:
        A dictionary with the following keys:
            total: Total number of attendance records.
            present: Number of records with status "Present".
            absent: Number of records with status "Absent".
            percentage: Attendance percentage (present / total * 100),
                rounded to 2 decimal places. 0 if total is 0.
    """
    total_query = "SELECT COUNT(*) AS total FROM attendance"
    present_query = "SELECT COUNT(*) AS present FROM attendance WHERE status = 'Present'"
    absent_query = "SELECT COUNT(*) AS absent FROM attendance WHERE status = 'Absent'"

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(total_query)
        total = cursor.fetchone()["total"]

        cursor.execute(present_query)
        present = cursor.fetchone()["present"]

        cursor.execute(absent_query)
        absent = cursor.fetchone()["absent"]

        conn.close()

        percentage = round((present / total) * 100, 2) if total > 0 else 0

        return {
            "total": total,
            "present": present,
            "absent": absent,
            "percentage": percentage,
        }
    except sqlite3.Error as e:
        print(f"[attendance_crud] Error generating attendance summary: {e}")
        return {
            "total": 0,
            "present": 0,
            "absent": 0,
            "percentage": 0,
        }