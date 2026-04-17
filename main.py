#!/usr/bin/env python3
"""
Punto de entrada principal del Taller de Refrigeración.
Ejecuta la interfaz gráfica por defecto.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from interface.gui.app import TallerApp
    
    print("Iniciando Taller de Refrigeración...")
    app = TallerApp()
    app.mainloop()