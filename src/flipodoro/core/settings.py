"""
settings.py
-----------
Settings model with JSON persistence.
Saves to %APPDATA%/Flipodoro/ on Windows.
"""

import json
import os
import logging
from typing import Any
from flipodoro.core.constants import (
    APP_NAME,
    SETTINGS_FILENAME,
    DEFAULT_STUDY_MINUTES,
    DEFAULT_SHORT_BREAK_MINUTES,
    DEFAULT_LONG_BREAK_MINUTES,
    DEFAULT_SESSIONS_BEFORE_LONG_BREAK,
    DEFAULT_ALWAYS_ON_TOP,
    DEFAULT_MINIMAL_ANIMATION,
    MIN_DURATION_MINUTES,
    MAX_DURATION_MINUTES,
    MIN_SESSIONS_BEFORE_LONG_BREAK,
    MAX_SESSIONS_BEFORE_LONG_BREAK,
)

logger = logging.getLogger(__name__)


class Settings:

    def __init__(self) -> None:
        self._study_minutes: int = DEFAULT_STUDY_MINUTES
        self._short_break_minutes: int = DEFAULT_SHORT_BREAK_MINUTES
        self._long_break_minutes: int = DEFAULT_LONG_BREAK_MINUTES
        self._sessions_before_long_break: int = DEFAULT_SESSIONS_BEFORE_LONG_BREAK
        self._sound_enabled: bool = True
        self._always_on_top: bool = DEFAULT_ALWAYS_ON_TOP
        self._minimal_animation: bool = DEFAULT_MINIMAL_ANIMATION
        self.load()

    @property
    def study_minutes(self) -> int:
        return self._study_minutes

    @study_minutes.setter
    def study_minutes(self, value: int) -> None:
        self._study_minutes = self._clamp_duration(value)

    @property
    def short_break_minutes(self) -> int:
        return self._short_break_minutes

    @short_break_minutes.setter
    def short_break_minutes(self, value: int) -> None:
        self._short_break_minutes = self._clamp_duration(value)

    @property
    def long_break_minutes(self) -> int:
        return self._long_break_minutes

    @long_break_minutes.setter
    def long_break_minutes(self, value: int) -> None:
        self._long_break_minutes = self._clamp_duration(value)

    @property
    def sessions_before_long_break(self) -> int:
        return self._sessions_before_long_break

    @sessions_before_long_break.setter
    def sessions_before_long_break(self, value: int) -> None:
        self._sessions_before_long_break = max(
            MIN_SESSIONS_BEFORE_LONG_BREAK,
            min(MAX_SESSIONS_BEFORE_LONG_BREAK, int(value)),
        )

    @property
    def sound_enabled(self) -> bool:
        return self._sound_enabled

    @sound_enabled.setter
    def sound_enabled(self, value: bool) -> None:
        self._sound_enabled = bool(value)

    @property
    def always_on_top(self) -> bool:
        return self._always_on_top

    @always_on_top.setter
    def always_on_top(self, value: bool) -> None:
        self._always_on_top = bool(value)

    @property
    def minimal_animation(self) -> bool:
        return self._minimal_animation

    @minimal_animation.setter
    def minimal_animation(self, value: bool) -> None:
        self._minimal_animation = bool(value)

    def load(self) -> None:
        path = self._settings_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)
            self._apply(data)
        except (json.JSONDecodeError, OSError, TypeError) as exc:
            logger.warning("Could not load settings (%s). Using defaults.", exc)

    def save(self) -> None:
        path = self._settings_path()
        directory = os.path.dirname(path)
        try:
            os.makedirs(directory, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._to_dict(), f, indent=2)
        except OSError as exc:
            logger.error("Could not save settings: %s", exc)

    def reset_to_defaults(self) -> None:
        self._study_minutes = DEFAULT_STUDY_MINUTES
        self._short_break_minutes = DEFAULT_SHORT_BREAK_MINUTES
        self._long_break_minutes = DEFAULT_LONG_BREAK_MINUTES
        self._sessions_before_long_break = DEFAULT_SESSIONS_BEFORE_LONG_BREAK
        self._sound_enabled = True
        self._always_on_top = DEFAULT_ALWAYS_ON_TOP
        self._minimal_animation = DEFAULT_MINIMAL_ANIMATION

    def _apply(self, data: dict[str, Any]) -> None:
        if "study_minutes" in data:
            self.study_minutes = data["study_minutes"]
        if "short_break_minutes" in data:
            self.short_break_minutes = data["short_break_minutes"]
        if "long_break_minutes" in data:
            self.long_break_minutes = data["long_break_minutes"]
        if "sessions_before_long_break" in data:
            self.sessions_before_long_break = data["sessions_before_long_break"]
        if "sound_enabled" in data:
            self.sound_enabled = data["sound_enabled"]
        if "always_on_top" in data:
            self.always_on_top = data["always_on_top"]
        if "minimal_animation" in data:
            self.minimal_animation = data["minimal_animation"]

    def _to_dict(self) -> dict[str, Any]:
        return {
            "study_minutes": self._study_minutes,
            "short_break_minutes": self._short_break_minutes,
            "long_break_minutes": self._long_break_minutes,
            "sessions_before_long_break": self._sessions_before_long_break,
            "sound_enabled": self._sound_enabled,
            "always_on_top": self._always_on_top,
            "minimal_animation": self._minimal_animation,
        }

    @staticmethod
    def _settings_path() -> str:
        app_data = os.environ.get("APPDATA") or os.path.expanduser("~/.config")
        return os.path.join(app_data, APP_NAME, SETTINGS_FILENAME)

    @staticmethod
    def _clamp_duration(value: Any) -> int:
        try:
            return max(MIN_DURATION_MINUTES, min(MAX_DURATION_MINUTES, int(value)))
        except (TypeError, ValueError):
            return DEFAULT_STUDY_MINUTES