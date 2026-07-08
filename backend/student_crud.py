"""
Student CRUD Operations
------------------------
Every SQL statement for the 'students' table lives here.
The UI layer must NEVER execute raw SQL - it only calls the
functions defined in this module and handles the exceptions
they raise.
"""

import sqlite3
from database.database import get_connection

# Columns that are safe to use in ORDER BY / WHERE clauses.
# (Whitelisting prevents SQL injection via f-string column names.)
_SORTABLE_COLUMNS = {
    "student_id": "student_id",
    "fullname": "fullname",
    "course": "course",
    "status": "status",
    "id": "id",
}


class DuplicateStudentIDError(Exception):
    """Raised when a student_id already exists in the database."""
    pass


class DuplicateEmailError(Exception):
    """Raised when an email already exists in the database."""
    pass


def generate_student_id():
    """
    Generate the next sequential Student ID in the format STU-0001.

    Looks at the highest existing numeric suffix among IDs matching
    'STU-####' and returns the next one in sequence.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id FROM students
            WHERE student_id LIKE 'STU-%'
            ORDER BY CAST(SUBSTR(student_id, 5) AS INTEGER) DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row is None:
            return "STU-0001"

        last_number = int(row["student_id"].split("-")[1])
        return f"STU-{last_number + 1:04d}"
    finally:
        conn.close()


def insert_student(student_data):
    """
    Insert a new student record.

    student_data: tuple in the order
        (student_id, fullname, gender, dob, email, phone, course, address, status)

    Raises:
        DuplicateStudentIDError - if student_id already exists
        DuplicateEmailError     - if email already exists
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students
                (student_id, fullname, gender, dob, email, phone, course, address, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, student_data)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as error:
        _raise_specific_integrity_error(error)
    finally:
        conn.close()


def get_all_students(order_by="id", descending=True):
    """
    Fetch every student, ordered by the given column.
    Defaults to newest-first (id DESC), per spec.
    """
    column = _SORTABLE_COLUMNS.get(order_by, "id")
    direction = "DESC" if descending else "ASC"

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT student_id, fullname, course, email, phone, status
            FROM students
            ORDER BY {column} {direction}
        """)
        return cursor.fetchall()
    finally:
        conn.close()


def get_student(student_id):
    """Fetch a single full student record by student_id. Returns None if not found."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        return cursor.fetchone()
    finally:
        conn.close()


def update_student(student_id, student_data):
    """
    Update an existing student identified by student_id.

    student_data: tuple in the order
        (fullname, gender, dob, email, phone, course, address, status)

    Returns True if a row was updated, False if student_id was not found.
    Raises DuplicateEmailError if the new email collides with another record.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students
            SET fullname = ?, gender = ?, dob = ?, email = ?,
                phone = ?, course = ?, address = ?, status = ?
            WHERE student_id = ?
        """, (*student_data, student_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.IntegrityError as error:
        _raise_specific_integrity_error(error)
    finally:
        conn.close()


def delete_student(student_id):
    """Delete a student by student_id. Returns True if a row was deleted."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def search_students(keyword, order_by="id", descending=True):
    """
    Search students by Student ID, Name, Email, or Course
    (case-insensitive partial match), ordered by the given column.
    """
    column = _SORTABLE_COLUMNS.get(order_by, "id")
    direction = "DESC" if descending else "ASC"
    like_term = f"%{keyword}%"

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT student_id, fullname, course, email, phone, status
            FROM students
            WHERE student_id LIKE ? OR fullname LIKE ? OR email LIKE ? OR course LIKE ?
            ORDER BY {column} {direction}
        """, (like_term, like_term, like_term, like_term))
        return cursor.fetchall()
    finally:
        conn.close()


def email_exists(email, exclude_student_id=None):
    """Check whether an email is already registered (optionally excluding one student)."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if exclude_student_id:
            cursor.execute(
                "SELECT 1 FROM students WHERE email = ? AND student_id != ?",
                (email, exclude_student_id),
            )
        else:
            cursor.execute("SELECT 1 FROM students WHERE email = ?", (email,))
        return cursor.fetchone() is not None
    finally:
        conn.close()


def _raise_specific_integrity_error(error):
    """Translate a raw sqlite3.IntegrityError into a specific, catchable exception."""
    message = str(error).lower()
    if "student_id" in message:
        raise DuplicateStudentIDError("This Student ID already exists.") from error
    elif "email" in message:
        raise DuplicateEmailError("This email is already registered.") from error
    else:
        raise error