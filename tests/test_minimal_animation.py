"""Tests for visualization with minimal movement mode."""

import tkinter as tk

import pytest

from flipodoro.core.settings import Settings
from flipodoro.core.constants import DEFAULT_MINIMAL_ANIMATION
from flipodoro.ui.flip_clock import (
    FlipDigit,
    FlipClock,
    ANIMATION_STEPS,
    ANIMATION_DELAY_MS,
)


class TestMinimalAnimationSetting:

    def test_default_is_false(self):
        settings = Settings.__new__(Settings)
        settings._minimal_animation = DEFAULT_MINIMAL_ANIMATION
        assert settings.minimal_animation is False

    def test_setter_stores_bool(self):
        settings = Settings.__new__(Settings)
        settings._minimal_animation = False
        settings.minimal_animation = True
        assert settings.minimal_animation is True

    def test_persists_in_dict(self):
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = False
        settings._minimal_animation = True
        settings._autostart = False
        d = settings._to_dict()
        assert "minimal_animation" in d
        assert d["minimal_animation"] is True

    def test_loads_from_dict(self):
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = False
        settings._minimal_animation = False
        settings._autostart = False
        settings._apply({"minimal_animation": True})
        assert settings.minimal_animation is True

    def test_reset_to_defaults_clears_flag(self):
        settings = Settings.__new__(Settings)
        settings._study_minutes = 25
        settings._short_break_minutes = 5
        settings._long_break_minutes = 15
        settings._sessions_before_long_break = 4
        settings._sound_enabled = True
        settings._always_on_top = False
        settings._minimal_animation = True
        settings._autostart = False
        settings.reset_to_defaults()
        assert settings.minimal_animation is False


class TestFlipDigitMinimalMode:

    def test_static_draw_does_not_animate(self, tk_root):
        digit = FlipDigit(tk_root, char="0")
        digit.set_minimal(True)
        digit.set_char("1")
        assert not digit._animating

    def test_normal_mode_animates(self, tk_root):
        digit = FlipDigit(tk_root, char="0")
        digit.set_minimal(False)
        digit.set_char("1")
        assert digit._animating

    def test_same_char_never_animates(self, tk_root):
        digit = FlipDigit(tk_root, char="5")
        digit.set_minimal(False)
        digit.set_char("5")
        assert not digit._animating


class TestFlipClockMinimalMode:

    def test_set_minimal_propagates_to_digits(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_minimal(True)
        for d in clock._digits:
            assert d._minimal is True

    def test_set_minimal_false_by_default(self, tk_root):
        clock = FlipClock(tk_root)
        for d in clock._digits:
            assert d._minimal is False
