"""
constants.py
------------
Single source of truth for every constant in Flipodoro.
No magic numbers anywhere else in the codebase.
"""

from typing import Final

# Application identity
APP_NAME: Final[str] = "Flipodoro"
APP_VERSION: Final[str] = "1.0.0"
APP_AUTHOR: Final[str] = "Your Name"

# Default durations (minutes)
DEFAULT_STUDY_MINUTES: Final[int] = 25
DEFAULT_SHORT_BREAK_MINUTES: Final[int] = 5
DEFAULT_LONG_BREAK_MINUTES: Final[int] = 15
DEFAULT_SESSIONS_BEFORE_LONG_BREAK: Final[int] = 4

# Duration constraints (minutes)
MIN_DURATION_MINUTES: Final[int] = 1
MAX_DURATION_MINUTES: Final[int] = 120
MIN_SESSIONS_BEFORE_LONG_BREAK: Final[int] = 1
MAX_SESSIONS_BEFORE_LONG_BREAK: Final[int] = 10

# Timer tick interval (milliseconds)
TICK_INTERVAL_MS: Final[int] = 500

# Session type identifiers
SESSION_STUDY: Final[str] = "study"
SESSION_SHORT_BREAK: Final[str] = "short_break"
SESSION_LONG_BREAK: Final[str] = "long_break"

# Settings
SETTINGS_FILENAME: Final[str] = "flipodoro_settings.json"

# Window dimensions
WINDOW_MIN_WIDTH: Final[int] = 480
WINDOW_MIN_HEIGHT: Final[int] = 380
WINDOW_DEFAULT_WIDTH: Final[int] = 520
WINDOW_DEFAULT_HEIGHT: Final[int] = 420
COMPACT_MIN_WIDTH: Final[int] = 280
COMPACT_MIN_HEIGHT: Final[int] = 200

# Minibar (minimized pinned window)
MINIBAR_WIDTH: Final[int] = 300
MINIBAR_HEIGHT: Final[int] = 36
SETTINGS_WINDOW_WIDTH: Final[int] = 420
SETTINGS_WINDOW_HEIGHT: Final[int] = 480

# Focus mode
FOCUS_MODE_EXIT_KEY: Final[str] = "<Escape>"

# Always-on-top
DEFAULT_ALWAYS_ON_TOP: Final[bool] = False

# Minimal animation
DEFAULT_MINIMAL_ANIMATION: Final[bool] = False

# Autostart next session
DEFAULT_AUTOSTART: Final[bool] = False