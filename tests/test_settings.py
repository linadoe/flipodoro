"""Tests for Settings persistence and validation."""

import json
import os
import tempfile
from unittest.mock import patch

from flipodoro.core.settings import Settings
from flipodoro.core.constants import (
    DEFAULT_STUDY_MINUTES,
    DEFAULT_SHORT_BREAK_MINUTES,
    DEFAULT_LONG_BREAK_MINUTES,
    DEFAULT_SESSIONS_BEFORE_LONG_BREAK,
    MIN_DURATION_MINUTES,
    MAX_DURATION_MINUTES,
    MIN_SESSIONS_BEFORE_LONG_BREAK,
    MAX_SESSIONS_BEFORE_LONG_BREAK,
)


def _make_settings_no_load():
    """Create a Settings instance without triggering load() from disk."""
    s = Settings.__new__(Settings)
    s._study_minutes = DEFAULT_STUDY_MINUTES
    s._short_break_minutes = DEFAULT_SHORT_BREAK_MINUTES
    s._long_break_minutes = DEFAULT_LONG_BREAK_MINUTES
    s._sessions_before_long_break = DEFAULT_SESSIONS_BEFORE_LONG_BREAK
    s._sound_enabled = True
    s._always_on_top = False
    s._minimal_animation = False
    s._autostart = False
    return s


class TestDefaults:

    def test_default_study(self):
        s = _make_settings_no_load()
        assert s.study_minutes == DEFAULT_STUDY_MINUTES

    def test_default_short_break(self):
        s = _make_settings_no_load()
        assert s.short_break_minutes == DEFAULT_SHORT_BREAK_MINUTES

    def test_default_long_break(self):
        s = _make_settings_no_load()
        assert s.long_break_minutes == DEFAULT_LONG_BREAK_MINUTES

    def test_default_sessions_before_long_break(self):
        s = _make_settings_no_load()
        assert s.sessions_before_long_break == DEFAULT_SESSIONS_BEFORE_LONG_BREAK

    def test_default_sound_enabled(self):
        s = _make_settings_no_load()
        assert s.sound_enabled is True


class TestClamping:

    def test_study_below_min_clamps(self):
        s = _make_settings_no_load()
        s.study_minutes = 0
        assert s.study_minutes == MIN_DURATION_MINUTES

    def test_study_above_max_clamps(self):
        s = _make_settings_no_load()
        s.study_minutes = 999
        assert s.study_minutes == MAX_DURATION_MINUTES

    def test_short_break_clamps(self):
        s = _make_settings_no_load()
        s.short_break_minutes = -5
        assert s.short_break_minutes == MIN_DURATION_MINUTES

    def test_long_break_clamps(self):
        s = _make_settings_no_load()
        s.long_break_minutes = 200
        assert s.long_break_minutes == MAX_DURATION_MINUTES

    def test_sessions_before_long_break_below_min(self):
        s = _make_settings_no_load()
        s.sessions_before_long_break = 0
        assert s.sessions_before_long_break == MIN_SESSIONS_BEFORE_LONG_BREAK

    def test_sessions_before_long_break_above_max(self):
        s = _make_settings_no_load()
        s.sessions_before_long_break = 99
        assert s.sessions_before_long_break == MAX_SESSIONS_BEFORE_LONG_BREAK

    def test_clamp_with_invalid_type_returns_default(self):
        s = _make_settings_no_load()
        s.study_minutes = "not a number"
        assert s.study_minutes == DEFAULT_STUDY_MINUTES


class TestSerialization:

    def test_to_dict_has_all_keys(self):
        s = _make_settings_no_load()
        d = s._to_dict()
        expected_keys = {
            "study_minutes", "short_break_minutes", "long_break_minutes",
            "sessions_before_long_break", "sound_enabled",
            "always_on_top", "minimal_animation", "autostart",
        }
        assert set(d.keys()) == expected_keys

    def test_roundtrip_via_dict(self):
        s = _make_settings_no_load()
        s.study_minutes = 45
        s.short_break_minutes = 10
        s.long_break_minutes = 20
        s.sessions_before_long_break = 3
        s.sound_enabled = False

        d = s._to_dict()
        s2 = _make_settings_no_load()
        s2._apply(d)

        assert s2.study_minutes == 45
        assert s2.short_break_minutes == 10
        assert s2.long_break_minutes == 20
        assert s2.sessions_before_long_break == 3
        assert s2.sound_enabled is False

    def test_apply_ignores_unknown_keys(self):
        s = _make_settings_no_load()
        s._apply({"unknown_key": 42, "study_minutes": 30})
        assert s.study_minutes == 30


class TestPersistence:

    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "settings.json")
            with patch.object(Settings, "_settings_path", return_value=path):
                s = Settings()
                s.study_minutes = 42
                s.sound_enabled = False
                s.save()

                s2 = Settings()
                assert s2.study_minutes == 42
                assert s2.sound_enabled is False

    def test_load_missing_file_uses_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "nonexistent.json")
            with patch.object(Settings, "_settings_path", return_value=path):
                s = Settings()
                assert s.study_minutes == DEFAULT_STUDY_MINUTES

    def test_load_corrupt_json_uses_defaults(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "settings.json")
            with open(path, "w") as f:
                f.write("{corrupt json!!")
            with patch.object(Settings, "_settings_path", return_value=path):
                s = Settings()
                assert s.study_minutes == DEFAULT_STUDY_MINUTES


class TestResetDefaults:

    def test_reset_restores_all(self):
        s = _make_settings_no_load()
        s.study_minutes = 99
        s.short_break_minutes = 30
        s.long_break_minutes = 60
        s.sessions_before_long_break = 8
        s.sound_enabled = False
        s.always_on_top = True
        s.minimal_animation = True

        s.reset_to_defaults()

        assert s.study_minutes == DEFAULT_STUDY_MINUTES
        assert s.short_break_minutes == DEFAULT_SHORT_BREAK_MINUTES
        assert s.long_break_minutes == DEFAULT_LONG_BREAK_MINUTES
        assert s.sessions_before_long_break == DEFAULT_SESSIONS_BEFORE_LONG_BREAK
        assert s.sound_enabled is True
        assert s.always_on_top is False
        assert s.minimal_animation is False
