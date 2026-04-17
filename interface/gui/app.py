"""
Aplicación GUI para Taller de Refrigeración
Arquitectura: Separación estricta entre UI y lógica de negocio
"""

import customtkinter as ctk
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.database import init_db, get_session
from infrastructure.repositories.cliente_repository_impl import ClienteRepositoryImpl
from infrastructure.repositories.equipo_repository_impl import EquipoRepositoryImpl
from infrastructure.repositories.orden_repository_impl import OrdenRepositoryImpl
from infrastructure.repositories.tecnico_repository_impl import TecnicoRepositoryImpl
from infrastructure.repositories.repuesto_repository_impl import RepuestoRepositoryImpl
from infrastructure.repositories.item_orden_repository_impl import (
    ItemOrdenRepositoryImpl,
)
from infrastructure.repositories.factura_repository_impl import FacturaRepositoryImpl
from application.use_cases.cliente_use_cases import ClienteUseCases
from application.use_cases.equipo_use_cases import EquipoUseCases
from application.use_cases.orden_use_cases import OrdenUseCases
from application.use_cases.tecnico_use_cases import TecnicoUseCases
from application.use_cases.repuesto_use_cases import RepuestoUseCases
from application.use_cases.reporte_use_cases import ReporteUseCases
from application.use_cases.factura_use_cases import FacturaUseCases


class TallerApp(ctk.CTk):
    """Aplicación principal con conexión al backend."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Taller de Refrigeración Africano")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self._init_backend()
        self._init_ui()

    def _init_backend(self):
        """Inicializa la conexión con el backend (Clean Architecture)."""
        init_db()
        session = get_session()

        self.cliente_repo = ClienteRepositoryImpl(session)
        self.equipo_repo = EquipoRepositoryImpl(session)
        self.orden_repo = OrdenRepositoryImpl(session)
        self.tecnico_repo = TecnicoRepositoryImpl(session)
        self.repuesto_repo = RepuestoRepositoryImpl(session)
        self.item_orden_repo = ItemOrdenRepositoryImpl(session)
        self.factura_repo = FacturaRepositoryImpl(session)

        self.cliente_use_cases = ClienteUseCases(self.cliente_repo)
        self.equipo_use_cases = EquipoUseCases(self.equipo_repo)
        self.orden_use_cases = OrdenUseCases(
            self.orden_repo, self.item_orden_repo, self.repuesto_repo
        )
        self.tecnico_use_cases = TecnicoUseCases(self.tecnico_repo)
        self.repuesto_use_cases = RepuestoUseCases(self.repuesto_repo)
        self.reporte_use_cases = ReporteUseCases(
            self.cliente_repo, self.equipo_repo, self.orden_repo, self.tecnico_repo
        )
        self.factura_use_cases = FacturaUseCases(
            self.factura_repo, self.orden_repo, self.item_orden_repo
        )
        self.tecnico_use_cases = TecnicoUseCases(self.tecnico_repo)
        self.repuesto_use_cases = RepuestoUseCases(self.repuesto_repo)
        self.reporte_use_cases = ReporteUseCases(
            self.cliente_repo, self.equipo_repo, self.orden_repo, self.tecnico_repo
        )

    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarFrame(self, self._show_frame)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content_frame = None
        self._show_frame("clientes")

    def _show_frame(self, frame_name: str):
        """Cambia el frame de contenido."""
        if self.content_frame:
            self.content_frame.destroy()

        if frame_name == "clientes":
            from .frames.clientes_frame import ClientesFrame

            self.content_frame = ClientesFrame(
                self, self.cliente_use_cases, self.equipo_use_cases
            )
        elif frame_name == "equipos":
            from .frames.equipos_frame import EquiposFrame

            self.content_frame = EquiposFrame(
                self, self.equipo_use_cases, self.cliente_use_cases
            )
        elif frame_name == "tecnicos":
            from .frames.tecnicos_frame import TecnicosFrame

            self.content_frame = TecnicosFrame(self, self.tecnico_use_cases)
        elif frame_name == "ordenes":
            from .frames.ordenes_frame import OrdenesFrame

            self.content_frame = OrdenesFrame(
                self,
                self.orden_use_cases,
                self.equipo_use_cases,
                self.tecnico_use_cases,
                self.repuesto_use_cases,
            )
        elif frame_name == "finanzas":
            from .frames.finanzas_frame import FinanzasFrame

            self.content_frame = FinanzasFrame(self)
        elif frame_name == "facturacion":
            from .frames.facturacion_frame import FacturacionFrame

            self.content_frame = FacturacionFrame(
                self,
                self.factura_use_cases,
                self.orden_use_cases,
                self.cliente_use_cases,
                self.equipo_use_cases,
                self.tecnico_use_cases,
                self.repuesto_use_cases,
            )
        elif frame_name == "inventario":
            from .frames.inventario_frame import InventarioFrame

            self.content_frame = InventarioFrame(self, self.repuesto_use_cases)

        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


class SidebarFrame(ctk.CTkFrame):
    """Barra lateral de navegación."""

    def __init__(self, master, callback):
        super().__init__(master, width=200, corner_radius=0)

        self.callback = callback

        self._init_ui()

    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="TALLER DE\nREFRIGERACIÓN\nAFRICANO",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#3498db",
        )
        title.grid(row=0, column=0, padx=20, pady=(30, 40))

        nav_items = [
            ("Clientes", "clientes"),
            ("Equipos", "equipos"),
            ("Técnicos", "tecnicos"),
            ("Órdenes", "ordenes"),
            ("Inventario", "inventario"),
            ("Finanzas", "finanzas"),
            ("Facturación", "facturacion"),
        ]

        for i, (label, key) in enumerate(nav_items, 1):
            btn = ctk.CTkButton(
                self,
                text=label,
                command=lambda k=key: self.callback(k),
                fg_color="transparent",
                hover_color=("#3498db", "#2980b9"),
                anchor="w",
                height=40,
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")

        spacer = ctk.CTkLabel(self, text="")
        spacer.grid(row=len(nav_items) + 1, column=0, pady=20)

        btn_salir = ctk.CTkButton(
            self,
            text="Salir",
            command=self.master.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b",
        )
        btn_salir.grid(row=len(nav_items) + 2, column=0, padx=20, pady=20, sticky="ew")


if __name__ == "__main__":
    app = TallerApp()
    app.mainloop()
