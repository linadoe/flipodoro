"""Tests for FlipClock and FlipDigit widgets."""

import pytest

from flipodoro.ui.flip_clock import (
    FlipDigit,
    FlipSeparator,
    FlipClock,
    CARD_WIDTH,
    CARD_HEIGHT,
    ANIMATION_STEPS,
)


class TestFlipDigit:

    def test_initial_char(self, tk_root):
        d = FlipDigit(tk_root, char="7")
        assert d._char == "7"

    def test_set_same_char_no_animation(self, tk_root):
        d = FlipDigit(tk_root, char="3")
        d.set_char("3")
        assert not d._animating

    def test_set_different_char_starts_animation(self, tk_root):
        d = FlipDigit(tk_root, char="0")
        d.set_char("1")
        assert d._animating

    def test_canvas_dimensions(self, tk_root):
        d = FlipDigit(tk_root)
        assert int(d.cget("width")) == CARD_WIDTH
        assert int(d.cget("height")) == CARD_HEIGHT

    def test_set_accent_updates(self, tk_root):
        d = FlipDigit(tk_root, char="0")
        d.set_accent("#ff0000")
        assert d._accent == "#ff0000"

    def test_set_accent_same_color_no_redraw(self, tk_root):
        d = FlipDigit(tk_root, char="0")
        initial_accent = d._accent
        d.set_accent(initial_accent)
        # No error, no-op


class TestFlipSeparator:

    def test_set_accent(self, tk_root):
        sep = FlipSeparator(tk_root)
        sep.set_accent("#00ff00")
        assert sep._accent == "#00ff00"


class TestFlipClock:

    def test_set_time_zero(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_time(0, 0)
        assert clock._digits[0]._char == "0"
        assert clock._digits[1]._char == "0"
        assert clock._digits[2]._char == "0"
        assert clock._digits[3]._char == "0"

    def test_set_time_25_00(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_minimal(True)
        clock.set_time(25, 0)
        assert clock._digits[0]._char == "2"
        assert clock._digits[1]._char == "5"
        assert clock._digits[2]._char == "0"
        assert clock._digits[3]._char == "0"

    def test_set_time_clamps_minutes_to_99(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_minimal(True)
        clock.set_time(150, 30)
        assert clock._digits[0]._char == "9"
        assert clock._digits[1]._char == "9"

    def test_set_time_clamps_seconds_to_59(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_minimal(True)
        clock.set_time(10, 99)
        assert clock._digits[2]._char == "5"
        assert clock._digits[3]._char == "9"

    def test_set_time_clamps_negative(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_time(-5, -10)
        assert clock._digits[0]._char == "0"
        assert clock._digits[1]._char == "0"
        assert clock._digits[2]._char == "0"
        assert clock._digits[3]._char == "0"

    def test_set_from_seconds(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_minimal(True)
        clock.set_from_seconds(90)  # 1:30
        assert clock._digits[0]._char == "0"
        assert clock._digits[1]._char == "1"
        assert clock._digits[2]._char == "3"
        assert clock._digits[3]._char == "0"

    def test_set_from_seconds_zero(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_from_seconds(0)
        for d in clock._digits:
            assert d._char == "0"

    def test_set_from_seconds_negative_clamps(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_from_seconds(-100)
        for d in clock._digits:
            assert d._char == "0"

    def test_set_accent_propagates(self, tk_root):
        clock = FlipClock(tk_root)
        clock.set_accent("#abcdef")
        for d in clock._digits:
            assert d._accent == "#abcdef"

    def test_has_four_digits(self, tk_root):
        clock = FlipClock(tk_root)
        assert len(clock._digits) == 4

    def test_has_separator(self, tk_root):
        clock = FlipClock(tk_root)
        assert clock._separator is not None
