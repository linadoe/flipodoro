"""Tests for settings window opening beside the main window when pinned."""

import tkinter as tk

import pytest

from flipodoro.ui.settings_view import SettingsView, SETTINGS_WIDTH, SETTINGS_HEIGHT
from flipodoro.core.settings import Settings


class TestSettingsPositionBeside:

    def test_when_pinned_opens_to_the_right(self, tk_root):
        tk_root.geometry("520x420+100+100")
        tk_root.update_idletasks()
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = True
        settings._minimal_animation = False

        sv = SettingsView(
            parent=tk_root,
            settings=settings,
            on_save=lambda: None,
            pinned=True,
        )
        sv.update_idletasks()

        sx = sv.winfo_x()
        parent_right = tk_root.winfo_x() + tk_root.winfo_width()
        assert sx >= parent_right - 10, (
            f"Settings x={sx} should be near parent right edge {parent_right}"
        )
        sv.destroy()

    def test_when_not_pinned_centers_on_parent(self, tk_root):
        tk_root.geometry("520x420+200+200")
        tk_root.update_idletasks()
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = False
        settings._minimal_animation = False

        sv = SettingsView(
            parent=tk_root,
            settings=settings,
            on_save=lambda: None,
            pinned=False,
        )
        sv.update_idletasks()

        expected_x = 200 + (520 - SETTINGS_WIDTH) // 2
        sx = sv.winfo_x()
        assert abs(sx - expected_x) < 20, (
            f"Settings x={sx} should be near center {expected_x}"
        )
        sv.destroy()
