"""This module contains a helper method that other classes should use when accessing files.
    This solution was created by Dennis Parraga so we can package the exe with all its needed resources without
    preventing us from testing the program using just our preferred IDEs."""
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Executes when testing in development
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)