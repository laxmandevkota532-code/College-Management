import re
import sqlite3

from database.database import get_connection

# --------------------------------------------------
# CUSTOM EXCEPTIONS
# --------------------------------------------------
class DuplicateStudentIDError(Exception):
    """Raised when a student_id already exists in the database."""
    pass


class DuplicateEmailError(Exception):
    """Raised when an email address already exists in the database."""
    pass


# --------------------------------------------------
# STUDENT ID GENERATION
# --------------------------------------------------
def generate_student_id() -> str:
    """
    Generates the next sequential Student ID in the format STU-0001.
    Looks at the most recently inserted row (by id) and increments the
    numeric suffix of its student_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    next_number = 1
    if row is not None and row["student_id"]:
        match = re.search(r"(\d+)$", row["student_id"])
        if match:
            next_number = int(match.group(1)) + 1

    return f"STU-{next_number:04d}"


# --------------------------------------------------
# INSERT
# --------------------------------------------------
def insert_student(student_data: dict) -> None:
    """
    Inserts a new student record into the existing 'students' table.

    Expected keys in student_data:
        student_id, fullname, email, phone, dob, course, gender, address, status

    Raises:
        DuplicateStudentIDError: if student_id already exists.
        DuplicateEmailError: if email already exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO students
                (student_id, fullname, gender, dob, email, phone, course, address, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_data["student_id"],
                student_data["fullname"],
                student_data["gender"],
                student_data["dob"],
                student_data["email"],
                student_data["phone"],
                student_data["course"],
                student_data["address"],
                student_data["status"],
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        message = str(e).lower()
        if "student_id" in message:
            raise DuplicateStudentIDError(
                f"Student ID '{student_data['student_id']}' already exists."
            ) from e
        if "email" in message:
            raise DuplicateEmailError(
                f"Email '{student_data['email']}' is already registered."
            ) from e
        raise
    finally:
        conn.close()


# --------------------------------------------------
# READ (RECENT STUDENTS)
# --------------------------------------------------
def get_recent_students(limit: int = 4) -> list[dict]:
    """
    Returns the most recently added students as a list of dicts,
    each containing at least "student_id" and "fullname".
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT student_id, fullname FROM students ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# --------------------------------------------------
# READ (ALL STUDENTS)
# --------------------------------------------------
def get_all_students() -> list[dict]:
    """
    Returns every student record for the Student Management table,
    ordered by insertion order (oldest first).

    Each dict contains: student_id, fullname, gender, dob, email,
    phone, course, address, status.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT student_id, fullname, gender, dob, email, phone, course, address, status
        FROM students
        ORDER BY id ASC
        """
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# --------------------------------------------------
# DELETE
# --------------------------------------------------
def delete_student(student_id: str) -> None:
    """
    Deletes the student with the given student_id from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()


# --------------------------------------------------
# UPDATE
# --------------------------------------------------
def update_student(student_data: dict) -> None:
    """
    Updates an existing student using student_id.

    Expected keys in student_data:
        student_id, fullname, email, phone, dob, course, gender, address, status
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET
            fullname = ?,
            gender = ?,
            dob = ?,
            email = ?,
            phone = ?,
            course = ?,
            address = ?,
            status = ?
        WHERE student_id = ?
    """, (
        student_data["fullname"],
        student_data["gender"],
        student_data["dob"],
        student_data["email"],
        student_data["phone"],
        student_data["course"],
        student_data["address"],
        student_data["status"],
        student_data["student_id"]
    ))

    conn.commit()
    conn.close()