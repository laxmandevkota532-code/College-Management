"""Settings page for the College Management System.

Fully backend-driven Settings page built with CustomTkinter. The visual
design (colors, fonts, spacing, layout, widget positions) is unchanged
from the original static page; this module only wires the existing
widgets to backend/settings_crud.py for persistence, validation, and
user feedback dialogs.
"""

from __future__ import annotations

import logging
import re
import tkinter as tk
from typing import Dict, List

import customtkinter as ctk

from backend.settings_crud import (
    backup_database_info,
    change_password,
    get_admin_profile,
    get_database_status,
    get_preferences,
    get_system_information,
    initialize_tables,
    update_admin_profile,
    update_preferences,
)

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

logger = logging.getLogger(__name__)


class SettingsPage(ctk.CTkFrame):
    """Admin settings page: profile, password, system info, and preferences."""

    _EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _PHONE_PATTERN = re.compile(r"^[\d\s()+\-]{7,20}$")

    _PROFILE_FIELD_ATTR = {
        "Full Name": "full_name_entry",
        "Username": "username_entry",
        "Email Address": "email_entry",
        "Phone Number": "phone_entry",
    }

    _PASSWORD_FIELD_ATTR = {
        "Current Password": "current_password_entry",
        "New Password": "new_password_entry",
        "Confirm Password": "confirm_password_entry",
    }

    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master, fg_color="#F8F9FC")

        # --- Color Palette ---
        self.PRIMARY_BLUE = "#4F5BD5"
        self.HOVER_BLUE = "#3F4ACB"
        self.BACKGROUND = "#F8F9FC"
        self.PANEL_BG = "#EEF2FF"
        self.TEXT_DARK = "#111827"
        self.TEXT_GRAY = "#6B7280"
        self.WHITE = "#FFFFFF"
        self.SUCCESS_GREEN = "#10B981"
        self.ERROR_RED = "#EF4444"

        self.system_info_labels: Dict[str, ctk.CTkLabel] = {}

        # Configure page grid layout as required
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_main_content()
        self._initialize_backend()

    # ------------------------------------------------------------------
    # UI construction (unchanged visual structure)
    # ------------------------------------------------------------------
    def create_main_content(self) -> None:
        """Builds responsive scrollable layout framework for system settings."""
        self._build_top_bar()

        scroll_content = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        scroll_content.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")
        scroll_content.grid_columnconfigure(0, weight=1)

        self._build_profile_section(scroll_content)
        self._build_password_section(scroll_content)
        self._build_system_info_section(scroll_content)
        self._build_preferences_section(scroll_content)

    def _build_top_bar(self) -> None:
        top_bar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color=self.WHITE)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_propagate(False)

        page_title = ctk.CTkLabel(
            top_bar, text="Settings", font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.TEXT_DARK,
        )
        page_title.grid(row=0, column=0, padx=30, pady=20, sticky="w")

        self.user_profile_label = ctk.CTkLabel(
            top_bar, text="Admin User", font=ctk.CTkFont(size=14), text_color=self.TEXT_GRAY,
        )
        self.user_profile_label.grid(row=0, column=1, padx=30, pady=20, sticky="e")

    def _build_profile_section(self, parent: ctk.CTkScrollableFrame) -> None:
        profile_section = ctk.CTkFrame(parent, fg_color=self.WHITE, corner_radius=8)
        profile_section.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        profile_section.grid_columnconfigure((0, 1), weight=1)

        p_sec_title = ctk.CTkLabel(
            profile_section, text="Profile Settings", font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.TEXT_DARK,
        )
        p_sec_title.grid(row=0, column=0, columnspan=2, padx=24, pady=(20, 15), sticky="w")

        fields = [
            ("Full Name", "Admin User", 1, 0),
            ("Username", "admin", 1, 1),
            ("Email Address", "admin@edumanager.com", 2, 0),
            ("Phone Number", "+1 234 567 890", 2, 1),
        ]

        for label_text, default_val, r, c in fields:
            f_frame = ctk.CTkFrame(profile_section, fg_color="transparent")
            f_frame.grid(row=r, column=c, padx=24, pady=10, sticky="ew")
            f_frame.grid_columnconfigure(0, weight=1)

            lbl = ctk.CTkLabel(
                f_frame, text=label_text, font=ctk.CTkFont(size=13, weight="normal"),
                text_color=self.TEXT_GRAY,
            )
            lbl.grid(row=0, column=0, sticky="w", pady=(0, 5))

            entry = ctk.CTkEntry(
                f_frame, height=40, fg_color=self.WHITE, border_color=self.PANEL_BG,
                text_color=self.TEXT_DARK,
            )
            entry.insert(0, default_val)
            entry.grid(row=1, column=0, sticky="ew")
            setattr(self, self._PROFILE_FIELD_ATTR[label_text], entry)

        p_btn_frame = ctk.CTkFrame(profile_section, fg_color="transparent")
        p_btn_frame.grid(row=3, column=0, columnspan=2, padx=24, pady=(15, 20), sticky="e")

        self.update_profile_btn = ctk.CTkButton(
            p_btn_frame, text="Update Profile", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE,
            height=36, corner_radius=6, command=self._on_update_profile,
        )
        self.update_profile_btn.grid(row=0, column=0, padx=(0, 10))

        self.reset_profile_btn = ctk.CTkButton(
            p_btn_frame, text="Reset Changes", font=ctk.CTkFont(size=13),
            fg_color="#F3F4F6", hover_color="#E5E7EB", text_color=self.TEXT_DARK,
            height=36, corner_radius=6, command=self._on_reset_profile,
        )
        self.reset_profile_btn.grid(row=0, column=1)

    def _build_password_section(self, parent: ctk.CTkScrollableFrame) -> None:
        password_section = ctk.CTkFrame(parent, fg_color=self.WHITE, corner_radius=8)
        password_section.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        password_section.grid_columnconfigure((0, 1, 2), weight=1)

        pass_sec_title = ctk.CTkLabel(
            password_section, text="Change Password", font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.TEXT_DARK,
        )
        pass_sec_title.grid(row=0, column=0, columnspan=3, padx=24, pady=(20, 15), sticky="w")

        pass_fields = [("Current Password", 0), ("New Password", 1), ("Confirm Password", 2)]

        for label_text, c in pass_fields:
            f_frame = ctk.CTkFrame(password_section, fg_color="transparent")
            f_frame.grid(row=1, column=c, padx=24, pady=10, sticky="ew")
            f_frame.grid_columnconfigure(0, weight=1)

            lbl = ctk.CTkLabel(
                f_frame, text=label_text, font=ctk.CTkFont(size=13, weight="normal"),
                text_color=self.TEXT_GRAY,
            )
            lbl.grid(row=0, column=0, sticky="w", pady=(0, 5))

            entry = ctk.CTkEntry(
                f_frame, show="•", height=40, fg_color=self.WHITE, border_color=self.PANEL_BG,
                text_color=self.TEXT_DARK,
            )
            entry.grid(row=1, column=0, sticky="ew")
            setattr(self, self._PASSWORD_FIELD_ATTR[label_text], entry)

        self.change_password_btn = ctk.CTkButton(
            password_section, text="Change Password", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE,
            height=36, corner_radius=6, command=self._on_change_password,
        )
        self.change_password_btn.grid(row=2, column=2, padx=24, pady=(15, 20), sticky="e")

    def _build_system_info_section(self, parent: ctk.CTkScrollableFrame) -> None:
        sys_section = ctk.CTkFrame(parent, fg_color="transparent")
        sys_section.grid(row=2, column=0, pady=(0, 20), sticky="ew")

        sys_sec_title = ctk.CTkLabel(
            sys_section, text="System Information", font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.TEXT_DARK,
        )
        sys_sec_title.grid(row=0, column=0, columnspan=5, pady=(0, 12), sticky="w")

        for i in range(5):
            sys_section.grid_columnconfigure(i, weight=1, uniform="sys_equal")

        card_titles = ["Application Name", "Version", "Developer", "Database", "Status"]

        for idx, title in enumerate(card_titles):
            card_box = ctk.CTkFrame(sys_section, fg_color=self.WHITE, height=85, corner_radius=8)
            card_box.grid(
                row=1, column=idx,
                padx=(0 if idx == 0 else 8, 0 if idx == 4 else 8), sticky="ew",
            )
            card_box.grid_propagate(False)
            card_box.grid_columnconfigure(0, weight=1)

            title_lbl = ctk.CTkLabel(
                card_box, text=title, font=ctk.CTkFont(size=12, weight="normal"),
                text_color=self.TEXT_GRAY, anchor="w",
            )
            title_lbl.grid(row=0, column=0, padx=16, pady=(14, 2), sticky="ew")

            val_lbl = ctk.CTkLabel(
                card_box, text="Loading...", font=ctk.CTkFont(size=15, weight="bold"),
                text_color=self.TEXT_DARK, anchor="w",
            )
            val_lbl.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")
            self.system_info_labels[title] = val_lbl

    def _build_preferences_section(self, parent: ctk.CTkScrollableFrame) -> None:
        pref_section = ctk.CTkFrame(parent, fg_color=self.WHITE, corner_radius=8)
        pref_section.grid(row=3, column=0, pady=(0, 10), sticky="ew")
        pref_section.grid_columnconfigure(0, weight=1)

        pref_sec_title = ctk.CTkLabel(
            pref_section, text="Preferences", font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.TEXT_DARK,
        )
        pref_sec_title.grid(row=0, column=0, padx=24, pady=(20, 10), sticky="w")

        chk_frame = ctk.CTkFrame(pref_section, fg_color="transparent")
        chk_frame.grid(row=1, column=0, padx=24, pady=10, sticky="w")

        self.notifications_var = tk.BooleanVar(value=True)
        self.dark_mode_var = tk.BooleanVar(value=True)
        self.remember_login_var = tk.BooleanVar(value=True)

        cb_notif = ctk.CTkCheckBox(
            chk_frame, text="Enable Notifications", variable=self.notifications_var,
            text_color=self.TEXT_DARK, font=ctk.CTkFont(size=13), fg_color=self.PRIMARY_BLUE,
            hover_color=self.HOVER_BLUE, border_color=self.TEXT_GRAY,
        )
        cb_notif.grid(row=0, column=0, padx=(0, 30), sticky="w")

        cb_dark = ctk.CTkCheckBox(
            chk_frame, text="Enable Dark Mode", variable=self.dark_mode_var,
            text_color=self.TEXT_DARK, font=ctk.CTkFont(size=13), fg_color=self.PRIMARY_BLUE,
            hover_color=self.HOVER_BLUE, border_color=self.TEXT_GRAY,
        )
        cb_dark.grid(row=0, column=1, padx=(0, 30), sticky="w")

        cb_rem = ctk.CTkCheckBox(
            chk_frame, text="Remember Login", variable=self.remember_login_var,
            text_color=self.TEXT_DARK, font=ctk.CTkFont(size=13), fg_color=self.PRIMARY_BLUE,
            hover_color=self.HOVER_BLUE, border_color=self.TEXT_GRAY,
        )
        cb_rem.grid(row=0, column=2, sticky="w")

        self.save_preferences_btn = ctk.CTkButton(
            pref_section, text="Save Settings", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE,
            height=36, corner_radius=6, command=self._on_save_preferences,
        )
        self.save_preferences_btn.grid(row=2, column=0, padx=24, pady=(15, 20), sticky="e")

    # ------------------------------------------------------------------
    # Backend initialization and data loading
    # ------------------------------------------------------------------
    def _initialize_backend(self) -> None:
        """Ensure tables exist, then load profile, system info, and preferences."""
        try:
            initialize_tables()
        except Exception as exc:
            logger.exception("Failed to initialize settings tables")
            self._show_message_dialog(
                "Startup Error", f"Database initialization failed.\n{exc}", False
            )
            return
        self._load_profile_data()
        self._load_system_information()
        self._load_preferences()

    def _load_profile_data(self) -> None:
        try:
            profile = get_admin_profile()
        except Exception as exc:
            logger.exception("Unable to load admin profile")
            self._show_message_dialog("Load Error", f"Could not load profile data.\n{exc}", False)
            return
        self._set_entry_value(self.full_name_entry, profile["full_name"])
        self._set_entry_value(self.username_entry, profile["username"])
        self._set_entry_value(self.email_entry, profile["email"])
        self._set_entry_value(self.phone_entry, profile["phone"])
        self.user_profile_label.configure(text=profile["full_name"])

    def _load_system_information(self) -> None:
        try:
            info = get_system_information()
            backup_info = backup_database_info()
            status = get_database_status()
        except Exception:
            logger.exception("Failed to load system information")
            info = {"app_name": "Unknown", "version": "Unknown", "developer": "Unknown"}
            backup_info = {"engine": "Unknown"}
            status = "Inactive"

        values = {
            "Application Name": info["app_name"],
            "Version": info["version"],
            "Developer": info["developer"],
            "Database": backup_info["engine"],
            "Status": status,
        }
        for title, label in self.system_info_labels.items():
            label.configure(text=values.get(title, "N/A"))

        status_label = self.system_info_labels.get("Status")
        if status_label is not None:
            color = self.SUCCESS_GREEN if values["Status"] == "Active" else self.ERROR_RED
            status_label.configure(text_color=color)

    def _load_preferences(self) -> None:
        try:
            prefs = get_preferences()
        except Exception:
            logger.exception("Failed to load preferences")
            return
        self.notifications_var.set(prefs["enable_notifications"])
        self.dark_mode_var.set(prefs["enable_dark_mode"])
        self.remember_login_var.set(prefs["remember_login"])

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_update_profile(self) -> None:
        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not all([full_name, username, email, phone]):
            self._show_message_dialog("Validation Error", "All fields are required.", False)
            return
        if not self._EMAIL_PATTERN.match(email):
            self._show_message_dialog("Validation Error", "Enter a valid email address.", False)
            return
        if not self._PHONE_PATTERN.match(phone):
            self._show_message_dialog("Validation Error", "Enter a valid phone number.", False)
            return

        buttons = [self.update_profile_btn, self.reset_profile_btn]
        self._set_widgets_state(buttons, "disabled")
        self.update_idletasks()
        try:
            update_admin_profile(full_name, username, email, phone)
            self.user_profile_label.configure(text=full_name)
            self._show_message_dialog("Success", "Profile updated successfully.", True)
        except Exception as exc:
            logger.exception("Failed to update profile")
            self._show_message_dialog("Update Failed", str(exc), False)
        finally:
            self._set_widgets_state(buttons, "normal")

    def _on_reset_profile(self) -> None:
        self._load_profile_data()

    def _on_change_password(self) -> None:
        current = self.current_password_entry.get()
        new = self.new_password_entry.get()
        confirm = self.confirm_password_entry.get()

        if not all([current, new, confirm]):
            self._show_message_dialog(
                "Validation Error", "All password fields are required.", False
            )
            return
        if new != confirm:
            self._show_message_dialog(
                "Validation Error", "New password and confirmation do not match.", False
            )
            return

        self._set_widgets_state([self.change_password_btn], "disabled")
        self.update_idletasks()
        try:
            change_password(current, new)
            self._clear_password_fields()
            self._show_message_dialog("Success", "Password changed successfully.", True)
        except Exception as exc:
            logger.exception("Failed to change password")
            self._show_message_dialog("Change Failed", str(exc), False)
        finally:
            self._set_widgets_state([self.change_password_btn], "normal")

    def _on_save_preferences(self) -> None:
        self._set_widgets_state([self.save_preferences_btn], "disabled")
        self.update_idletasks()
        try:
            update_preferences(
                self.notifications_var.get(),
                self.dark_mode_var.get(),
                self.remember_login_var.get(),
            )
            self._show_message_dialog("Success", "Preferences saved successfully.", True)
        except Exception as exc:
            logger.exception("Failed to save preferences")
            self._show_message_dialog("Save Failed", str(exc), False)
        finally:
            self._set_widgets_state([self.save_preferences_btn], "normal")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _set_entry_value(entry: ctk.CTkEntry, value: str) -> None:
        entry.delete(0, "end")
        entry.insert(0, value)

    def _clear_password_fields(self) -> None:
        for entry in (
            self.current_password_entry,
            self.new_password_entry,
            self.confirm_password_entry,
        ):
            entry.delete(0, "end")

    @staticmethod
    def _set_widgets_state(widgets: List[ctk.CTkButton], state: str) -> None:
        for widget in widgets:
            widget.configure(state=state)

    def _show_message_dialog(self, title: str, message: str, success: bool) -> None:
        """Display a modal CTkToplevel dialog for success/error feedback."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("360x180")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.WHITE)
        dialog.grid_columnconfigure(0, weight=1)
        dialog.transient(self.winfo_toplevel())

        accent = self.SUCCESS_GREEN if success else self.ERROR_RED
        icon_text = "✓" if success else "✕"

        icon_label = ctk.CTkLabel(
            dialog, text=icon_text, font=ctk.CTkFont(size=28, weight="bold"), text_color=accent,
        )
        icon_label.grid(row=0, column=0, pady=(24, 8))

        msg_label = ctk.CTkLabel(
            dialog, text=message, font=ctk.CTkFont(size=13), text_color=self.TEXT_DARK,
            wraplength=300, justify="center",
        )
        msg_label.grid(row=1, column=0, padx=20, pady=(0, 16))

        ok_btn = ctk.CTkButton(
            dialog, text="OK", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=self.PRIMARY_BLUE, hover_color=self.HOVER_BLUE, text_color=self.WHITE,
            height=36, corner_radius=6, width=100, command=dialog.destroy,
        )
        ok_btn.grid(row=2, column=0, pady=(0, 20))

        # Delay grab_set until the toplevel is actually mapped to avoid
        # "grab failed: window not viewable" errors on some platforms.
        dialog.after(50, dialog.grab_set)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x700")
    page = SettingsPage(root)
    page.pack(fill="both", expand=True)
    root.mainloop()