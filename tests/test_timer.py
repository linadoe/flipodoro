"""Tests for PomodoroTimer core logic."""

import time
from unittest.mock import MagicMock

from flipodoro.core.timer import PomodoroTimer, TimerState
from flipodoro.core.constants import (
    SESSION_STUDY,
    SESSION_SHORT_BREAK,
    SESSION_LONG_BREAK,
    DEFAULT_STUDY_MINUTES,
    DEFAULT_SHORT_BREAK_MINUTES,
    DEFAULT_LONG_BREAK_MINUTES,
    DEFAULT_SESSIONS_BEFORE_LONG_BREAK,
)


class TestTimerInit:

    def test_initial_state_is_idle(self):
        t = PomodoroTimer()
        assert t.state == TimerState.IDLE

    def test_initial_session_is_study(self):
        t = PomodoroTimer()
        assert t.current_session_type == SESSION_STUDY

    def test_initial_remaining_equals_study_duration(self):
        t = PomodoroTimer(study_minutes=25)
        assert t.remaining_seconds == 25 * 60

    def test_initial_completed_sessions_is_zero(self):
        t = PomodoroTimer()
        assert t.completed_study_sessions == 0

    def test_custom_durations(self):
        t = PomodoroTimer(study_minutes=50, short_break_minutes=10,
                          long_break_minutes=30, sessions_before_long_break=2)
        assert t.remaining_seconds == 50 * 60
        assert t.total_seconds == 50 * 60


class TestStartPauseReset:

    def test_start_changes_state_to_running(self):
        t = PomodoroTimer()
        t.start()
        assert t.state == TimerState.RUNNING

    def test_pause_changes_state_to_paused(self):
        t = PomodoroTimer()
        t.start()
        t.pause()
        assert t.state == TimerState.PAUSED

    def test_pause_when_idle_does_nothing(self):
        t = PomodoroTimer()
        t.pause()
        assert t.state == TimerState.IDLE

    def test_start_from_paused(self):
        t = PomodoroTimer()
        t.start()
        t.pause()
        t.start()
        assert t.state == TimerState.RUNNING

    def test_reset_returns_to_idle(self):
        t = PomodoroTimer()
        t.start()
        t.reset()
        assert t.state == TimerState.IDLE

    def test_reset_restores_full_duration(self):
        t = PomodoroTimer(study_minutes=25)
        t.start()
        t.reset()
        assert t.remaining_seconds == 25 * 60

    def test_start_when_already_running_stays_running(self):
        t = PomodoroTimer()
        t.start()
        t.start()
        assert t.state == TimerState.RUNNING


class TestTick:

    def test_tick_when_idle_does_nothing(self):
        t = PomodoroTimer(study_minutes=1)
        initial = t.remaining_seconds
        t.tick()
        assert t.remaining_seconds == initial

    def test_tick_decrements_remaining(self):
        t = PomodoroTimer(study_minutes=1)
        t.start()
        t._start_wall_time = time.monotonic() - 5
        t.tick()
        assert t.remaining_seconds <= 55

    def test_tick_fires_on_tick_callback(self):
        cb = MagicMock()
        t = PomodoroTimer(study_minutes=1)
        t.set_on_tick(cb)
        t.start()
        t._start_wall_time = time.monotonic() - 1
        t.tick()
        cb.assert_called()

    def test_tick_at_zero_completes_session(self):
        cb = MagicMock()
        t = PomodoroTimer(study_minutes=1)
        t.set_on_complete(cb)
        t.start()
        t._start_wall_time = time.monotonic() - 61
        t.tick()
        cb.assert_called_once_with(SESSION_STUDY)


class TestSessionCycling:

    def test_study_then_short_break(self):
        t = PomodoroTimer(study_minutes=1, sessions_before_long_break=4)
        t.start()
        t._start_wall_time = time.monotonic() - 61
        t.tick()
        assert t.current_session_type == SESSION_SHORT_BREAK

    def test_short_break_then_study(self):
        t = PomodoroTimer(study_minutes=1, short_break_minutes=1,
                          sessions_before_long_break=4)
        t.start()
        t._start_wall_time = time.monotonic() - 61
        t.tick()
        assert t.current_session_type == SESSION_SHORT_BREAK
        t.start()
        t._start_wall_time = time.monotonic() - 61
        t.tick()
        assert t.current_session_type == SESSION_STUDY

    def test_long_break_after_n_sessions(self):
        t = PomodoroTimer(study_minutes=1, short_break_minutes=1,
                          sessions_before_long_break=2)
        for i in range(2):
            t.start()
            t._start_wall_time = time.monotonic() - 61
            t.tick()
            if t.current_session_type in (SESSION_SHORT_BREAK, SESSION_LONG_BREAK):
                t.start()
                t._start_wall_time = time.monotonic() - 61
                t.tick()
        assert t.completed_study_sessions == 2

    def test_skip_advances_session(self):
        t = PomodoroTimer()
        t.skip()
        assert t.current_session_type == SESSION_SHORT_BREAK
        assert t.completed_study_sessions == 1

    def test_skip_from_break_goes_to_study(self):
        t = PomodoroTimer()
        t.skip()  # study -> short break
        t.skip()  # short break -> study
        assert t.current_session_type == SESSION_STUDY


class TestSetSessionType:

    def test_set_to_short_break(self):
        t = PomodoroTimer(short_break_minutes=5)
        t.set_session_type(SESSION_SHORT_BREAK)
        assert t.current_session_type == SESSION_SHORT_BREAK
        assert t.remaining_seconds == 5 * 60

    def test_set_to_long_break(self):
        t = PomodoroTimer(long_break_minutes=15)
        t.set_session_type(SESSION_LONG_BREAK)
        assert t.current_session_type == SESSION_LONG_BREAK
        assert t.remaining_seconds == 15 * 60

    def test_set_session_type_ignored_when_running(self):
        t = PomodoroTimer()
        t.start()
        t.set_session_type(SESSION_SHORT_BREAK)
        assert t.current_session_type == SESSION_STUDY

    def test_invalid_session_type_raises(self):
        t = PomodoroTimer()
        import pytest
        with pytest.raises(ValueError):
            t.set_session_type("invalid")


class TestProgress:

    def test_progress_zero_at_start(self):
        t = PomodoroTimer()
        assert t.progress == 0.0

    def test_progress_one_at_completion(self):
        t = PomodoroTimer(study_minutes=1)
        t.start()
        t._start_wall_time = time.monotonic() - 60
        t.tick()
        # After completion, timer advances to next session, so check completed count
        assert t.completed_study_sessions == 1


class TestUpdateDurations:

    def test_update_resets_to_idle(self):
        t = PomodoroTimer()
        t.start()
        t.update_durations(
            study_minutes=30,
            short_break_minutes=10,
            long_break_minutes=20,
            sessions_before_long_break=3,
        )
        assert t.state == TimerState.IDLE

    def test_update_changes_remaining(self):
        t = PomodoroTimer()
        t.update_durations(
            study_minutes=30,
            short_break_minutes=10,
            long_break_minutes=20,
            sessions_before_long_break=3,
        )
        assert t.remaining_seconds == 30 * 60


class TestCallbacks:

    def test_state_change_callback(self):
        cb = MagicMock()
        t = PomodoroTimer()
        t.set_on_state_change(cb)
        t.start()
        cb.assert_called_with(TimerState.RUNNING)

    def test_state_change_on_pause(self):
        cb = MagicMock()
        t = PomodoroTimer()
        t.set_on_state_change(cb)
        t.start()
        t.pause()
        cb.assert_called_with(TimerState.PAUSED)

    def test_state_change_on_reset(self):
        cb = MagicMock()
        t = PomodoroTimer()
        t.set_on_state_change(cb)
        t.start()
        t.reset()
        cb.assert_called_with(TimerState.IDLE)
