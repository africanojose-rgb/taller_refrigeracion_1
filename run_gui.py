#!/usr/bin/env python3
"""
Entry point para ejecutar la aplicación GUI.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interface.gui.app import TallerApp

if __name__ == "__main__":
    app = TallerApp()
    app.mainloop()