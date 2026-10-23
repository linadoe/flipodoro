import tkinter as tk
import logging
import sys
import os

from flipodoro.core.timer import PomodoroTimer
from flipodoro.core.settings import Settings
from flipodoro.core.constants import (
    APP_NAME,
    APP_VERSION,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    COMPACT_MIN_WIDTH,
    COMPACT_MIN_HEIGHT,
)

from flipodoro.ui.theme import PALETTE
from flipodoro.ui.timer_view import TimerView
from flipodoro.ui.settings_view import SettingsView


logger = logging.getLogger(__name__)


def get_icon_path():
    """Get absolute path to icon.ico, handling both source and EXE."""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
        return os.path.join(base, "assets", "icon.ico")
    else:
        this_file = os.path.abspath(__file__)
        ui_dir = os.path.dirname(this_file)
        src_dir = os.path.dirname(ui_dir)
        return os.path.join(src_dir, "assets", "icon.ico")


class App:

    def __init__(self):
        self._settings = Settings()
        self._timer = PomodoroTimer(
            study_minutes=self._settings.study_minutes,
            short_break_minutes=self._settings.short_break_minutes,
            long_break_minutes=self._settings.long_break_minutes,
            sessions_before_long_break=self._settings.sessions_before_long_break,
        )
        self._root = self._create_root_window()
        self._timer_view = self._create_timer_view()
        self._timer_view.pack(fill=tk.BOTH, expand=True)
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._bind_shortcuts()
        logger.info("%s v%s started.", APP_NAME, APP_VERSION)

    def run(self):
        self._root.mainloop()

    def _create_root_window(self):
        root = tk.Tk()
        root.title(APP_NAME)
        root.configure(bg=PALETTE.bg_primary)
        root.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")
        root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        root.resizable(True, True)

        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            try:
                root.iconbitmap(default=icon_path)
                logger.info("Icon loaded from: %s", icon_path)
                root.after_idle(lambda: self._reapply_icon(root, icon_path))
            except Exception as e:
                logger.warning("Failed to set iconbitmap: %s", e)
                try:
                    icon_img = tk.PhotoImage(file=icon_path)
                    root.iconphoto(True, icon_img)
                    logger.info("Icon set via iconphoto fallback")
                except Exception as e2:
                    logger.error("Both icon methods failed: %s", e2)
        else:
            logger.warning("Icon file not found at: %s", icon_path)

        if self._settings.always_on_top:
            root.attributes("-topmost", True)
            root.minsize(COMPACT_MIN_WIDTH, COMPACT_MIN_HEIGHT)

        return root

    @staticmethod
    def _reapply_icon(root, icon_path):
        try:
            root.iconbitmap(default=icon_path)
        except Exception:
            pass

    def _create_timer_view(self):
        return TimerView(
            parent=self._root,
            timer=self._timer,
            settings=self._settings,
            on_open_settings=self._open_settings,
            on_toggle_always_on_top=self.toggle_always_on_top,
        )

    def _open_settings(self):
        SettingsView(
            parent=self._root,
            settings=self._settings,
            on_save=self._on_settings_saved,
            pinned=self._settings.always_on_top,
        )

    def _on_settings_saved(self):
        self._timer_view.on_settings_applied()
        on_top = self._settings.always_on_top
        self._root.attributes("-topmost", on_top)
        if on_top:
            from flipodoro.core.constants import COMPACT_MIN_WIDTH, COMPACT_MIN_HEIGHT
            self._root.minsize(COMPACT_MIN_WIDTH, COMPACT_MIN_HEIGHT)
        else:
            self._root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self._timer_view.update_pin_button(on_top)

    def _on_close(self):
        self._timer_view.stop_tick_loop()
        self._settings.save()
        self._root.destroy()

    def toggle_always_on_top(self):
        new_val = not self._settings.always_on_top
        self._settings.always_on_top = new_val
        self._root.attributes("-topmost", new_val)
        if new_val:
            self._root.minsize(COMPACT_MIN_WIDTH, COMPACT_MIN_HEIGHT)
        else:
            self._root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self._settings.save()
        self._timer_view.update_pin_button(new_val)

    def _bind_shortcuts(self):
        self._root.bind("<space>", lambda e: self._timer_view._on_start_pause())
        self._root.bind("<r>", lambda e: self._timer_view._on_reset())
        self._root.bind("<R>", lambda e: self._timer_view._on_reset())
        self._root.bind("<s>", lambda e: self._timer_view._on_skip())
        self._root.bind("<S>", lambda e: self._timer_view._on_skip())
        self._root.bind("<f>", lambda e: self._timer_view._toggle_focus_mode())
        self._root.bind("<F>", lambda e: self._timer_view._toggle_focus_mode())
        self._root.bind("<t>", lambda e: self.toggle_always_on_top())
        self._root.bind("<T>", lambda e: self.toggle_always_on_top())
        self._root.bind("<Control-comma>", lambda e: self._open_settings())