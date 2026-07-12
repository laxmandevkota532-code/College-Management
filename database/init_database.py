import sqlite3

# Connect to Database
conn = sqlite3.connect("database/student_management.db")
cursor = conn.cursor()


# USERS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")


# STUDENTS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE NOT NULL,
    fullname TEXT NOT NULL,
    gender TEXT,
    dob TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    course TEXT,
    address TEXT,
    status TEXT DEFAULT 'Active'
)
""")


# COURSES TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id TEXT UNIQUE NOT NULL,
    course_name TEXT NOT NULL,
    duration TEXT,
    description TEXT
)
""")


# TEACHERS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id TEXT UNIQUE NOT NULL,
    fullname TEXT NOT NULL,
    subject TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    experience TEXT,
    status TEXT DEFAULT 'Active'
)
""")


# ATTENDANCE TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    fullname TEXT NOT NULL,
    course TEXT NOT NULL ,
    attendance_date TEXT NOT NULL,
    status TEXT NOT NULL,
    UNIQUE(student_id, attendance_date)
)
""")


# REPORTS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT UNIQUE NOT NULL,
    report_name TEXT NOT NULL,
    report_type TEXT,
    generated_date TEXT,
    status TEXT DEFAULT 'Ready'
)
""")

# SETTINGS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT,
    notifications INTEGER DEFAULT 1,
    dark_mode INTEGER DEFAULT 0,
    remember_login INTEGER DEFAULT 1
)
""")

conn.commit()
conn.close()

print("✅ Student Management Database Created Successfully!")


"""
Database Connection Module
---------------------------
Handles the SQLite connection and schema setup for the
Student Management System. This is the ONLY module that knows
about the physical database file path.
"""

import sqlite3
import os

# Path to the SQLite database file
DB_PATH = os.path.join("database", "student_management.db")


def get_connection():
    """
    Create and return a new SQLite connection.

    - Ensures the parent 'database/' directory exists.
    - Ensures the 'students' table exists (created on first run).
    - Uses sqlite3.Row so columns can be accessed by name (row["fullname"]).
    """
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    _initialize_schema(conn)
    return conn


def _initialize_schema(conn):
    """Create the students table if it does not already exist."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            fullname TEXT,
            gender TEXT,
            dob TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            course TEXT,
            address TEXT,
            status TEXT
        )
    """)
    conn.commit()