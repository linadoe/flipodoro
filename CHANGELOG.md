# Changelog

All notable changes to Flipodoro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Always-on-top toggle (pin button in top bar + `T` shortcut + settings checkbox)
- Minimal animation mode — skips flip animation, redraws digits statically (settings checkbox)
- New "Display" section in settings for always-on-top and minimal animation

### Fixed
- Custom icon now persists in taskbar/title bar via `after_idle` reapply workaround
- Always-on-top state restored on app launch from saved settings

### Planned (v1.1 — remaining)
- Support durations above 99 minutes
- Custom completion sound
- Multiple theme options (light mode + more)
- Tick sound on flip animation

### Planned (v1.2)
- Responsive flip clock scaling
- System tray support

---

## [1.0.0] - 2026-07-06

### Added
- Initial public release
- Flip clock display with satisfying flip animation on every tick
- Three session types: Focus, Short Break, and Long Break
- Fully customisable session durations (1-99 minutes)
- Dark theme easy on the eyes for long sessions
- Focus mode: fullscreen, distraction-free (ESC to exit)
- Keyboard shortcuts (Space, R, S, F, Esc, Ctrl+,)
- Settings persistence via `flipodoro_settings.json`
- Offline-first: no accounts, no cloud, just a timer
- Standalone Windows EXE (no installation required)
- Zero third-party dependencies (pure Tkinter!)
- Custom flip clock widget built with Canvas primitives

### Known Issues
- Custom icon does not appear in taskbar/title bar while app is running (Windows caching)
- Maximum practical duration is 99 minutes (display limit)
- Flip clock does not scale with window resize

---

## Version Format

- **[MAJOR.MINOR.PATCH]** — e.g., `1.2.3`
  - **MAJOR**: Breaking changes
  - **MINOR**: New features (backwards compatible)
  - **PATCH**: Bug fixes only

## Categories

- **Added** — new features
- **Changed** — updates to existing features
- **Deprecated** — features to be removed
- **Removed** — removed features
- **Fixed** — bug fixes
- **Security** — security patches