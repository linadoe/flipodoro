import time
from enum import Enum, auto
from typing import Callable, Optional
from flipodoro.core.constants import (
    DEFAULT_STUDY_MINUTES,
    DEFAULT_SHORT_BREAK_MINUTES,
    DEFAULT_LONG_BREAK_MINUTES,
    DEFAULT_SESSIONS_BEFORE_LONG_BREAK,
    SESSION_STUDY,
    SESSION_SHORT_BREAK,
    SESSION_LONG_BREAK,
)


class TimerState(Enum):
    IDLE = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()


class PomodoroTimer:

    def __init__(
        self,
        study_minutes=DEFAULT_STUDY_MINUTES,
        short_break_minutes=DEFAULT_SHORT_BREAK_MINUTES,
        long_break_minutes=DEFAULT_LONG_BREAK_MINUTES,
        sessions_before_long_break=DEFAULT_SESSIONS_BEFORE_LONG_BREAK,
    ):
        self._study_minutes = study_minutes
        self._short_break_minutes = short_break_minutes
        self._long_break_minutes = long_break_minutes
        self._sessions_before_long_break = sessions_before_long_break

        self._completed_study_sessions = 0
        self._current_session_type = SESSION_STUDY

        self._state = TimerState.IDLE
        self._total_seconds = self._duration_for_session(SESSION_STUDY)
        self._remaining_seconds = self._total_seconds

        self._start_wall_time = None
        self._remaining_at_last_start = self._remaining_seconds

        self._on_tick = None
        self._on_complete = None
        self._on_state_change = None

    def update_durations(
        self,
        study_minutes,
        short_break_minutes,
        long_break_minutes,
        sessions_before_long_break,
    ):
        old_current_duration = self._duration_for_session(self._current_session_type)

        self._study_minutes = study_minutes
        self._short_break_minutes = short_break_minutes
        self._long_break_minutes = long_break_minutes
        self._sessions_before_long_break = sessions_before_long_break

        new_current_duration = self._duration_for_session(self._current_session_type)

        if old_current_duration != new_current_duration or self._state == TimerState.IDLE:
            self._start_wall_time = None
            self._state = TimerState.IDLE
            self._total_seconds = new_current_duration
            self._remaining_seconds = new_current_duration
            self._remaining_at_last_start = new_current_duration
            self._notify_state_change()
            self._notify_tick()
        else:
            self._total_seconds = new_current_duration

    def set_on_tick(self, callback):
        self._on_tick = callback

    def set_on_complete(self, callback):
        self._on_complete = callback

    def set_on_state_change(self, callback):
        self._on_state_change = callback

    def start(self):
        if self._state in (TimerState.IDLE, TimerState.PAUSED):
            self._start_wall_time = time.monotonic()
            self._remaining_at_last_start = self._remaining_seconds
            self._state = TimerState.RUNNING
            self._notify_state_change()

    def pause(self):
        if self._state == TimerState.RUNNING:
            self._remaining_seconds = self._compute_remaining()
            self._start_wall_time = None
            self._state = TimerState.PAUSED
            self._notify_state_change()
            self._notify_tick()

    def reset(self):
        self._start_wall_time = None
        self._state = TimerState.IDLE
        self._total_seconds = self._duration_for_session(self._current_session_type)
        self._remaining_seconds = self._total_seconds
        self._remaining_at_last_start = self._total_seconds
        self._notify_state_change()
        self._notify_tick()

    def skip(self):
        self._advance_session()

    def tick(self):
        if self._state != TimerState.RUNNING:
            return
        self._remaining_seconds = self._compute_remaining()
        self._notify_tick()
        if self._remaining_seconds <= 0:
            self._remaining_seconds = 0
            self._complete_session()

    def set_session_type(self, session_type):
        valid_types = {SESSION_STUDY, SESSION_SHORT_BREAK, SESSION_LONG_BREAK}
        if session_type not in valid_types:
            raise ValueError("Invalid session type")
        if self._state != TimerState.IDLE:
            return

        self._current_session_type = session_type
        self._total_seconds = self._duration_for_session(session_type)
        self._remaining_seconds = self._total_seconds
        self._remaining_at_last_start = self._total_seconds
        self._notify_tick()

    @property
    def state(self):
        return self._state

    @property
    def remaining_seconds(self):
        return max(0, self._remaining_seconds)

    @property
    def total_seconds(self):
        return self._total_seconds

    @property
    def current_session_type(self):
        return self._current_session_type

    @property
    def completed_study_sessions(self):
        return self._completed_study_sessions

    @property
    def progress(self):
        if self._total_seconds == 0:
            return 0.0
        elapsed = self._total_seconds - self.remaining_seconds
        return min(1.0, max(0.0, elapsed / self._total_seconds))

    def _compute_remaining(self):
        if self._start_wall_time is None:
            return self._remaining_seconds
        elapsed = time.monotonic() - self._start_wall_time
        return max(0, self._remaining_at_last_start - int(elapsed))

    def _complete_session(self):
        completed_type = self._current_session_type
        self._state = TimerState.COMPLETED
        self._notify_state_change()
        if self._on_complete:
            self._on_complete(completed_type)
        self._advance_session()

    def _advance_session(self):
        if self._current_session_type == SESSION_STUDY:
            self._completed_study_sessions += 1
            if self._completed_study_sessions % self._sessions_before_long_break == 0:
                next_session = SESSION_LONG_BREAK
            else:
                next_session = SESSION_SHORT_BREAK
        else:
            next_session = SESSION_STUDY

        self._current_session_type = next_session
        self._total_seconds = self._duration_for_session(next_session)
        self._remaining_seconds = self._total_seconds
        self._remaining_at_last_start = self._total_seconds
        self._start_wall_time = None
        self._state = TimerState.IDLE
        self._notify_state_change()
        self._notify_tick()

    def _duration_for_session(self, session_type):
        durations = {
            SESSION_STUDY: self._study_minutes * 60,
            SESSION_SHORT_BREAK: self._short_break_minutes * 60,
            SESSION_LONG_BREAK: self._long_break_minutes * 60,
        }
        return durations.get(session_type, self._study_minutes * 60)

    def _notify_tick(self):
        if self._on_tick:
            self._on_tick(self.remaining_seconds, self._total_seconds)

    def _notify_state_change(self):
        if self._on_state_change:
            self._on_state_change(self._state)