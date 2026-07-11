from database.database import get_connection


def get_total_students():
    """Return the total number of students in the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception:
        return 0
    finally:
        conn.close()


def get_total_courses():
    """Return the total number of courses in the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception:
        return 0
    finally:
        conn.close()


def get_total_teachers():
    """Return the total number of teachers in the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM teachers;")
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception:
        return 0
    finally:
        conn.close()


def get_attendance_rate():
    """Return the attendance rate as a whole-number percentage.

    Rate = (Present Records / Total Attendance Records) * 100
    Returns 0 if there are no attendance records.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance;")
        total_row = cursor.fetchone()
        total = total_row[0] if total_row else 0

        if not total:
            return 0

        cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'Present';")
        present_row = cursor.fetchone()
        present = present_row[0] if present_row else 0

        return round((present / total) * 100)
    except Exception:
        return 0
    finally:
        conn.close()


def get_recent_students():
    """Return the latest 5 students, newest first.

    Each record is a tuple: (student_id, fullname, course, email, status)
    Returns an empty list if there are no students.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT student_id, fullname, course, email, status
            FROM students
            ORDER BY id DESC
            LIMIT 5;
            """
        )
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        conn.close()