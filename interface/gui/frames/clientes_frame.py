"""
Vista de Clientes - CRUD completo con conexión al backend.
"""
import customtkinter as ctk
from typing import Optional


class ClientesFrame(ctk.CTkFrame):
    """Frame para gestión de clientes."""
    
    def __init__(self, master, cliente_use_cases, equipo_use_cases):
        super().__init__(master, fg_color="transparent")
        
        self.cliente_use_cases = cliente_use_cases
        self.equipo_use_cases = equipo_use_cases
        
        self._init_ui()
        self._cargar_clientes()
    
    def _init_ui(self):
        """Inicializa la interfaz."""
        self.grid_columnconfigure(0, weight=1)
        
        self._crear_formulario()
        self._crear_tabla()
    
    def _crear_formulario(self):
        """Crea el formulario de cliente."""
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        form_frame.grid_columnconfigure((1, 2, 3), weight=1)
        
        titulo = ctk.CTkLabel(
            form_frame,
            text="Nuevo Cliente",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=10)
        
        ctk.CTkLabel(form_frame, text="Nombre:*").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo")
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Teléfono:*").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.entry_telefono = ctk.CTkEntry(form_frame, placeholder_text="Teléfono")
        self.entry_telefono.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Dirección:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_direccion = ctk.CTkEntry(form_frame, placeholder_text="Dirección")
        self.entry_direccion.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Email:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(form_frame, placeholder_text="email@ejemplo.com")
        self.entry_email.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Guardar Cliente",
            command=self._guardar_cliente,
            fg_color="#27ae60",
            hover_color="#229954"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Limpiar",
            command=self._limpiar_formulario,
            fg_color="#7f8c8d",
            hover_color="#626567"
        ).pack(side="left", padx=5)
    
    def _crear_tabla(self):
        """Crea la tabla de clientes."""
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="Lista de Clientes",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.entry_buscar = ctk.CTkEntry(
            header_frame,
            placeholder_text="Buscar por nombre...",
            width=200
        )
        self.entry_buscar.pack(side="right", padx=10)
        
        self.entry_buscar.bind("<KeyRelease>", lambda e: self._buscar_cliente())
        
        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self._crear_encabezado_tabla()
    
    def _crear_encabezado_tabla(self):
        """Crea el encabezado de la tabla."""
        columnas = ["ID", "Nombre", "Teléfono", "Dirección", "Email", "Acción"]
        
        headers = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        headers.grid(row=0, column=0, sticky="ew", columnspan=6)
        
        for i, col in enumerate(columnas):
            ctk.CTkLabel(
                headers,
                text=col,
                font=ctk.CTkFont(weight="bold"),
                text_color="#3498db"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
    def _guardar_cliente(self):
        """Guarda un nuevo cliente usando el caso de uso."""
        from application.dto.cliente_dto import ClienteCreateDTO
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        direccion = self.entry_direccion.get().strip()
        email = self.entry_email.get().strip() or None
        
        if not nombre or not telefono:
            mostrar_mensaje(self, "Nombre y teléfono son obligatorios", "error")
            return
        
        try:
            dto = ClienteCreateDTO(
                nombre=nombre,
                telefono=telefono,
                direccion=direccion or None,
                email=email
            )
            self.cliente_use_cases.crear_cliente(dto)
            mostrar_mensaje(self, "Cliente guardado exitosamente", "success")
            self._limpiar_formulario()
            self._cargar_clientes()
        except Exception as e:
            mostrar_mensaje(self, f"Error: {str(e)}", "error")
    
    def _limpiar_formulario(self):
        """Limpia los campos del formulario."""
        self.entry_nombre.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.entry_direccion.delete(0, "end")
        self.entry_email.delete(0, "end")
    
    def _cargar_clientes(self):
        """Carga todos los clientes desde el backend."""
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()
        
        clientes = self.cliente_use_cases.listar_clientes()
        
        if not clientes:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No hay clientes registrados",
                text_color="gray"
            ).grid(row=1, column=0, columnspan=6, pady=20)
            return
        
        for i, cliente in enumerate(clientes, 1):
            self._crear_fila_cliente(cliente, i)
    
    def _crear_fila_cliente(self, cliente, row):
        """Crea una fila de cliente en la tabla."""
        ctk.CTkLabel(self.scroll_frame, text=str(cliente.id)).grid(
            row=row, column=0, padx=5, pady=5, sticky="w"
        )
        ctk.CTkLabel(self.scroll_frame, text=cliente.nombre).grid(
            row=row, column=1, padx=5, pady=5, sticky="w"
        )
        ctk.CTkLabel(self.scroll_frame, text=cliente.telefono).grid(
            row=row, column=2, padx=5, pady=5, sticky="w"
        )
        ctk.CTkLabel(self.scroll_frame, text=cliente.direccion or "-").grid(
            row=row, column=3, padx=5, pady=5, sticky="w"
        )
        ctk.CTkLabel(self.scroll_frame, text=cliente.email or "-").grid(
            row=row, column=4, padx=5, pady=5, sticky="w"
        )
        
        btn = ctk.CTkButton(
            self.scroll_frame,
            text="Ver Equipos",
            command=lambda: self._ver_equipos_cliente(cliente),
            width=80,
            height=25,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        btn.grid(row=row, column=5, padx=5, pady=5)
    
    def _buscar_cliente(self):
        """Busca clientes por nombre."""
        termino = self.entry_buscar.get().strip()
        
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()
        
        if termino:
            clientes = self.cliente_use_cases.buscar_clientes(termino)
        else:
            clientes = self.cliente_use_cases.listar_clientes()
        
        if not clientes:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No se encontraron resultados",
                text_color="gray"
            ).grid(row=1, column=0, columnspan=6, pady=20)
            return
        
        for i, cliente in enumerate(clientes, 1):
            self._crear_fila_cliente(cliente, i)
    
    def _ver_equipos_cliente(self, cliente):
        """Muestra los equipos de un cliente específico."""
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        equipos = self.equipo_use_cases.listar_equipos_por_cliente(cliente.id)
        
        if not equipos:
            mostrar_mensaje(self, f"El cliente {cliente.nombre} no tiene equipos registrados", "info")
            return
        
        info = f"Equipos de {cliente.nombre}:\n\n"
        for eq in equipos:
            info += f"• {eq.tipo_equipo} {eq.marca} {eq.modelo or ''}\n"
        
        mostrar_mensaje(self, info, "info")