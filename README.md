# Flipodoro

A flip clock Pomodoro timer for developers who work on a single screen and need a timer that stays out of the way.

> **Work in progress** — this is a personal dev tool, not a polished release. Expect rough edges.

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.14%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Why

Most Pomodoro apps either take over your screen or hide in a tray where you forget about them. Flipodoro pins a tiny bar to the top of your monitor — just the countdown and session type — so you always see the time without losing workspace. When you want the full view, expand it back with a double-click.

---

## Getting Started

Requires **Python 3.14+** and [**uv**](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/The-Python-Dev/flipodoro.git
cd flipodoro
uv run flipodoro
```

That's it. `uv` handles the virtual environment and dependencies automatically.

If you want to run it without installing the package:

```bash
uv run python -m flipodoro.main
```

---

## Features

- Flip clock display with flip animation on every tick
- Three session types: **Focus**, **Short Break**, **Long Break**
- Customisable durations (1-99 minutes)
- **Always-on-top** — pin the timer above other windows (`T`)
- **Minibar mode** — collapse to a thin bar at the top of the screen (`M`), perfect for single-monitor setups
- **Auto-start** — optionally start the next session (break or focus) automatically, no manual intervention needed
- Focus mode: fullscreen distraction-free (`F`, `ESC` to exit)
- Minimal animation option
- Session dots showing cycle progress
- Session-based accent colors (red / teal / purple)
- Dark theme
- Settings persist between sessions
- Zero dependencies — pure Python standard library + Tkinter

### Minibar Mode

Pin the timer with `T`, then press `M` to collapse it into a minimal bar at the top center of the screen. It shows the countdown, session type, and play/pause — nothing else. Drag it to reposition, double-click to restore.

---

## Keyboard Shortcuts

| Key        | Action                       |
|------------|------------------------------|
| `Space`    | Start / Pause                |
| `R`        | Reset                        |
| `S`        | Skip session                 |
| `F`        | Toggle focus mode            |
| `T`        | Toggle always-on-top         |
| `M`        | Toggle minibar (when pinned) |
| `Esc`      | Exit focus mode              |
| `Ctrl + ,` | Open settings                |

---

## Project Structure

```
flipodoro/
├── src/flipodoro/
│   ├── main.py               # Entry point, logging
│   ├── core/                  # Business logic (no UI)
│   │   ├── timer.py
│   │   ├── settings.py
│   │   └── constants.py
│   ├── ui/                    # All visual components
│   │   ├── app.py
│   │   ├── timer_view.py
│   │   ├── settings_view.py
│   │   ├── flip_clock.py
│   │   ├── minibar.py
│   │   └── theme.py
│   └── assets/
│       └── icon.ico
├── tests/
├── pyproject.toml
└── README.md
```

---

## Building an EXE

If you want a standalone binary:

```bash
uv run pyinstaller --onefile --windowed --name Flipodoro --icon=src/flipodoro/assets/icon.ico --add-data "src/flipodoro/assets;assets" src/flipodoro/main.py
```

Output: `dist/Flipodoro.exe`

---

## Known Limitations

- 99-minute display limit
- Flip clock doesn't scale with window resize
- Windows only (Tkinter + `winsound` + Windows app ID)

---

## License

MIT — see [LICENSE](LICENSE).

---

## Authors

Originally created by **Om Dautkhani** ([@The-Python-Dev](https://github.com/The-Python-Dev)).

Always-on-top, minibar, minimal animation, and compact mode by **Lina Doering**.
