"""Tests for theme helpers."""

from flipodoro.ui.theme import (
    PALETTE,
    TYPOGRAPHY,
    SPACING,
    DIMENSIONS,
    session_accent_color,
    session_label_text,
)
from flipodoro.core.constants import (
    SESSION_STUDY,
    SESSION_SHORT_BREAK,
    SESSION_LONG_BREAK,
)


class TestSessionAccentColor:

    def test_study_returns_accent_study(self):
        assert session_accent_color(SESSION_STUDY) == PALETTE.accent_study

    def test_short_break_returns_accent_short_break(self):
        assert session_accent_color(SESSION_SHORT_BREAK) == PALETTE.accent_short_break

    def test_long_break_returns_accent_long_break(self):
        assert session_accent_color(SESSION_LONG_BREAK) == PALETTE.accent_long_break

    def test_unknown_falls_back_to_study(self):
        assert session_accent_color("unknown") == PALETTE.accent_study


class TestSessionLabelText:

    def test_study_label(self):
        assert session_label_text(SESSION_STUDY) == "Focus"

    def test_short_break_label(self):
        assert session_label_text(SESSION_SHORT_BREAK) == "Short Break"

    def test_long_break_label(self):
        assert session_label_text(SESSION_LONG_BREAK) == "Long Break"

    def test_unknown_falls_back_to_focus(self):
        assert session_label_text("unknown") == "Focus"


class TestPaletteConsistency:

    def test_all_colors_are_hex(self):
        for field_name in PALETTE.__dataclass_fields__:
            val = getattr(PALETTE, field_name)
            assert val.startswith("#"), f"{field_name} = {val} is not a hex color"

    def test_bg_primary_is_dark(self):
        r = int(PALETTE.bg_primary[1:3], 16)
        g = int(PALETTE.bg_primary[3:5], 16)
        b = int(PALETTE.bg_primary[5:7], 16)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        assert luminance < 128, "bg_primary should be a dark color"


class TestTypography:

    def test_mono_font_set(self):
        assert TYPOGRAPHY.family_mono != ""

    def test_body_font_set(self):
        assert TYPOGRAPHY.family_body != ""


class TestSpacing:

    def test_spacing_increasing(self):
        assert SPACING.xs < SPACING.sm < SPACING.md < SPACING.lg < SPACING.xl < SPACING.xxl
