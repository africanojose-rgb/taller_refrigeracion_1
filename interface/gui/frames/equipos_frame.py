"""
Vista de Equipos - CRUD y relación con clientes.
"""
import customtkinter as ctk


class EquiposFrame(ctk.CTkFrame):
    """Frame para gestión de equipos."""
    
    def __init__(self, master, equipo_use_cases, cliente_use_cases):
        super().__init__(master, fg_color="transparent")
        
        self.equipo_use_cases = equipo_use_cases
        self.cliente_use_cases = cliente_use_cases
        
        self._init_ui()
        self._cargar_datos()
    
    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        self._crear_formulario()
        self._crear_tabla()
    
    def _crear_formulario(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        form_frame.grid_columnconfigure((1, 2), weight=1)
        
        titulo = ctk.CTkLabel(
            form_frame,
            text="Nuevo Equipo",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=10)
        
        ctk.CTkLabel(form_frame, text="Cliente:*").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.combo_cliente = ctk.CTkComboBox(form_frame)
        self.combo_cliente.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Tipo:*").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.combo_tipo = ctk.CTkComboBox(form_frame, values=["Aire Acondicionado", "Refrigerador", "Congelador", "Vitrina", "Otro"])
        self.combo_tipo.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Marca:*").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_marca = ctk.CTkEntry(form_frame, placeholder_text="Marca")
        self.entry_marca.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Modelo:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.entry_modelo = ctk.CTkEntry(form_frame, placeholder_text="Modelo")
        self.entry_modelo.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Serial:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_serial = ctk.CTkEntry(form_frame, placeholder_text="Número de serie")
        self.entry_serial.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Guardar Equipo",
            command=self._guardar_equipo,
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
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkLabel(
            table_frame,
            text="Lista de Equipos",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        self._crear_encabezado()
    
    def _crear_encabezado(self):
        columnas = ["ID", "Tipo", "Marca", "Modelo", "Serial", "Cliente"]
        
        headers = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        headers.grid(row=0, column=0, sticky="ew", columnspan=6)
        
        for i, col in enumerate(columnas):
            ctk.CTkLabel(
                headers,
                text=col,
                font=ctk.CTkFont(weight="bold"),
                text_color="#3498db"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
    def _cargar_datos(self):
        clientes = self.cliente_use_cases.listar_clientes()
        self.clientes_dict = {f"{c.nombre} (ID: {c.id})": c.id for c in clientes}
        self.combo_cliente.configure(values=list(self.clientes_dict.keys()))
        if clientes:
            self.combo_cliente.set(list(self.clientes_dict.keys())[0])
        
        self._cargar_equipos()
    
    def _cargar_equipos(self):
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()
        
        equipos = self.equipo_use_cases.listar_equipos()
        
        if not equipos:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No hay equipos registrados",
                text_color="gray"
            ).grid(row=1, column=0, columnspan=6, pady=20)
            return
        
        clientes = {c.id: c.nombre for c in self.cliente_use_cases.listar_clientes()}
        
        for i, eq in enumerate(equipos, 1):
            ctk.CTkLabel(self.scroll_frame, text=str(eq.id)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=eq.tipo_equipo).grid(row=i, column=1, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=eq.marca).grid(row=i, column=2, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=eq.modelo or "-").grid(row=i, column=3, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=eq.serial or "-").grid(row=i, column=4, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=clientes.get(eq.cliente_id, "N/A")).grid(row=i, column=5, padx=5, pady=5, sticky="w")
    
    def _guardar_equipo(self):
        from application.dto.equipo_dto import EquipoCreateDTO
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        cliente_key = self.combo_cliente.get()
        cliente_id = self.clientes_dict.get(cliente_key)
        
        if not cliente_id:
            mostrar_mensaje(self, "Seleccione un cliente", "error")
            return
        
        tipo = self.combo_tipo.get()
        marca = self.entry_marca.get().strip()
        modelo = self.entry_modelo.get().strip()
        serial = self.entry_serial.get().strip()
        
        if not tipo or not marca:
            mostrar_mensaje(self, "Tipo y marca son obligatorios", "error")
            return
        
        try:
            dto = EquipoCreateDTO(
                tipo_equipo=tipo,
                marca=marca,
                modelo=modelo or None,
                serial=serial or None,
                cliente_id=cliente_id
            )
            self.equipo_use_cases.crear_equipo(dto)
            mostrar_mensaje(self, "Equipo guardado exitosamente", "success")
            self._limpiar_formulario()
            self._cargar_equipos()
        except Exception as e:
            mostrar_mensaje(self, f"Error: {str(e)}", "error")
    
    def _limpiar_formulario(self):
        self.entry_marca.delete(0, "end")
        self.entry_modelo.delete(0, "end")
        self.entry_serial.delete(0, "end")