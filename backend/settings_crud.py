"""Backend CRUD operations for the Settings page.

Handles admin profile management, password changes, application
preferences, and system/database status information using SQLite.

Assumption: the database file lives at ``database/college.db`` relative
to the project root, matching the ``database/`` folder used by the rest
of the project. If the Student/Course modules already use a shared
connection helper (e.g. ``database/db_connection.py``) with a different
path, update ``DB_PATH`` below to match it.
"""

from __future__ import annotations

import hashlib
import logging
import os
import secrets
import sqlite3
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)

DB_PATH = os.path.join("database", "college.db")

APP_NAME = "College Management System"
APP_VERSION = "1.0"
DEVELOPER_NAME = "Laxman"

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"
_PBKDF2_ITERATIONS = 100_000


def _get_connection() -> sqlite3.Connection:
    """Create and return a new SQLite connection."""
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _hash_password(password: str, salt: Optional[bytes] = None) -> str:
    """Hash a password with PBKDF2-HMAC-SHA256. Returns 'salt_hex$digest_hex'."""
    if salt is None:
        salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plaintext password against a stored 'salt_hex$digest_hex' hash."""
    try:
        salt_hex, digest_hex = stored_hash.split("$")
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
    return secrets.compare_digest(digest.hex(), digest_hex)


def initialize_tables() -> None:
    """Create the admin_profile and app_preferences tables if missing."""
    try:
        with _get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS admin_profile (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    full_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    password_hash TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS app_preferences (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    enable_notifications INTEGER NOT NULL DEFAULT 1,
                    enable_dark_mode INTEGER NOT NULL DEFAULT 1,
                    remember_login INTEGER NOT NULL DEFAULT 1
                )
                """
            )
            if conn.execute("SELECT COUNT(*) FROM admin_profile").fetchone()[0] == 0:
                conn.execute(
                    "INSERT INTO admin_profile "
                    "(id, full_name, username, email, phone, password_hash) "
                    "VALUES (1, ?, ?, ?, ?, ?)",
                    (
                        "Admin User",
                        DEFAULT_USERNAME,
                        "admin@edumanager.com",
                        "+1 234 567 890",
                        _hash_password(DEFAULT_PASSWORD),
                    ),
                )
            if conn.execute("SELECT COUNT(*) FROM app_preferences").fetchone()[0] == 0:
                conn.execute(
                    "INSERT INTO app_preferences "
                    "(id, enable_notifications, enable_dark_mode, remember_login) "
                    "VALUES (1, 1, 1, 1)"
                )
            conn.commit()
    except sqlite3.Error:
        logger.exception("Failed to initialize settings tables")
        raise


def get_admin_profile() -> Dict[str, str]:
    """Return the admin's profile fields (password excluded)."""
    try:
        with _get_connection() as conn:
            row = conn.execute(
                "SELECT full_name, username, email, phone FROM admin_profile WHERE id = 1"
            ).fetchone()
        if row is None:
            raise ValueError("Admin profile not found")
        return {"full_name": row[0], "username": row[1], "email": row[2], "phone": row[3]}
    except sqlite3.Error:
        logger.exception("Failed to fetch admin profile")
        raise


def update_admin_profile(full_name: str, username: str, email: str, phone: str) -> None:
    """Update the admin's profile fields."""
    if not all([full_name.strip(), username.strip(), email.strip(), phone.strip()]):
        raise ValueError("All profile fields are required")
    try:
        with _get_connection() as conn:
            conn.execute(
                "UPDATE admin_profile SET full_name = ?, username = ?, "
                "email = ?, phone = ? WHERE id = 1",
                (full_name.strip(), username.strip(), email.strip(), phone.strip()),
            )
            conn.commit()
    except sqlite3.Error:
        logger.exception("Failed to update admin profile")
        raise


def change_password(current_password: str, new_password: str) -> None:
    """Verify the current password, then update it to new_password."""
    if len(new_password) < 6:
        raise ValueError("New password must be at least 6 characters long")
    try:
        with _get_connection() as conn:
            row = conn.execute(
                "SELECT password_hash FROM admin_profile WHERE id = 1"
            ).fetchone()
            if row is None:
                raise ValueError("Admin profile not found")
            if not _verify_password(current_password, row[0]):
                raise ValueError("Current password is incorrect")
            conn.execute(
                "UPDATE admin_profile SET password_hash = ? WHERE id = 1",
                (_hash_password(new_password),),
            )
            conn.commit()
    except sqlite3.Error:
        logger.exception("Failed to change password")
        raise


def get_preferences() -> Dict[str, bool]:
    """Return the saved application preferences."""
    try:
        with _get_connection() as conn:
            row = conn.execute(
                "SELECT enable_notifications, enable_dark_mode, remember_login "
                "FROM app_preferences WHERE id = 1"
            ).fetchone()
        if row is None:
            raise ValueError("Preferences not found")
        return {
            "enable_notifications": bool(row[0]),
            "enable_dark_mode": bool(row[1]),
            "remember_login": bool(row[2]),
        }
    except sqlite3.Error:
        logger.exception("Failed to fetch preferences")
        raise


def update_preferences(
    enable_notifications: bool, enable_dark_mode: bool, remember_login: bool
) -> None:
    """Persist application preferences."""
    try:
        with _get_connection() as conn:
            conn.execute(
                "UPDATE app_preferences SET enable_notifications = ?, "
                "enable_dark_mode = ?, remember_login = ? WHERE id = 1",
                (int(enable_notifications), int(enable_dark_mode), int(remember_login)),
            )
            conn.commit()
    except sqlite3.Error:
        logger.exception("Failed to update preferences")
        raise


def get_system_information() -> Dict[str, str]:
    """Return static application metadata for the System Information cards."""
    return {"app_name": APP_NAME, "version": APP_VERSION, "developer": DEVELOPER_NAME}


def get_database_status() -> str:
    """Check database connectivity. Returns 'Active' or 'Inactive'."""
    try:
        with _get_connection() as conn:
            conn.execute("SELECT 1")
        return "Active"
    except sqlite3.Error:
        logger.exception("Database status check failed")
        return "Inactive"


def backup_database_info() -> Dict[str, str]:
    """Return the storage engine name and the database file's last-modified time."""
    engine = "SQLite"
    if os.path.exists(DB_PATH):
        modified = datetime.fromtimestamp(os.path.getmtime(DB_PATH))
        last_modified = modified.strftime("%Y-%m-%d %H:%M")
    else:
        last_modified = "Never"
    return {"engine": engine, "last_modified": last_modified}