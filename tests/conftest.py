import tkinter as tk

import pytest


@pytest.fixture
def tk_root():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter/Tcl not available in this environment")
    root.withdraw()
    yield root
    root.destroy()
