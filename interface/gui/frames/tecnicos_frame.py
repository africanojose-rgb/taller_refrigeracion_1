"""
Vista de Técnicos - CRUD simple.
"""
import customtkinter as ctk


class TecnicosFrame(ctk.CTkFrame):
    """Frame para gestión de técnicos."""
    
    def __init__(self, master, tecnico_use_cases):
        super().__init__(master, fg_color="transparent")
        
        self.tecnico_use_cases = tecnico_use_cases
        
        self._init_ui()
        self._cargar_tecnicos()
    
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
            text="Nuevo Técnico",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=10)
        
        ctk.CTkLabel(form_frame, text="Nombre:*").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo")
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Especialidad:*").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.combo_especialidad = ctk.CTkComboBox(
            form_frame,
            values=["Refrigeración Doméstica", "Aire Acondicionado", "Comercial", "Industrial", "Otro"]
        )
        self.combo_especialidad.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Teléfono:*").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_telefono = ctk.CTkEntry(form_frame, placeholder_text="Teléfono")
        self.entry_telefono.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Guardar Técnico",
            command=self._guardar_tecnico,
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
            text="Lista de Técnicos",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self._crear_encabezado()
    
    def _crear_encabezado(self):
        columnas = ["ID", "Nombre", "Especialidad", "Teléfono"]
        
        headers = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        headers.grid(row=0, column=0, sticky="ew", columnspan=4)
        
        for i, col in enumerate(columnas):
            ctk.CTkLabel(
                headers,
                text=col,
                font=ctk.CTkFont(weight="bold"),
                text_color="#3498db"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
    def _cargar_tecnicos(self):
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()
        
        tecnicos = self.tecnico_use_cases.listar_tecnicos()
        
        if not tecnicos:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No hay técnicos registrados",
                text_color="gray"
            ).grid(row=1, column=0, columnspan=4, pady=20)
            return
        
        for i, t in enumerate(tecnicos, 1):
            ctk.CTkLabel(self.scroll_frame, text=str(t.id)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=t.nombre).grid(row=i, column=1, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=t.especialidad).grid(row=i, column=2, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=t.telefono).grid(row=i, column=3, padx=5, pady=5, sticky="w")
    
    def _guardar_tecnico(self):
        from application.dto.tecnico_dto import TecnicoCreateDTO
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        nombre = self.entry_nombre.get().strip()
        especialidad = self.combo_especialidad.get()
        telefono = self.entry_telefono.get().strip()
        
        if not nombre or not telefono:
            mostrar_mensaje(self, "Nombre y teléfono son obligatorios", "error")
            return
        
        try:
            dto = TecnicoCreateDTO(
                nombre=nombre,
                especialidad=especialidad,
                telefono=telefono
            )
            self.tecnico_use_cases.crear_tecnico(dto)
            mostrar_mensaje(self, "Técnico guardado exitosamente", "success")
            self._limpiar_formulario()
            self._cargar_tecnicos()
        except Exception as e:
            mostrar_mensaje(self, f"Error: {str(e)}", "error")
    
    def _limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_telefono.delete(0, "end")