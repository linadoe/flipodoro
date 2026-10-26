import tkinter as tk
from flipodoro.core.timer import PomodoroTimer, TimerState
from flipodoro.ui.theme import PALETTE, TYPOGRAPHY, session_accent_color


class MiniBar(tk.Frame):

    def __init__(self, parent, timer: PomodoroTimer, on_restore, on_start_pause,
                 on_close):
        super().__init__(parent, bg=PALETTE.bg_secondary, highlightbackground=PALETTE.border,
                         highlightthickness=1)
        self._timer = timer
        self._on_restore = on_restore
        self._on_start_pause = on_start_pause
        self._on_close = on_close
        self._drag_x = 0
        self._drag_y = 0
        self._build_ui()

    def _build_ui(self):
        self._accent_bar = tk.Frame(self, bg=PALETTE.accent_study, width=4)
        self._accent_bar.pack(side=tk.LEFT, fill=tk.Y)

        self._time_label = tk.Label(
            self,
            text="25:00",
            font=(TYPOGRAPHY.family_mono, 14, TYPOGRAPHY.weight_bold),
            fg=PALETTE.text_primary,
            bg=PALETTE.bg_secondary,
            padx=10,
        )
        self._time_label.pack(side=tk.LEFT)

        self._session_label = tk.Label(
            self,
            text="Focus",
            font=(TYPOGRAPHY.family_body, 9),
            fg=PALETTE.text_muted,
            bg=PALETTE.bg_secondary,
        )
        self._session_label.pack(side=tk.LEFT, padx=(0, 8))

        close_btn = tk.Label(
            self, text="✕", font=(TYPOGRAPHY.family_body, 10),
            fg=PALETTE.text_muted, bg=PALETTE.bg_secondary, cursor="hand2",
            padx=6,
        )
        close_btn.pack(side=tk.RIGHT)
        close_btn.bind("<Button-1>", lambda e: self._on_close())

        restore_btn = tk.Label(
            self, text="□", font=(TYPOGRAPHY.family_body, 12),
            fg=PALETTE.text_muted, bg=PALETTE.bg_secondary, cursor="hand2",
            padx=4,
        )
        restore_btn.pack(side=tk.RIGHT)
        restore_btn.bind("<Button-1>", lambda e: self._on_restore())

        play_pause = tk.Label(
            self, text="▶", font=(TYPOGRAPHY.family_body, 11),
            fg=PALETTE.text_primary, bg=PALETTE.bg_secondary, cursor="hand2",
            padx=4,
        )
        play_pause.pack(side=tk.RIGHT)
        play_pause.bind("<Button-1>", lambda e: self._on_start_pause())
        self._play_pause_label = play_pause

        for w in (self._time_label, self._session_label, self):
            w.bind("<Button-1>", self._start_drag)
            w.bind("<B1-Motion>", self._do_drag)
            w.bind("<Double-Button-1>", lambda e: self._on_restore())

    def _start_drag(self, event):
        self._drag_x = event.x_root
        self._drag_y = event.y_root

    def _do_drag(self, event):
        root = self.winfo_toplevel()
        dx = event.x_root - self._drag_x
        dy = event.y_root - self._drag_y
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"+{x}+{y}")
        self._drag_x = event.x_root
        self._drag_y = event.y_root

    def update_display(self, remaining_seconds: int, session_type: str, state: TimerState):
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        self._time_label.config(text=f"{minutes:02d}:{seconds:02d}")

        color = session_accent_color(session_type)
        self._accent_bar.config(bg=color)

        from flipodoro.ui.theme import session_label_text
        self._session_label.config(text=session_label_text(session_type))

        if state == TimerState.RUNNING:
            self._play_pause_label.config(text="⏸")
        else:
            self._play_pause_label.config(text="▶")
