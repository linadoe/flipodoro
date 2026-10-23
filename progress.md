# Flipodoro v1.1 Progress

## Tasks

### 1. Translate requirements to uv lock
- [x] Update `pyproject.toml` with proper metadata, dev deps (`pytest`, `pyinstaller`)
- [x] Run `uv lock` to generate `uv.lock`

### 2. Always-on-top toggle
- [x] Add `always_on_top` setting to `Settings` (persisted, default `False`)
- [x] Add `DEFAULT_ALWAYS_ON_TOP` constant to `constants.py`
- [x] Add toggle button in `TimerView` top bar (pin icon)
- [x] Add checkbox in `SettingsView`
- [x] Wire `root.attributes("-topmost", ...)` in `App`
- [x] Add keyboard shortcut (`T` key)
- [x] Tests pass

### 3. Fix custom icon in taskbar/title bar
- [x] Ensure `SetCurrentProcessExplicitAppUserModelID` is called before Tk() init
- [x] Use `iconbitmap(default=...)` with verified path
- [x] Add `after_idle` icon refresh workaround for Windows caching
- [x] Tests pass

### 4. Visualization with minimal movement
- [x] Add "minimal animation" mode: skip flip, redraw static when `_minimal` is True
- [x] Add `minimal_animation` setting to `Settings` (persisted, default `False`)
- [x] `FlipDigit.set_minimal()` and `FlipClock.set_minimal()` implemented
- [x] Add checkbox in `SettingsView`
- [x] Wire minimal mode from settings into TimerView/FlipClock
- [x] Tests pass

### 5. Final
- [x] All tests green (25 passed, 0 failed)
- [x] Update CHANGELOG.md
- [x] Wire remaining UI (settings checkboxes, always-on-top button, icon refresh)
