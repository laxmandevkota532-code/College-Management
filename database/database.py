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
    fullname TEXT,
    course TEXT,
    attendance_date TEXT,
    status TEXT
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

