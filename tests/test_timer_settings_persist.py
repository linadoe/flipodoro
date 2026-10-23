"""Tests for timer continuing through settings save."""

import time
from flipodoro.core.timer import PomodoroTimer, TimerState
from flipodoro.core.constants import SESSION_STUDY


class TestTimerContinuesThroughSettingsSave:

    def test_running_timer_stays_running_when_duration_unchanged(self):
        t = PomodoroTimer(study_minutes=25)
        t.start()
        t.update_durations(
            study_minutes=25,
            short_break_minutes=5,
            long_break_minutes=15,
            sessions_before_long_break=4,
        )
        assert t.state == TimerState.RUNNING

    def test_running_timer_preserves_remaining_when_duration_unchanged(self):
        t = PomodoroTimer(study_minutes=25)
        t.start()
        t._start_wall_time = time.monotonic() - 60
        t.tick()
        remaining_before = t.remaining_seconds
        t.update_durations(
            study_minutes=25,
            short_break_minutes=10,
            long_break_minutes=20,
            sessions_before_long_break=3,
        )
        assert t.remaining_seconds == remaining_before
        assert t.state == TimerState.RUNNING

    def test_running_timer_resets_when_current_session_duration_changes(self):
        t = PomodoroTimer(study_minutes=25)
        t.start()
        t.update_durations(
            study_minutes=30,
            short_break_minutes=5,
            long_break_minutes=15,
            sessions_before_long_break=4,
        )
        assert t.state == TimerState.IDLE
        assert t.remaining_seconds == 30 * 60

    def test_paused_timer_stays_paused_when_duration_unchanged(self):
        t = PomodoroTimer(study_minutes=25)
        t.start()
        t._start_wall_time = time.monotonic() - 30
        t.pause()
        remaining_before = t.remaining_seconds
        t.update_durations(
            study_minutes=25,
            short_break_minutes=10,
            long_break_minutes=20,
            sessions_before_long_break=3,
        )
        assert t.state == TimerState.PAUSED
        assert t.remaining_seconds == remaining_before

    def test_paused_timer_resets_when_current_duration_changes(self):
        t = PomodoroTimer(study_minutes=25)
        t.start()
        t.pause()
        t.update_durations(
            study_minutes=50,
            short_break_minutes=5,
            long_break_minutes=15,
            sessions_before_long_break=4,
        )
        assert t.state == TimerState.IDLE
        assert t.remaining_seconds == 50 * 60

    def test_idle_timer_updates_duration(self):
        t = PomodoroTimer(study_minutes=25)
        t.update_durations(
            study_minutes=30,
            short_break_minutes=5,
            long_break_minutes=15,
            sessions_before_long_break=4,
        )
        assert t.state == TimerState.IDLE
        assert t.remaining_seconds == 30 * 60

    def test_other_session_duration_change_doesnt_reset_current(self):
        """Changing short_break duration while in a study session should not reset."""
        t = PomodoroTimer(study_minutes=25, short_break_minutes=5)
        t.start()
        t.update_durations(
            study_minutes=25,
            short_break_minutes=10,
            long_break_minutes=15,
            sessions_before_long_break=4,
        )
        assert t.state == TimerState.RUNNING
