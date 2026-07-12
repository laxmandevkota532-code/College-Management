import sqlite3
from typing import List, Dict, Optional, Any

# Standard project-wide database helper. Assumed to return a connection 
# pre-configured with conn.row_factory = sqlite3.Row
from database.database import get_connection


class DuplicateTeacherIDError(Exception):
    """Exception raised when a teacher_id already exists in the database."""
    pass


def _fetch_all_as_dicts(cursor: sqlite3.Cursor, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Execute a query and return all rows as a list of dictionaries.
    
    Args:
        cursor: SQLite cursor object.
        query: SQL query string.
        params: Tuple of parameters for parameterized query.
    
    Returns:
        List of dictionaries representing rows, or empty list if no rows found.
    """
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def _fetch_one_as_dict(cursor: sqlite3.Cursor, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """
    Execute a query and return a single row as a dictionary.
    
    Args:
        cursor: SQLite cursor object.
        query: SQL query string.
        params: Tuple of parameters for parameterized query.
    
    Returns:
        Dictionary representing the row, or None if no row found.
    """
    cursor.execute(query, params)
    row = cursor.fetchone()
    return dict(row) if row else None


def _normalize_teacher_dict(db_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize database column names to frontend-expected keys.
    Maps fullname → teacher_name, subject → department, etc.
    
    Args:
        db_dict: Dictionary with database column names.
    
    Returns:
        Dictionary with normalized keys for frontend compatibility.
    """
    if not db_dict:
        return db_dict
    
    return {
        "id": db_dict.get("id"),
        "teacher_id": db_dict.get("teacher_id"),
        "teacher_name": db_dict.get("fullname"),
        "department": db_dict.get("subject"),
        "email": db_dict.get("email"),
        "phone": db_dict.get("phone"),
        "experience": db_dict.get("experience"),
        "status": db_dict.get("status"),
    }


def generate_teacher_id() -> str:
    """
    Automatically generate a new teacher ID (T001, T002, T003, etc.).
    Uses numeric ordering on the suffix to guarantee correct sequence.
    
    Returns:
        A new teacher ID string in the format 'TXXX' where XXX is a zero-padded number.
    
    Raises:
        sqlite3.Error: If database error occurs.
    """
    query = """
        SELECT teacher_id FROM teachers 
        WHERE teacher_id LIKE 'T%' 
        ORDER BY CAST(SUBSTR(teacher_id, 2) AS INTEGER) DESC 
        LIMIT 1
    """
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        row = _fetch_one_as_dict(cursor, query)
        
        if row and row.get('teacher_id'):
            last_id = row['teacher_id']
            num_part = int(last_id[1:]) + 1
            return f"T{num_part:03d}"
        
        return "T001"
    except sqlite3.Error as e:
        print(f"Error generating teacher ID: {e}")
        raise
    finally:
        conn.close()


def insert_teacher(teacher_data: Dict[str, Any]) -> bool:
    """
    Insert a new teacher record into the database.
    
    Args:
        teacher_data: Dictionary containing teacher information with keys:
                     teacher_id, teacher_name, department, email, phone,
                     experience, status.
    
    Returns:
        True if insertion was successful, False otherwise.
    
    Raises:
        DuplicateTeacherIDError: If teacher_id already exists (unique constraint violation).
    """
    query = """
        INSERT INTO teachers 
        (teacher_id, fullname, subject, email, phone, experience, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (
            teacher_data.get('teacher_id'),
            teacher_data.get('teacher_name'),
            teacher_data.get('department'),
            teacher_data.get('email'),
            teacher_data.get('phone'),
            teacher_data.get('experience'),
            teacher_data.get('status')
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        conn.rollback()
        error_msg = str(e).lower()
        if "unique constraint" in error_msg or "primary key" in error_msg:
            raise DuplicateTeacherIDError(f"Teacher ID '{teacher_data.get('teacher_id')}' already exists.")
        print(f"Integrity Error inserting teacher: {e}")
        return False
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Database Error inserting teacher: {e}")
        return False
    finally:
        conn.close()


def get_all_teachers() -> List[Dict[str, Any]]:
    """
    Retrieve all teachers from the database, sorted by teacher ID in numeric order.
    
    Returns:
        List of dictionaries containing all teacher records, sorted by teacher ID
        (e.g., T001, T002, T010). Empty list if no teachers found or on error.
    """
    query = """
        SELECT id, teacher_id, fullname, subject, email, phone, experience, status 
        FROM teachers 
        ORDER BY CAST(SUBSTR(teacher_id, 2) AS INTEGER)
    """
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        rows = _fetch_all_as_dicts(cursor, query)
        return [_normalize_teacher_dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Error fetching all teachers: {e}")
        return []
    finally:
        conn.close()


def get_recent_teachers(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve the most recently added teachers, sorted by numeric teacher ID.
    
    Args:
        limit: Maximum number of recent teachers to retrieve (default: 5).
    
    Returns:
        List of dictionaries containing up to 'limit' most recent teachers.
        Empty list if no teachers found or on error.
    """
    query = """
        SELECT id, teacher_id, fullname, subject, email, phone, experience, status 
        FROM teachers 
        ORDER BY CAST(SUBSTR(teacher_id, 2) AS INTEGER) DESC 
        LIMIT ?
    """
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        rows = _fetch_all_as_dicts(cursor, query, (limit,))
        return [_normalize_teacher_dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Error fetching recent teachers: {e}")
        return []
    finally:
        conn.close()


def get_teacher_by_id(teacher_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single teacher by their unique teacher ID.
    
    Args:
        teacher_id: The teacher ID to search for (e.g., 'T001').
    
    Returns:
        Dictionary containing teacher record if found, None otherwise.
    """
    query = "SELECT id, teacher_id, fullname, subject, email, phone, experience, status FROM teachers WHERE teacher_id = ?"
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        row = _fetch_one_as_dict(cursor, query, (teacher_id,))
        return _normalize_teacher_dict(row) if row else None
    except sqlite3.Error as e:
        print(f"Error fetching teacher by ID '{teacher_id}': {e}")
        return None
    finally:
        conn.close()


def search_teachers(keyword: str) -> List[Dict[str, Any]]:
    """
    Search for teachers across multiple fields with case-insensitive matching.
    
    Searches across: teacher_id, fullname, subject, email, phone, and status.
    
    Args:
        keyword: Search term to match. Whitespace is trimmed automatically.
                If empty after trimming, returns all teachers.
    
    Returns:
        List of dictionaries containing matching teacher records,
        sorted by numeric teacher ID. Empty list if no matches found or on error.
    """
    keyword = keyword.strip()
    
    # If search keyword is empty, return all teachers
    if not keyword:
        return get_all_teachers()
    
    query = """
        SELECT id, teacher_id, fullname, subject, email, phone, experience, status 
        FROM teachers 
        WHERE teacher_id LIKE ?
           OR fullname LIKE ? 
           OR subject LIKE ? 
           OR email LIKE ?
           OR phone LIKE ?
           OR status LIKE ?
        ORDER BY CAST(SUBSTR(teacher_id, 2) AS INTEGER)
    """
    search_pattern = f"%{keyword}%"
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        params = (search_pattern,) * 6
        rows = _fetch_all_as_dicts(cursor, query, params)
        return [_normalize_teacher_dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"Error searching teachers with keyword '{keyword}': {e}")
        return []
    finally:
        conn.close()


def update_teacher(teacher_data: Dict[str, Any]) -> bool:
    """
    Update an existing teacher's record by teacher ID.
    
    Args:
        teacher_data: Dictionary containing teacher information with required key
                     'teacher_id' to identify the record, plus fields to update:
                     teacher_name, department, email, phone, experience, status.
    
    Returns:
        True if a record was updated successfully, False if no matching record
        found or database error occurred.
    """
    query = """
        UPDATE teachers 
        SET fullname = ?, 
            subject = ?, 
            email = ?, 
            phone = ?, 
            experience = ?, 
            status = ?
        WHERE teacher_id = ?
    """
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (
            teacher_data.get('teacher_name'),
            teacher_data.get('department'),
            teacher_data.get('email'),
            teacher_data.get('phone'),
            teacher_data.get('experience'),
            teacher_data.get('status'),
            teacher_data.get('teacher_id')
        ))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error updating teacher '{teacher_data.get('teacher_id')}': {e}")
        return False
    finally:
        conn.close()


def delete_teacher(teacher_id: str) -> bool:
    """
    Delete a teacher record by their unique teacher ID.
    
    Args:
        teacher_id: The teacher ID to delete (e.g., 'T001').
    
    Returns:
        True if a record was deleted successfully, False if no matching record
        found or database error occurred.
    """
    query = "DELETE FROM teachers WHERE teacher_id = ?"
    conn = get_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (teacher_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error deleting teacher '{teacher_id}': {e}")
        return False
    finally:
        conn.close()