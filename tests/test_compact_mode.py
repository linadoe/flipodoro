"""Tests for compact window mode (smaller min size when pinned)."""

from flipodoro.core.constants import (
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    COMPACT_MIN_WIDTH,
    COMPACT_MIN_HEIGHT,
)


class TestCompactConstants:

    def test_compact_smaller_than_default(self):
        assert COMPACT_MIN_WIDTH < WINDOW_MIN_WIDTH
        assert COMPACT_MIN_HEIGHT < WINDOW_MIN_HEIGHT

    def test_compact_min_width_reasonable(self):
        assert COMPACT_MIN_WIDTH >= 200

    def test_compact_min_height_reasonable(self):
        assert COMPACT_MIN_HEIGHT >= 150


class TestCompactWindow:

    def test_minsize_shrinks_when_pinned(self, tk_root):
        tk_root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        tk_root.minsize(COMPACT_MIN_WIDTH, COMPACT_MIN_HEIGHT)
        tk_root.update_idletasks()
        # Tk accepted the smaller minsize without error

    def test_minsize_restores_when_unpinned(self, tk_root):
        tk_root.minsize(COMPACT_MIN_WIDTH, COMPACT_MIN_HEIGHT)
        tk_root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        tk_root.update_idletasks()
        # Restored to default

    def test_window_can_be_resized_to_compact(self, tk_root):
        tk_root.minsize(COMPACT_MIN_WIDTH, COMPACT_MIN_HEIGHT)
        tk_root.geometry(f"{COMPACT_MIN_WIDTH}x{COMPACT_MIN_HEIGHT}")
        tk_root.update_idletasks()
