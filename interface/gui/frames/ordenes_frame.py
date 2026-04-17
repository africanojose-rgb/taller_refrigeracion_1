"""
Vista de Órdenes de Servicio - CRUD + materiales + mano de obra.
"""
import customtkinter as ctk


class OrdenesFrame(ctk.CTkFrame):
    """Frame para gestión de órdenes de servicio."""
    
    def __init__(self, master, orden_use_cases, equipo_use_cases, tecnico_use_cases, repuesto_use_cases=None):
        super().__init__(master, fg_color="transparent")
        
        self.orden_use_cases = orden_use_cases
        self.equipo_use_cases = equipo_use_cases
        self.tecnico_use_cases = tecnico_use_cases
        self.repuesto_use_cases = repuesto_use_cases
        
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
            text="Nueva Orden de Servicio",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=10)
        
        ctk.CTkLabel(form_frame, text="Equipo:*").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.combo_equipo = ctk.CTkComboBox(form_frame)
        self.combo_equipo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Técnico:*").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.combo_tecnico = ctk.CTkComboBox(form_frame)
        self.combo_tecnico.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Descripción Falla:*").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_falla = ctk.CTkEntry(form_frame, placeholder_text="Descripción de la falla reportada")
        self.entry_falla.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Crear Orden",
            command=self._crear_orden,
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
            text="Órdenes de Servicio",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        self._crear_encabezado()
    
    def _crear_encabezado(self):
        columnas = ["ID", "Fecha", "Estado", "Falla", "Técnico", "M.Obra", "Materiales", "Acción"]
        
        headers = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        headers.grid(row=0, column=0, sticky="ew", columnspan=8)
        
        for i, col in enumerate(columnas):
            ctk.CTkLabel(
                headers,
                text=col,
                font=ctk.CTkFont(weight="bold"),
                text_color="#3498db"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
    def _cargar_datos(self):
        equipos = self.equipo_use_cases.listar_equipos()
        self.equipos_dict = {f"{e.tipo_equipo} {e.marca} (ID: {e.id})": e.id for e in equipos}
        self.combo_equipo.configure(values=list(self.equipos_dict.keys()) if equipos else ["Sin equipos"])
        if equipos:
            self.combo_equipo.set(list(self.equipos_dict.keys())[0])
        
        tecnicos = self.tecnico_use_cases.listar_tecnicos()
        self.tecnicos_dict = {f"{t.nombre} ({t.especialidad})": t.id for t in tecnicos}
        self.combo_tecnico.configure(values=list(self.tecnicos_dict.keys()) if tecnicos else ["Sin técnicos"])
        if tecnicos:
            self.combo_tecnico.set(list(self.tecnicos_dict.keys())[0])
        
        self._cargar_ordenes()
    
    def _cargar_ordenes(self):
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()
        
        ordenes = self.orden_use_cases.listar_ordenes()
        
        if not ordenes:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No hay órdenes registradas",
                text_color="gray"
            ).grid(row=1, column=0, columnspan=8, pady=20)
            return
        
        tecnicos = {t.id: t.nombre for t in self.tecnico_use_cases.listar_tecnicos()}
        
        for i, o in enumerate(ordenes, 1):
            estado_color = self._get_estado_color(o.estado.value)
            
            items = self.orden_use_cases.obtener_materiales(o.id) if self.repuesto_use_cases else []
            total_materiales = sum(item.get_subtotal() for item in items)
            
            falla = (o.descripcion_falla[:15] + "...") if o.descripcion_falla and len(o.descripcion_falla) > 15 else (o.descripcion_falla or "-")
            
            ctk.CTkLabel(self.scroll_frame, text=str(o.id)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=str(o.fecha_ingreso)).grid(row=i, column=1, padx=5, pady=5, sticky="w")
            
            estado_label = ctk.CTkLabel(
                self.scroll_frame,
                text=o.estado.value.upper(),
                text_color=estado_color,
                font=ctk.CTkFont(weight="bold")
            )
            estado_label.grid(row=i, column=2, padx=5, pady=5, sticky="w")
            
            ctk.CTkLabel(self.scroll_frame, text=falla).grid(row=i, column=3, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=tecnicos.get(o.tecnico_id, "N/A")).grid(row=i, column=4, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"${o.mano_obra:.2f}").grid(row=i, column=5, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"${total_materiales:.2f}").grid(row=i, column=6, padx=5, pady=5, sticky="w")
            
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=self._get_accion_texto(o.estado.value),
                command=lambda oo=o: self._cambiar_estado(oo),
                width=80,
                height=25,
                fg_color=self._get_accion_color(o.estado.value),
                hover_color=self._get_accion_hover(o.estado.value)
            )
            btn.grid(row=i, column=7, padx=5, pady=5)
    
    def _get_estado_color(self, estado):
        colors = {
            "pendiente": "#f39c12",
            "en_proceso": "#3498db",
            "terminado": "#27ae60",
            "cancelado": "#e74c3c"
        }
        return colors.get(estado, "white")
    
    def _get_accion_texto(self, estado):
        textos = {
            "pendiente": "Iniciar",
            "en_proceso": "Completar",
            "terminado": "Ver"
        }
        return textos.get(estado, "...")
    
    def _get_accion_color(self, estado):
        colors = {
            "pendiente": "#3498db",
            "en_proceso": "#27ae60",
            "terminado": "#7f8c8d"
        }
        return colors.get(estado, "#7f8c8d")
    
    def _get_accion_hover(self, estado):
        colors = {
            "pendiente": "#2980b9",
            "en_proceso": "#229954",
            "terminado": "#626567"
        }
        return colors.get(estado, "#626567")
    
    def _crear_orden(self):
        from application.dto.orden_dto import OrdenCreateDTO
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        equipo_key = self.combo_equipo.get()
        equipo_id = self.equipos_dict.get(equipo_key)
        
        tecnico_key = self.combo_tecnico.get()
        tecnico_id = self.tecnicos_dict.get(tecnico_key)
        
        if not equipo_id or not tecnico_id:
            mostrar_mensaje(self, "Seleccione equipo y técnico", "error")
            return
        
        falla = self.entry_falla.get().strip()
        
        if not falla:
            mostrar_mensaje(self, "La descripción de la falla es obligatoria", "error")
            return
        
        try:
            dto = OrdenCreateDTO(
                descripcion_falla=falla,
                equipo_id=equipo_id,
                tecnico_id=tecnico_id
            )
            self.orden_use_cases.crear_orden(dto)
            mostrar_mensaje(self, "Orden creada exitosamente", "success")
            self._limpiar_formulario()
            self._cargar_ordenes()
        except Exception as e:
            mostrar_mensaje(self, f"Error: {str(e)}", "error")
    
    def _cambiar_estado(self, orden):
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        try:
            if orden.estado.value == "pendiente":
                self.orden_use_cases.iniciar_orden(orden.id)
                mostrar_mensaje(self, "Orden iniciada", "success")
            elif orden.estado.value == "en_proceso":
                self._mostrar_completar_dialog(orden)
                return
            elif orden.estado.value == "terminado":
                self._mostrar_detalles_dialog(orden)
                return
            
            self._cargar_ordenes()
        except Exception as e:
            mostrar_mensaje(self, f"Error: {str(e)}", "error")
    
    def _mostrar_completar_dialog(self, orden):
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Completar Orden")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.update()
        
        ctk.CTkLabel(dialog, text="Completar Orden de Servicio", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        
        ctk.CTkLabel(dialog, text="Diagnóstico:").pack(pady=(10, 3))
        entry_diagnostico = ctk.CTkEntry(dialog, width=450)
        entry_diagnostico.pack(pady=3)
        
        ctk.CTkLabel(dialog, text="Solución:").pack(pady=(10, 3))
        entry_solucion = ctk.CTkEntry(dialog, width=450)
        entry_solucion.pack(pady=3)
        
        ctk.CTkLabel(dialog, text="Mano de Obra ($):").pack(pady=(10, 3))
        entry_mano_obra = ctk.CTkEntry(dialog, width=450)
        entry_mano_obra.insert(0, "0.00")
        entry_mano_obra.pack(pady=3)
        
        ctk.CTkLabel(dialog, text="Agregar Materiales:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        
        self.materiales_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        self.materiales_frame.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(self.materiales_frame, text="Repuesto:").pack(side="left")
        
        self.combo_repuestos = ctk.CTkComboBox(self.materiales_frame, width=200)
        self.combo_repuestos.pack(side="left", padx=5)
        
        self.entry_cantidad_material = ctk.CTkEntry(self.materiales_frame, width=60, placeholder_text="Qty")
        self.entry_cantidad_material.pack(side="left", padx=5)
        
        def agregar_material():
            if not self.repuesto_use_cases:
                mostrar_mensaje(self, "Módulo de inventario no disponible", "error")
                return
            
            repuesto_key = self.combo_repuestos.get()
            if not repuesto_key:
                return
            
            repuesto = self.repuesto_use_cases.obtener_repuesto(repuesto_id)
            repuesto_id = None
            
            for r in self.repuesto_use_cases.listar_repuestos():
                key = f"{r.codigo} - {r.nombre}"
                if key == repuesto_key:
                    repuesto_id = r.id
                    break
            
            if not repuesto_id:
                return
            
            try:
                cantidad = int(self.entry_cantidad_material.get().strip() or 1)
                from application.dto.orden_dto import ItemOrdenDTO
                dto = ItemOrdenDTO(
                    repuesto_id=repuesto_id,
                    cantidad=cantidad,
                    precio_unitario=repuesto.precio_venta if repuesto else 0
                )
                self.orden_use_cases.agregar_material(orden.id, dto)
                mostrar_mensaje(self, "Material agregado", "success")
                self.entry_cantidad_material.delete(0, "end")
            except Exception as e:
                mostrar_mensaje(self, f"Error: {str(e)}", "error")
        
        ctk.CTkButton(self.materiales_frame, text="+", command=agregar_material, width=40).pack(side="left", padx=5)
        
        if self.repuesto_use_cases:
            repuestos = self.repuesto_use_cases.listar_repuestos()
            self.repuestos_dict = {f"{r.codigo} - {r.nombre}": r for r in repuestos}
            self.combo_repuestos.configure(values=list(self.repuestos_dict.keys()))
        
        def completar():
            try:
                from application.dto.orden_dto import OrdenCompletarDTO
                dto = OrdenCompletarDTO(
                    diagnostico=entry_diagnostico.get().strip(),
                    solucion=entry_solucion.get().strip(),
                    mano_obra=float(entry_mano_obra.get().strip() or 0)
                )
                self.orden_use_cases.completar_orden(orden.id, dto)
                dialog.destroy()
                mostrar_mensaje(self, "Orden completada", "success")
                self._cargar_ordenes()
            except Exception as e:
                mostrar_mensaje(self, f"Error: {str(e)}", "error")
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Completar", command=completar, fg_color="#27ae60", hover_color="#229954").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancelar", command=dialog.destroy, fg_color="#e74c3c", hover_color="#c0392b").pack(side="left", padx=5)
    
    def _mostrar_detalles_dialog(self, orden):
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        items = self.orden_use_cases.obtener_materiales(orden.id)
        total_materiales = sum(item.get_subtotal() for item in items)
        total = orden.mano_obra + total_materiales
        
        info = f"=== ORDEN #{orden.id} ===\n\n"
        info += f"Falla: {orden.descripcion_falla}\n"
        info += f"Diagnóstico: {orden.diagnostico}\n"
        info += f"Solución: {orden.solucion}\n\n"
        info += f"Mano de Obra: ${orden.mano_obra:.2f}\n"
        info += f"Materiales: ${total_materiales:.2f}\n"
        info += f"TOTAL: ${total:.2f}"
        
        mostrar_mensaje(self, info, "info")
    
    def _limpiar_formulario(self):
        self.entry_falla.delete(0, "end")