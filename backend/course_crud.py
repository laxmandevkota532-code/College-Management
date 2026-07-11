import re
import sqlite3

from database.database import get_connection

# --------------------------------------------------
# CUSTOM EXCEPTIONS
# --------------------------------------------------
class DuplicateCourseIDError(Exception):
    """Raised when a course_id already exists in the database."""
    pass


# --------------------------------------------------
# COURSE ID GENERATION
# --------------------------------------------------
def generate_course_id() -> str:
    """
    Generates the next sequential Course ID in the format CRS-0001.
    Looks at the most recently inserted row (by id) and increments the
    numeric suffix of its course_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT course_id FROM courses ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    next_number = 1
    if row is not None and row["course_id"]:
        match = re.search(r"(\d+)$", row["course_id"])
        if match:
            next_number = int(match.group(1)) + 1

    return f"CRS-{next_number:04d}"


# --------------------------------------------------
# INSERT
# --------------------------------------------------
def insert_course(course_data: dict) -> None:
    """
    Inserts a new course record into the existing 'courses' table.

    Expected keys in course_data:
        course_id, course_name, duration, description

    Raises:
        DuplicateCourseIDError: if course_id already exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO courses
                (course_id, course_name, duration, description)
            VALUES (?, ?, ?, ?)
            """,
            (
                course_data["course_id"],
                course_data["course_name"],
                course_data["duration"],
                course_data["description"],
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        message = str(e).lower()
        if "course_id" in message:
            raise DuplicateCourseIDError(
                f"Course ID '{course_data['course_id']}' already exists."
            ) from e
        raise
    finally:
        conn.close()


# --------------------------------------------------
# READ (RECENT COURSES)
# --------------------------------------------------
def get_recent_courses(limit: int = 4) -> list[dict]:
    """
    Returns the most recently added courses as a list of dicts,
    each containing at least "course_id" and "course_name".
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT course_id, course_name FROM courses ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# --------------------------------------------------
# READ (ALL COURSES)
# --------------------------------------------------
def get_all_courses() -> list[dict]:
    """
    Returns every course record for the Course Management table,
    ordered by insertion order (oldest first).

    Each dict contains: course_id, course_name, duration, description.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT course_id, course_name, duration, description
        FROM courses
        ORDER BY id ASC
        """
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# --------------------------------------------------
# DELETE
# --------------------------------------------------
def delete_course(course_id: str) -> None:
    """
    Deletes the course with the given course_id from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
    conn.commit()
    conn.close()