"""
settings_view.py
----------------
Settings modal window.
"""

import tkinter as tk
from tkinter import messagebox
from flipodoro.core.settings import Settings
from flipodoro.core.constants import (
    MIN_DURATION_MINUTES,
    MAX_DURATION_MINUTES,
    MIN_SESSIONS_BEFORE_LONG_BREAK,
    MAX_SESSIONS_BEFORE_LONG_BREAK,
    APP_NAME,
    APP_VERSION,
)
from flipodoro.ui.theme import PALETTE, TYPOGRAPHY, SPACING


SETTINGS_WIDTH = 460
SETTINGS_HEIGHT = 620


class SettingsView(tk.Toplevel):

    def __init__(self, parent, settings, on_save, pinned=False):
        super().__init__(parent)

        self._settings = settings
        self._on_save_callback = on_save
        self._pinned = pinned

        self.title(APP_NAME + " - Settings")
        self.resizable(False, False)
        self.configure(bg=PALETTE.bg_primary)
        self.grab_set()

        self._position_on_parent(parent)
        self._build_ui()
        self._populate_values()

    def _position_on_parent(self, parent):
        self.geometry(f"{SETTINGS_WIDTH}x{SETTINGS_HEIGHT}")
        self.update_idletasks()
        if self._pinned:
            x = parent.winfo_x() + parent.winfo_width() + 8
            y = parent.winfo_y()
        else:
            x = parent.winfo_x() + (parent.winfo_width() - SETTINGS_WIDTH) // 2
            y = parent.winfo_y() + (parent.winfo_height() - SETTINGS_HEIGHT) // 2
        self.geometry(f"{SETTINGS_WIDTH}x{SETTINGS_HEIGHT}+{x}+{y}")

    def _build_ui(self):
        # ============ FOOTER FIRST (packed to bottom so it's always visible) ============
        footer = tk.Frame(self, bg=PALETTE.bg_secondary, height=70)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)

        # Save button - big and obvious
        save_btn = tk.Button(
            footer,
            text="Save",
            font=(TYPOGRAPHY.family_body, 12, TYPOGRAPHY.weight_bold),
            bd=0,
            relief=tk.FLAT,
            fg="#ffffff",
            bg=PALETTE.accent_study,
            activeforeground="#ffffff",
            activebackground=PALETTE.btn_primary_hover,
            cursor="hand2",
            padx=30,
            pady=10,
            command=self._on_save,
        )
        save_btn.pack(side=tk.RIGHT, padx=(0, 20), pady=15)

        # Cancel button
        cancel_btn = tk.Button(
            footer,
            text="Cancel",
            font=(TYPOGRAPHY.family_body, 11),
            bd=1,
            relief=tk.SOLID,
            fg=PALETTE.text_primary,
            bg=PALETTE.bg_secondary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_tertiary,
            highlightthickness=0,
            cursor="hand2",
            padx=18,
            pady=8,
            command=self.destroy,
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=15)

        # Restore defaults button
        restore_btn = tk.Button(
            footer,
            text="Restore Defaults",
            font=(TYPOGRAPHY.family_body, 10),
            bd=0,
            relief=tk.FLAT,
            fg=PALETTE.text_secondary,
            bg=PALETTE.bg_secondary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_secondary,
            cursor="hand2",
            command=self._on_restore_defaults,
        )
        restore_btn.pack(side=tk.LEFT, padx=20, pady=15)

        # ============ HEADER ============
        header = tk.Frame(self, bg=PALETTE.bg_secondary, pady=SPACING.md)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Settings",
            font=(
                TYPOGRAPHY.family_display,
                TYPOGRAPHY.size_heading,
                TYPOGRAPHY.weight_bold,
            ),
            fg=PALETTE.text_primary,
            bg=PALETTE.bg_secondary,
        ).pack(padx=SPACING.lg)

        # ============ BODY (fills remaining space between header and footer) ============
        body = tk.Frame(
            self,
            bg=PALETTE.bg_primary,
            padx=SPACING.lg,
            pady=SPACING.lg,
        )
        body.pack(fill=tk.BOTH, expand=True)

        # Timer durations
        self._make_section_label(body, "TIMER DURATIONS")

        self._study_var = self._make_spinner_row(
            body, "Focus duration (minutes)",
            MIN_DURATION_MINUTES, MAX_DURATION_MINUTES,
        )
        self._short_break_var = self._make_spinner_row(
            body, "Short break (minutes)",
            MIN_DURATION_MINUTES, MAX_DURATION_MINUTES,
        )
        self._long_break_var = self._make_spinner_row(
            body, "Long break (minutes)",
            MIN_DURATION_MINUTES, MAX_DURATION_MINUTES,
        )

        tk.Frame(body, bg=PALETTE.border, height=1).pack(
            fill=tk.X, pady=SPACING.md
        )

        # Session settings
        self._make_section_label(body, "SESSION SETTINGS")

        self._sessions_var = self._make_spinner_row(
            body, "Sessions before long break",
            MIN_SESSIONS_BEFORE_LONG_BREAK,
            MAX_SESSIONS_BEFORE_LONG_BREAK,
        )

        self._autostart_var = self._make_checkbox_row(
            body, "Auto-start next session",
        )

        tk.Frame(body, bg=PALETTE.border, height=1).pack(
            fill=tk.X, pady=SPACING.md
        )

        # Sound
        self._make_section_label(body, "SOUND")

        self._sound_var = self._make_checkbox_row(
            body, "Play sound on session complete",
        )

        tk.Frame(body, bg=PALETTE.border, height=1).pack(
            fill=tk.X, pady=SPACING.md
        )

        # Display
        self._make_section_label(body, "DISPLAY")

        self._always_on_top_var = self._make_checkbox_row(
            body, "Always on top",
        )

        self._minimal_animation_var = self._make_checkbox_row(
            body, "Minimal animation (no flip)",
        )

        # Version
        tk.Label(
            body,
            text=APP_NAME + " v" + APP_VERSION,
            font=(TYPOGRAPHY.family_body, 9),
            fg=PALETTE.text_muted,
            bg=PALETTE.bg_primary,
        ).pack(anchor=tk.W, pady=(SPACING.md, 0))

    def _make_section_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=(
                TYPOGRAPHY.family_body,
                9,
                TYPOGRAPHY.weight_bold,
            ),
            fg=PALETTE.text_muted,
            bg=PALETTE.bg_primary,
        ).pack(anchor=tk.W, pady=(0, SPACING.xs))

    def _make_spinner_row(self, parent, label, min_val, max_val):
        row = tk.Frame(parent, bg=PALETTE.bg_primary)
        row.pack(fill=tk.X, pady=(0, SPACING.sm))

        tk.Label(
            row,
            text=label,
            font=(TYPOGRAPHY.family_body, 11),
            fg=PALETTE.text_primary,
            bg=PALETTE.bg_primary,
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        var = tk.IntVar()
        tk.Spinbox(
            row,
            from_=min_val,
            to=max_val,
            textvariable=var,
            width=5,
            font=(TYPOGRAPHY.family_body, 11),
            bg=PALETTE.bg_input,
            fg=PALETTE.text_primary,
            buttonbackground=PALETTE.bg_tertiary,
            insertbackground=PALETTE.text_primary,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightcolor=PALETTE.border_focus,
            highlightbackground=PALETTE.border,
        ).pack(side=tk.RIGHT, padx=(SPACING.sm, 0))

        return var

    def _make_checkbox_row(self, parent, label):
        row = tk.Frame(parent, bg=PALETTE.bg_primary)
        row.pack(fill=tk.X, pady=(0, SPACING.sm))

        var = tk.BooleanVar()

        tk.Label(
            row,
            text=label,
            font=(TYPOGRAPHY.family_body, 11),
            fg=PALETTE.text_primary,
            bg=PALETTE.bg_primary,
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Checkbutton(
            row,
            variable=var,
            bg=PALETTE.bg_primary,
            activebackground=PALETTE.bg_primary,
            selectcolor=PALETTE.bg_tertiary,
            relief=tk.FLAT,
        ).pack(side=tk.RIGHT)

        return var

    def _populate_values(self):
        self._study_var.set(self._settings.study_minutes)
        self._short_break_var.set(self._settings.short_break_minutes)
        self._long_break_var.set(self._settings.long_break_minutes)
        self._sessions_var.set(self._settings.sessions_before_long_break)
        self._sound_var.set(self._settings.sound_enabled)
        self._always_on_top_var.set(self._settings.always_on_top)
        self._minimal_animation_var.set(self._settings.minimal_animation)
        self._autostart_var.set(self._settings.autostart)

    def _on_save(self):
        try:
            study = int(self._study_var.get())
            short_b = int(self._short_break_var.get())
            long_b = int(self._long_break_var.get())
            sessions = int(self._sessions_var.get())
        except (tk.TclError, ValueError):
            messagebox.showerror(
                "Invalid Settings",
                "Please enter valid numbers.",
                parent=self,
            )
            return

        self._settings.study_minutes = study
        self._settings.short_break_minutes = short_b
        self._settings.long_break_minutes = long_b
        self._settings.sessions_before_long_break = sessions
        self._settings.sound_enabled = self._sound_var.get()
        self._settings.always_on_top = self._always_on_top_var.get()
        self._settings.minimal_animation = self._minimal_animation_var.get()
        self._settings.autostart = self._autostart_var.get()
        self._settings.save()
        self._on_save_callback()
        self.destroy()

    def _on_restore_defaults(self):
        self._settings.reset_to_defaults()
        self._populate_values()