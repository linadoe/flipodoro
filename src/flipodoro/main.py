"""
main.py
-------
Configures logging and launches the application.
"""

import logging
import sys
import os


def configure_logging() -> None:
    is_frozen = getattr(sys, "frozen", False)

    if is_frozen:
        app_data = os.environ.get("APPDATA") or os.path.expanduser("~/.config")
        log_dir = os.path.join(app_data, "Flipodoro")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "flipodoro.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[logging.FileHandler(log_path, encoding="utf-8")],
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )


def set_windows_app_id() -> None:
    """
    Tell Windows this is a distinct app (not just Python).
    This makes the taskbar show OUR icon instead of Python's icon.
    """
    try:
        from ctypes import windll
        app_id = "OmDautkhani.Flipodoro.FlipClockTimer.1.1.0"
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except (ImportError, AttributeError, OSError):
        pass


def main() -> None:
    configure_logging()
    logger = logging.getLogger(__name__)

    # Set Windows app ID BEFORE creating the app
    set_windows_app_id()

    try:
        from flipodoro.ui.app import App
        app = App()
        app.run()
    except Exception as exc:
        logger.critical("Unhandled exception: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()