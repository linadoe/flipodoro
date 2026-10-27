"""
timer_view.py
-------------
Main timer screen. Full-window layout.
"""

import tkinter as tk
from typing import Callable
from flipodoro.core.timer import PomodoroTimer, TimerState
from flipodoro.core.settings import Settings
from flipodoro.core.constants import (
    TICK_INTERVAL_MS,
    SESSION_STUDY,
    SESSION_SHORT_BREAK,
    SESSION_LONG_BREAK,
    FOCUS_MODE_EXIT_KEY,
)
from flipodoro.ui.theme import (
    PALETTE,
    TYPOGRAPHY,
    SPACING,
    session_accent_color,
    session_label_text,
)
from flipodoro.ui.flip_clock import FlipClock


class TimerView(tk.Frame):

    def __init__(self, parent, timer, settings, on_open_settings,
                 on_toggle_always_on_top=None, on_toggle_minibar=None):
        super().__init__(parent, bg=PALETTE.bg_primary)

        self._timer = timer
        self._settings = settings
        self._on_open_settings = on_open_settings
        self._on_toggle_always_on_top = on_toggle_always_on_top
        self._on_toggle_minibar = on_toggle_minibar
        self._focus_mode = False
        self._tick_job = None

        self._timer.set_on_tick(self._on_timer_tick)
        self._timer.set_on_state_change(self._on_timer_state_change)
        self._timer.set_on_complete(self._on_session_complete)

        self._build_ui()
        self._refresh_display()
        self._start_tick_loop()

    def _build_ui(self):
        self._build_top_bar()

        middle = tk.Frame(self, bg=PALETTE.bg_primary)
        middle.pack(fill=tk.BOTH, expand=True)

        self._session_label_var = tk.StringVar(value="Focus Session")
        self._session_label = tk.Label(
            middle,
            textvariable=self._session_label_var,
            font=(TYPOGRAPHY.family_body, 14, TYPOGRAPHY.weight_bold),
            fg=PALETTE.accent_study,
            bg=PALETTE.bg_primary,
        )
        self._session_label.pack(pady=(30, 20))

        clock_container = tk.Frame(middle, bg=PALETTE.bg_primary)
        clock_container.pack(expand=True)

        self._flip_clock = FlipClock(clock_container)
        self._flip_clock.set_minimal(self._settings.minimal_animation)
        self._flip_clock.pack()

        self._dots_frame = tk.Frame(middle, bg=PALETTE.bg_primary)
        self._dots_frame.pack(pady=(25, 0))
        self._dot_labels = []
        self._rebuild_dots()

        self._build_controls()

        self._focus_hint = tk.Label(
            self,
            text="Press ESC to exit focus mode",
            font=(TYPOGRAPHY.family_body, 9),
            fg=PALETTE.text_muted,
            bg=PALETTE.bg_primary,
        )

    def _build_top_bar(self):
        top = tk.Frame(self, bg=PALETTE.bg_primary)
        top.pack(fill=tk.X, padx=SPACING.lg, pady=(SPACING.md, 0))

        tabs_frame = tk.Frame(top, bg=PALETTE.bg_primary)
        tabs_frame.pack(side=tk.LEFT)

        self._tab_buttons = {}
        tab_configs = [
            (SESSION_STUDY, "Focus"),
            (SESSION_SHORT_BREAK, "Short Break"),
            (SESSION_LONG_BREAK, "Long Break"),
        ]
        for session_type, label in tab_configs:
            btn = tk.Button(
                tabs_frame,
                text=label,
                font=(TYPOGRAPHY.family_body, 10),
                bd=0,
                relief=tk.FLAT,
                padx=10,
                pady=6,
                cursor="hand2",
                command=lambda st=session_type: self._select_session(st),
            )
            btn.pack(side=tk.LEFT, padx=(0, 4))
            self._tab_buttons[session_type] = btn

        self._settings_btn = tk.Button(
            top,
            text="⚙",
            font=(TYPOGRAPHY.family_body, 16),
            bd=0,
            relief=tk.FLAT,
            fg=PALETTE.text_secondary,
            bg=PALETTE.bg_primary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_primary,
            cursor="hand2",
            command=self._on_open_settings,
        )
        self._settings_btn.pack(side=tk.RIGHT)

        pin_text = "📌" if self._settings.always_on_top else "📌"
        self._pin_btn = tk.Button(
            top,
            text=pin_text,
            font=(TYPOGRAPHY.family_body, 14),
            bd=0,
            relief=tk.FLAT,
            fg=PALETTE.accent_study if self._settings.always_on_top else PALETTE.text_muted,
            bg=PALETTE.bg_primary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_primary,
            cursor="hand2",
            command=self._on_toggle_pin,
        )
        self._pin_btn.pack(side=tk.RIGHT, padx=(0, 4))

        self._minibar_btn = tk.Button(
            top,
            text="▔",
            font=(TYPOGRAPHY.family_body, 14),
            bd=0,
            relief=tk.FLAT,
            fg=PALETTE.text_muted,
            bg=PALETTE.bg_primary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_primary,
            cursor="hand2",
            command=self._on_toggle_minibar_click,
        )
        if self._settings.always_on_top:
            self._minibar_btn.pack(side=tk.RIGHT, padx=(0, 4))

    def _rebuild_dots(self):
        for widget in self._dot_labels:
            widget.destroy()
        self._dot_labels.clear()

        count = self._settings.sessions_before_long_break
        for _ in range(count):
            dot = tk.Label(
                self._dots_frame,
                text="●",
                font=(TYPOGRAPHY.family_body, 10),
                bg=PALETTE.bg_primary,
                fg=PALETTE.text_muted,
            )
            dot.pack(side=tk.LEFT, padx=3)
            self._dot_labels.append(dot)

    def _build_controls(self):
        controls = tk.Frame(self, bg=PALETTE.bg_primary)
        controls.pack(pady=(20, 30))

        self._reset_btn = tk.Button(
            controls,
            text="Reset",
            font=(TYPOGRAPHY.family_body, 11),
            bd=1,
            relief=tk.SOLID,
            fg=PALETTE.text_primary,
            bg=PALETTE.bg_primary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_secondary,
            highlightthickness=0,
            cursor="hand2",
            padx=18,
            pady=8,
            command=self._on_reset,
        )
        self._reset_btn.pack(side=tk.LEFT, padx=8)

        self._start_btn = tk.Button(
            controls,
            text="Start",
            font=(TYPOGRAPHY.family_body, 12, TYPOGRAPHY.weight_bold),
            bd=0,
            relief=tk.FLAT,
            fg="#ffffff",
            bg=PALETTE.accent_study,
            activeforeground="#ffffff",
            activebackground=PALETTE.btn_primary_hover,
            cursor="hand2",
            padx=30,
            pady=9,
            command=self._on_start_pause,
        )
        self._start_btn.pack(side=tk.LEFT, padx=8)

        self._skip_btn = tk.Button(
            controls,
            text="Skip",
            font=(TYPOGRAPHY.family_body, 11),
            bd=1,
            relief=tk.SOLID,
            fg=PALETTE.text_primary,
            bg=PALETTE.bg_primary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_secondary,
            highlightthickness=0,
            cursor="hand2",
            padx=18,
            pady=8,
            command=self._on_skip,
        )
        self._skip_btn.pack(side=tk.LEFT, padx=8)

        self._focus_btn = tk.Button(
            controls,
            text="⛶",
            font=(TYPOGRAPHY.family_body, 14),
            bd=0,
            relief=tk.FLAT,
            fg=PALETTE.text_secondary,
            bg=PALETTE.bg_primary,
            activeforeground=PALETTE.text_primary,
            activebackground=PALETTE.bg_primary,
            cursor="hand2",
            command=self._toggle_focus_mode,
        )
        self._focus_btn.pack(side=tk.LEFT, padx=(20, 0))

    def _on_timer_tick(self, remaining, total):
        self._flip_clock.set_from_seconds(remaining)
        self._update_dots()

    def _on_timer_state_change(self, state):
        if state == TimerState.RUNNING:
            self._start_btn.config(text="Pause")
        elif state == TimerState.PAUSED:
            self._start_btn.config(text="Resume")
        else:
            self._start_btn.config(text="Start")
        self._update_tab_styles()

    def _on_session_complete(self, session_type):
        if self._settings.sound_enabled:
            self._play_completion_sound()
        self._flash_screen()
        if self._settings.autostart:
            self.after(1500, self._timer.start)

    def _on_start_pause(self):
        if self._timer.state == TimerState.RUNNING:
            self._timer.pause()
        else:
            self._timer.start()

    def _on_reset(self):
        self._timer.reset()

    def _on_skip(self):
        self._timer.skip()
        self._update_session_display()

    def _select_session(self, session_type):
        if self._timer.state != TimerState.IDLE:
            return
        self._timer.set_session_type(session_type)
        self._update_session_display()

    def _toggle_focus_mode(self):
        root = self.winfo_toplevel()
        if self._focus_mode:
            self._exit_focus_mode(root)
        else:
            self._enter_focus_mode(root)

    def _enter_focus_mode(self, root):
        self._focus_mode = True
        root.attributes("-fullscreen", True)
        self._focus_hint.pack(pady=(SPACING.sm, 0))
        root.bind(FOCUS_MODE_EXIT_KEY, lambda e: self._exit_focus_mode(root))

    def _exit_focus_mode(self, root):
        self._focus_mode = False
        root.attributes("-fullscreen", False)
        self._focus_hint.pack_forget()
        root.unbind(FOCUS_MODE_EXIT_KEY)

    def _refresh_display(self):
        self._update_session_display()
        self._flip_clock.set_from_seconds(self._timer.remaining_seconds)
        self._update_dots()
        self._rebuild_dots()

    def _update_session_display(self):
        session = self._timer.current_session_type
        color = session_accent_color(session)

        display_labels = {
            SESSION_STUDY: "Focus Session",
            SESSION_SHORT_BREAK: "Short Break",
            SESSION_LONG_BREAK: "Long Break",
        }
        self._session_label_var.set(display_labels.get(session, "Focus Session"))
        self._session_label.configure(fg=color)
        self._flip_clock.set_accent(color)

        self._start_btn.configure(bg=color, activebackground=color)

        self._update_tab_styles()

    def _update_tab_styles(self):
        current = self._timer.current_session_type
        for session_type, btn in self._tab_buttons.items():
            if session_type == current:
                color = session_accent_color(session_type)
                btn.configure(
                    fg=color,
                    bg=PALETTE.bg_primary,
                    font=(TYPOGRAPHY.family_body, 10, TYPOGRAPHY.weight_bold),
                )
            else:
                btn.configure(
                    fg=PALETTE.text_muted,
                    bg=PALETTE.bg_primary,
                    font=(TYPOGRAPHY.family_body, 10, TYPOGRAPHY.weight_normal),
                )

    def _update_dots(self):
        completed = self._timer.completed_study_sessions
        cycle_position = completed % self._settings.sessions_before_long_break
        color = session_accent_color(SESSION_STUDY)
        for i, dot in enumerate(self._dot_labels):
            if i < cycle_position:
                dot.configure(fg=color)
            else:
                dot.configure(fg=PALETTE.text_muted)

    def _start_tick_loop(self):
        self._schedule_tick()

    def _schedule_tick(self):
        self._tick_job = self.after(TICK_INTERVAL_MS, self._tick)

    def _tick(self):
        self._timer.tick()
        self._schedule_tick()

    def stop_tick_loop(self):
        if self._tick_job is not None:
            self.after_cancel(self._tick_job)
            self._tick_job = None

    def _play_completion_sound(self):
        import threading

        def _beep_sequence():
            try:
                import winsound
                melody = [
                    (880, 180), (1047, 180), (1319, 250),
                    (0, 120),
                    (880, 180), (1047, 180), (1319, 250),
                    (0, 120),
                    (1319, 150), (1480, 150), (1760, 400),
                ]
                for freq, ms in melody:
                    if freq == 0:
                        import time
                        time.sleep(ms / 1000)
                    else:
                        winsound.Beep(freq, ms)
            except (ImportError, RuntimeError):
                pass

        threading.Thread(target=_beep_sequence, daemon=True).start()

    def _flash_screen(self):
        color = session_accent_color(self._timer.current_session_type)
        steps = [color, PALETTE.bg_primary] * 3
        self._run_flash(steps, 0)

    def _run_flash(self, steps, index):
        if index >= len(steps):
            self.configure(bg=PALETTE.bg_primary)
            for w in self.winfo_children():
                try:
                    w.configure(bg=PALETTE.bg_primary)
                except tk.TclError:
                    pass
            return
        bg = steps[index]
        self.configure(bg=bg)
        for w in self.winfo_children():
            try:
                w.configure(bg=bg)
            except tk.TclError:
                pass
        self.after(200, lambda: self._run_flash(steps, index + 1))

    def _on_toggle_pin(self):
        if self._on_toggle_always_on_top:
            self._on_toggle_always_on_top()

    def update_pin_button(self, is_on_top: bool):
        color = PALETTE.accent_study if is_on_top else PALETTE.text_muted
        self._pin_btn.configure(fg=color)
        if is_on_top:
            self._minibar_btn.pack(side=tk.RIGHT, padx=(0, 4))
        else:
            self._minibar_btn.pack_forget()

    def _on_toggle_minibar_click(self):
        if self._on_toggle_minibar:
            self._on_toggle_minibar()

    def on_settings_applied(self):
        self._timer.update_durations(
            study_minutes=self._settings.study_minutes,
            short_break_minutes=self._settings.short_break_minutes,
            long_break_minutes=self._settings.long_break_minutes,
            sessions_before_long_break=self._settings.sessions_before_long_break,
        )
        self._flip_clock.set_minimal(self._settings.minimal_animation)
        self._refresh_display()