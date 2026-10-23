"""Tests for the always-on-top toggle feature."""

import tkinter as tk

from flipodoro.core.settings import Settings
from flipodoro.core.constants import DEFAULT_ALWAYS_ON_TOP


class TestAlwaysOnTopSetting:

    def test_default_is_false(self):
        settings = Settings.__new__(Settings)
        settings._always_on_top = DEFAULT_ALWAYS_ON_TOP
        assert settings.always_on_top is False

    def test_setter_stores_bool(self):
        settings = Settings.__new__(Settings)
        settings._always_on_top = False
        settings.always_on_top = True
        assert settings.always_on_top is True

    def test_setter_coerces_truthy(self):
        settings = Settings.__new__(Settings)
        settings._always_on_top = False
        settings.always_on_top = 1
        assert settings.always_on_top is True

    def test_persists_in_dict(self):
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = True
        settings._minimal_animation = False
        d = settings._to_dict()
        assert "always_on_top" in d
        assert d["always_on_top"] is True

    def test_loads_from_dict(self):
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = False
        settings._minimal_animation = False
        settings._apply({"always_on_top": True})
        assert settings.always_on_top is True

    def test_reset_to_defaults_clears_flag(self):
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = True
        settings._minimal_animation = False
        settings.reset_to_defaults()
        assert settings.always_on_top is False


class TestAlwaysOnTopWindow:

    def test_topmost_attribute_applied(self, tk_root):
        tk_root.attributes("-topmost", True)
        assert tk_root.attributes("-topmost")

    def test_topmost_attribute_removed(self, tk_root):
        tk_root.attributes("-topmost", True)
        tk_root.attributes("-topmost", False)
        assert not tk_root.attributes("-topmost")
