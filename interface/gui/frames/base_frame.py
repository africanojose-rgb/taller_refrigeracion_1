"""
Frame base para todas las vistas de la aplicación.
Contiene elementos comunes y métodos reutilizables.
"""
import customtkinter as ctk
from tkinter import ttk


class BaseFrame(ctk.CTkFrame):
    """Clase base para todos los frames de la aplicación."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def _crear_titulo(self, texto: str):
        """Crea un título de sección."""
        label = ctk.CTkLabel(
            self,
            text=texto,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        label.grid(row=0, column=0, sticky="w", pady=(0, 20))
    
    def _crear_tabla(self, columnas: list, row=1):
        """Crea una tabla(scrollframe) con las columnas especificadas."""
        scrollable_frame = ctk.CTkScrollableFrame(self, label_text="")
        scrollable_frame.grid(row=row, column=0, sticky="nsew", pady=10)
        scrollable_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        headers_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        headers_frame.grid(row=0, column=0, sticky="ew")
        
        for i, col in enumerate(columnas):
            header = ctk.CTkLabel(
                headers_frame,
                text=col,
                font=ctk.CTkFont(weight="bold"),
                text_color="#3498db"
            )
            header.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        return scrollable_frame
    
    def _mostrar_mensaje(self, mensaje: str, tipo: str = "info"):
        """Muestra un mensaje en un dialog."""
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        mostrar_mensaje(self, mensaje, tipo)
    
    def _crear_boton(self, texto: str, comando, row: int, col: int = 0, **kwargs):
        """Crea un botón con estilo consistente."""
        btn = ctk.CTkButton(
            self,
            text=texto,
            command=comando,
            **kwargs
        )
        btn.grid(row=row, column=col, padx=5, pady=10, sticky="ew")
        return btn
    
    def _crear_entrada(self, label: str, row: int, col: int = 0, variable=None):
        """Crea una etiqueta y entrada."""
        lbl = ctk.CTkLabel(self, text=label)
        lbl.grid(row=row, column=col, padx=5, pady=5, sticky="w")
        
        if variable:
            entrada = ctk.CTkEntry(self, textvariable=variable)
        else:
            entrada = ctk.CTkEntry(self)
        
        entrada.grid(row=row, column=col+1, padx=5, pady=5, sticky="ew")
        return entrada