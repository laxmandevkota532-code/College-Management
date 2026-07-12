"""
Backend CRUD Module for Reports Management
Handles database operations for the Reports Page using the existing SQLite schema.
"""

import sqlite3
from database.database import get_connection

# =============================================
# DASHBOARD
# =============================================

def get_dashboard_statistics():
    """Returns summary statistics for the dashboard cards."""
    conn = get_connection()
    cursor = conn.cursor()
    
    stats = {}
    
    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    stats["total_students"] = cursor.fetchone()[0]
    
    # Total Courses
    cursor.execute("SELECT COUNT(*) FROM courses")
    stats["total_courses"] = cursor.fetchone()[0]
    
    # Total Teachers
    cursor.execute("SELECT COUNT(*) FROM teachers")
    stats["total_teachers"] = cursor.fetchone()[0]
    
    # Attendance Rate
    cursor.execute("""
        SELECT CAST(SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*) 
        FROM attendance
    """)
    res = cursor.fetchone()[0]
    stats["attendance_rate"] = f"{int(res) if res is not None else 0}%"
    
    conn.close()
    return stats


# =============================================
# REPORT DATA RETRIEVAL
# =============================================

def get_student_reports():
    """Returns list of students with column aliases matching frontend keys."""
    conn = get_connection()
    cursor = conn.cursor()
    # Frontend expects: id, name, course, status
    cursor.execute("SELECT id, fullname AS name, course, status FROM students")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_teacher_reports():
    """Returns list of teachers with column aliases matching frontend keys."""
    conn = get_connection()
    cursor = conn.cursor()
    # Frontend expects: id, name, department, status
    # Assuming 'subject' acts as 'department'
    cursor.execute("SELECT teacher_id AS id, fullname AS name, subject AS department, status FROM teachers")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_course_reports():
    """Returns list of courses with column aliases matching frontend keys."""
    conn = get_connection()
    cursor = conn.cursor()
    # Frontend expects: name, instructor, students, status
    # Note: 'students' count requires join or subquery if not in table
    cursor.execute("""
        SELECT course_name AS name, 'N/A' AS instructor, 0 AS students, 'Active' AS status 
        FROM courses
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_attendance_reports():
    """Returns list of attendance with column aliases matching frontend keys."""
    conn = get_connection()
    cursor = conn.cursor()
    # Frontend expects: student, date, course, status
    cursor.execute("SELECT fullname AS student, attendance_date AS date, course, status FROM attendance")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# =============================================
# EXPORT FUNCTIONS (Mock)
# =============================================

def prepare_student_export(data, format="pdf"):
    print(f"✅ Student Report exported as {format.upper()}")

def prepare_teacher_export(data, format="pdf"):
    print(f"✅ Teacher Report exported as {format.upper()}")

def prepare_course_export(data, format="pdf"):
    print(f"✅ Course Report exported as {format.upper()}")

def prepare_attendance_export(data, format="pdf"):
    print(f"✅ Attendance Report exported as {format.upper()}")