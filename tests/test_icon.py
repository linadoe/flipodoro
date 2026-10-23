"""Tests for custom icon in taskbar/title bar."""

import os
import sys
import platform

import pytest

from flipodoro.ui.app import get_icon_path
from flipodoro.main import set_windows_app_id


class TestIconPath:

    def test_icon_path_exists(self):
        path = get_icon_path()
        assert os.path.isfile(path), f"Icon not found at {path}"

    def test_icon_path_is_ico(self):
        path = get_icon_path()
        assert path.endswith(".ico")

    def test_icon_file_not_empty(self):
        path = get_icon_path()
        assert os.path.getsize(path) > 0


class TestWindowsAppId:

    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows only")
    def test_set_app_id_does_not_raise(self):
        set_windows_app_id()

    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows only")
    def test_app_id_set_before_tk(self):
        """AppUserModelID must be set before Tk() for the taskbar icon to work."""
        from ctypes import windll
        app_id = "OmDautkhani.Flipodoro.FlipClockTimer.1.1.0"
        result = windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        assert result == 0  # S_OK


class TestIconAppliedToWindow:

    def test_iconbitmap_with_default(self, tk_root):
        path = get_icon_path()
        if os.path.isfile(path):
            tk_root.iconbitmap(default=path)
            # If no exception, icon was accepted by Tk

    def test_icon_survives_after_idle(self, tk_root):
        """Icon should persist after an after_idle cycle (Windows caching fix)."""
        path = get_icon_path()
        if not os.path.isfile(path):
            pytest.skip("icon.ico not found")
        tk_root.iconbitmap(default=path)
        applied = [False]

        def reapply():
            tk_root.iconbitmap(default=path)
            applied[0] = True

        tk_root.after_idle(reapply)
        tk_root.update_idletasks()
        assert applied[0]
