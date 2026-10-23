"""
theme.py
--------
Every colour, font, and size in one place.
Nothing in the UI should ever contain a raw hex colour string.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    bg_primary: str = "#1a1a2e"
    bg_secondary: str = "#16213e"
    bg_tertiary: str = "#0f3460"
    bg_input: str = "#1e2a45"

    text_primary: str = "#e0e0e0"
    text_secondary: str = "#a0aec0"
    text_muted: str = "#4a5568"

    accent_study: str = "#e94560"
    accent_short_break: str = "#0f9b8e"
    accent_long_break: str = "#6c63ff"

    btn_primary_bg: str = "#e94560"
    btn_primary_fg: str = "#ffffff"
    btn_primary_hover: str = "#ff6b6b"

    btn_secondary_bg: str = "#0f3460"
    btn_secondary_fg: str = "#e0e0e0"
    btn_secondary_hover: str = "#1a4a7a"

    digit_bg: str = "#16213e"
    digit_fg: str = "#e0e0e0"

    progress_bg: str = "#0f3460"
    progress_fill: str = "#e94560"

    focus_bg: str = "#0d0d1a"

    border: str = "#0f3460"
    border_focus: str = "#e94560"


@dataclass(frozen=True)
class Typography:
    family_display: str = "Segoe UI"
    family_mono: str = "Consolas"
    family_body: str = "Segoe UI"

    size_digit_large: int = 72
    size_heading: int = 16
    size_body: int = 11
    size_label: int = 10
    size_button: int = 11
    size_session_label: int = 13

    weight_bold: str = "bold"
    weight_normal: str = "normal"


@dataclass(frozen=True)
class Spacing:
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 40
    xxl: int = 64


@dataclass(frozen=True)
class Dimensions:
    flip_card_width: int = 90
    flip_card_height: int = 100
    flip_card_radius: int = 10
    progress_bar_height: int = 4
    button_height: int = 36
    button_width_primary: int = 120
    button_width_secondary: int = 80


PALETTE = Palette()
TYPOGRAPHY = Typography()
SPACING = Spacing()
DIMENSIONS = Dimensions()


def session_accent_color(session_type: str) -> str:
    from flipodoro.core.constants import (
        SESSION_STUDY,
        SESSION_SHORT_BREAK,
        SESSION_LONG_BREAK,
    )
    mapping = {
        SESSION_STUDY: PALETTE.accent_study,
        SESSION_SHORT_BREAK: PALETTE.accent_short_break,
        SESSION_LONG_BREAK: PALETTE.accent_long_break,
    }
    return mapping.get(session_type, PALETTE.accent_study)


def session_label_text(session_type: str) -> str:
    from flipodoro.core.constants import (
        SESSION_STUDY,
        SESSION_SHORT_BREAK,
        SESSION_LONG_BREAK,
    )
    mapping = {
        SESSION_STUDY: "Focus",
        SESSION_SHORT_BREAK: "Short Break",
        SESSION_LONG_BREAK: "Long Break",
    }
    return mapping.get(session_type, "Focus")