import tkinter as tk
from flipodoro.ui.theme import PALETTE, TYPOGRAPHY


CARD_WIDTH = 120
CARD_HEIGHT = 160
CARD_RADIUS = 12
GAP_HEIGHT = 4
DIGIT_FONT_SIZE = 90
SEPARATOR_WIDTH = 32

UPPER_COLOR = "#2a2a2e"
LOWER_COLOR = "#1f1f23"
GAP_COLOR = "#0a0a0d"
DIGIT_COLOR = "#f0f0f0"

ANIMATION_STEPS = 6
ANIMATION_DELAY_MS = 25


class FlipDigit(tk.Canvas):

    def __init__(self, parent, char="0", **kwargs):
        super().__init__(
            parent,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            bg=PALETTE.bg_primary,
            highlightthickness=0,
            **kwargs,
        )
        self._char = char
        self._next_char = char
        self._accent = PALETTE.accent_study
        self._animating = False
        self._minimal = False
        self._draw_static(char)

    def set_minimal(self, enabled: bool):
        self._minimal = enabled

    def set_char(self, char):
        if char == self._char and not self._animating:
            return
        self._next_char = char
        if self._minimal:
            self._char = char
            self._draw_static(char)
            return
        if not self._animating:
            self._start_flip()

    def set_accent(self, color):
        if color != self._accent:
            self._accent = color
            if not self._animating:
                self._draw_static(self._char)

    def _draw_static(self, char):
        self.delete("all")
        w = CARD_WIDTH
        h = CARD_HEIGHT
        r = CARD_RADIUS
        mid = h // 2

        self._draw_rounded_top(0, 0, w, mid, r, UPPER_COLOR)
        self._draw_rounded_bottom(0, mid, w, h, r, LOWER_COLOR)

        self.create_text(
            w // 2, h // 2,
            text=char,
            font=(TYPOGRAPHY.family_mono, DIGIT_FONT_SIZE, TYPOGRAPHY.weight_bold),
            fill=DIGIT_COLOR,
            anchor="center",
        )

        self.create_rectangle(
            0, mid - GAP_HEIGHT // 2,
            w, mid + GAP_HEIGHT // 2,
            fill=GAP_COLOR,
            outline="",
        )

    def _start_flip(self):
        self._animating = True
        self._animate_step(0)

    def _animate_step(self, step):
        total = ANIMATION_STEPS
        half = total // 2
        old_char = self._char
        new_char = self._next_char

        if step <= half:
            progress = step / half
            self._draw_upper_falling(old_char, new_char, progress)
        else:
            progress = (step - half) / (total - half)
            self._draw_lower_rising(old_char, new_char, progress)

        if step < total:
            self.after(ANIMATION_DELAY_MS, lambda: self._animate_step(step + 1))
        else:
            self._char = new_char
            self._animating = False
            self._draw_static(new_char)
            if self._next_char != self._char:
                self._start_flip()

    def _draw_upper_falling(self, old_char, new_char, progress):
        self.delete("all")
        w = CARD_WIDTH
        h = CARD_HEIGHT
        r = CARD_RADIUS
        mid = h // 2

        self._draw_rounded_bottom(0, mid, w, h, r, LOWER_COLOR)
        self.create_text(
            w // 2, h // 2,
            text=new_char,
            font=(TYPOGRAPHY.family_mono, DIGIT_FONT_SIZE, TYPOGRAPHY.weight_bold),
            fill=DIGIT_COLOR,
            anchor="center",
        )

        current_height = int(mid * (1.0 - progress))
        if current_height > 2:
            self._draw_rounded_top(0, 0, w, current_height, r, UPPER_COLOR)
            self.create_text(
                w // 2, mid,
                text=old_char,
                font=(TYPOGRAPHY.family_mono, DIGIT_FONT_SIZE, TYPOGRAPHY.weight_bold),
                fill=DIGIT_COLOR,
                anchor="center",
            )
            self.create_rectangle(
                0, current_height,
                w, mid,
                fill=PALETTE.bg_primary,
                outline="",
            )

        self.create_rectangle(
            0, mid - GAP_HEIGHT // 2,
            w, mid + GAP_HEIGHT // 2,
            fill=GAP_COLOR,
            outline="",
        )

    def _draw_lower_rising(self, old_char, new_char, progress):
        self.delete("all")
        w = CARD_WIDTH
        h = CARD_HEIGHT
        r = CARD_RADIUS
        mid = h // 2

        self._draw_rounded_top(0, 0, w, mid, r, UPPER_COLOR)
        self.create_text(
            w // 2, h // 2,
            text=new_char,
            font=(TYPOGRAPHY.family_mono, DIGIT_FONT_SIZE, TYPOGRAPHY.weight_bold),
            fill=DIGIT_COLOR,
            anchor="center",
        )
        self.create_rectangle(
            0, mid, w, h,
            fill=PALETTE.bg_primary,
            outline="",
        )

        flap_top = h - int((h - mid) * progress)
        if flap_top < h - 2:
            self._draw_rounded_bottom(0, flap_top, w, h, r, LOWER_COLOR)
            self.create_text(
                w // 2, h // 2,
                text=new_char,
                font=(TYPOGRAPHY.family_mono, DIGIT_FONT_SIZE, TYPOGRAPHY.weight_bold),
                fill=DIGIT_COLOR,
                anchor="center",
            )
            self.create_rectangle(
                0, mid,
                w, flap_top,
                fill=PALETTE.bg_primary,
                outline="",
            )

        self.create_rectangle(
            0, mid - GAP_HEIGHT // 2,
            w, mid + GAP_HEIGHT // 2,
            fill=GAP_COLOR,
            outline="",
        )

    def _draw_rounded_top(self, x1, y1, x2, y2, radius, color):
        r = radius
        if y2 - y1 < r:
            self.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            return
        self.create_rectangle(x1, y1 + r, x2, y2, fill=color, outline="")
        self.create_rectangle(x1 + r, y1, x2 - r, y1 + r, fill=color, outline="")
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, fill=color, outline="")
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, fill=color, outline="")

    def _draw_rounded_bottom(self, x1, y1, x2, y2, radius, color):
        r = radius
        if y2 - y1 < r:
            self.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            return
        self.create_rectangle(x1, y1, x2, y2 - r, fill=color, outline="")
        self.create_rectangle(x1 + r, y2 - r, x2 - r, y2, fill=color, outline="")
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, fill=color, outline="")
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, fill=color, outline="")


class FlipSeparator(tk.Canvas):

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            width=SEPARATOR_WIDTH,
            height=CARD_HEIGHT,
            bg=PALETTE.bg_primary,
            highlightthickness=0,
            **kwargs,
        )
        self._accent = PALETTE.accent_study
        self._draw()

    def set_accent(self, color):
        self._accent = color
        self._draw()

    def _draw(self):
        self.delete("all")
        w = SEPARATOR_WIDTH
        h = CARD_HEIGHT
        self.create_text(
            w // 2, h // 2,
            text=":",
            font=(TYPOGRAPHY.family_mono, 70, TYPOGRAPHY.weight_bold),
            fill=DIGIT_COLOR,
            anchor="center",
        )


class FlipClock(tk.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=PALETTE.bg_primary, **kwargs)

        self._digits = []

        m1 = FlipDigit(self)
        m1.pack(side=tk.LEFT, padx=4)
        self._digits.append(m1)

        m2 = FlipDigit(self)
        m2.pack(side=tk.LEFT, padx=4)
        self._digits.append(m2)

        self._separator = FlipSeparator(self)
        self._separator.pack(side=tk.LEFT, padx=6)

        s1 = FlipDigit(self)
        s1.pack(side=tk.LEFT, padx=4)
        self._digits.append(s1)

        s2 = FlipDigit(self)
        s2.pack(side=tk.LEFT, padx=4)
        self._digits.append(s2)

        self.set_time(0, 0)

    def set_minimal(self, enabled: bool):
        for digit in self._digits:
            digit.set_minimal(enabled)

    def set_time(self, minutes, seconds):
        minutes = max(0, min(99, minutes))
        seconds = max(0, min(59, seconds))
        chars = [
            str(minutes // 10),
            str(minutes % 10),
            str(seconds // 10),
            str(seconds % 10),
        ]
        for widget, char in zip(self._digits, chars):
            widget.set_char(char)

    def set_accent(self, color):
        for digit in self._digits:
            digit.set_accent(color)
        self._separator.set_accent(color)

    def set_from_seconds(self, total_seconds):
        total_seconds = max(0, total_seconds)
        self.set_time(total_seconds // 60, total_seconds % 60)