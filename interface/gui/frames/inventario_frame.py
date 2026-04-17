"""
Vista de Inventario - Gestión de repuestos.
"""
import customtkinter as ctk


class InventarioFrame(ctk.CTkFrame):
    """Frame para gestión de inventario/repuestos."""
    
    def __init__(self, master, repuesto_use_cases):
        super().__init__(master, fg_color="transparent")
        
        self.repuesto_use_cases = repuesto_use_cases
        
        self._init_ui()
        self._cargar_repuestos()
    
    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        self._crear_formulario()
        self._crear_tabla()
    
    def _crear_formulario(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        form_frame.grid_columnconfigure((1, 2, 3, 4), weight=1)
        
        titulo = ctk.CTkLabel(
            form_frame,
            text="Nuevo Repuesto",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=6, pady=10)
        
        ctk.CTkLabel(form_frame, text="Nombre:*").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Nombre del repuesto")
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Código:*").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.entry_codigo = ctk.CTkEntry(form_frame, placeholder_text="Código único")
        self.entry_codigo.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Descripción:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_descripcion = ctk.CTkEntry(form_frame, placeholder_text="Descripción")
        self.entry_descripcion.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Costo Compra:*").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_costo = ctk.CTkEntry(form_frame, placeholder_text="0.00")
        self.entry_costo.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Precio Venta:*").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.entry_precio = ctk.CTkEntry(form_frame, placeholder_text="0.00")
        self.entry_precio.grid(row=3, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Cantidad:*").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_cantidad = ctk.CTkEntry(form_frame, placeholder_text="0")
        self.entry_cantidad.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Stock Mín:").grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.entry_stock_min = ctk.CTkEntry(form_frame, placeholder_text="5")
        self.entry_stock_min.grid(row=4, column=3, padx=10, pady=5, sticky="ew")
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=4, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Guardar Repuesto",
            command=self._guardar_repuesto,
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
        
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="Inventario de Repuestos",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.entry_buscar = ctk.CTkEntry(
            header_frame,
            placeholder_text="Buscar por nombre o código...",
            width=250
        )
        self.entry_buscar.pack(side="right", padx=10)
        self.entry_buscar.bind("<KeyRelease>", lambda e: self._buscar_repuesto())
        
        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        self._crear_encabezado()
    
    def _crear_encabezado(self):
        columnas = ["Código", "Nombre", "Costo", "Precio", "Stock", "Margen", "Acción"]
        
        headers = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        headers.grid(row=0, column=0, sticky="ew", columnspan=7)
        
        for i, col in enumerate(columnas):
            ctk.CTkLabel(
                headers,
                text=col,
                font=ctk.CTkFont(weight="bold"),
                text_color="#3498db"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")
    
    def _guardar_repuesto(self):
        from application.dto.repuesto_dto import RepuestoCreateDTO
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        nombre = self.entry_nombre.get().strip()
        codigo = self.entry_codigo.get().strip().upper()
        descripcion = self.entry_descripcion.get().strip()
        
        try:
            costo = float(self.entry_costo.get().strip() or 0)
            precio = float(self.entry_precio.get().strip() or 0)
            cantidad = int(self.entry_cantidad.get().strip() or 0)
            stock_min = int(self.entry_stock_min.get().strip() or 5)
        except ValueError:
            mostrar_mensaje(self, "Verifique los valores numéricos", "error")
            return
        
        if not nombre or not codigo:
            mostrar_mensaje(self, "Nombre y código son obligatorios", "error")
            return
        
        try:
            dto = RepuestoCreateDTO(
                nombre=nombre,
                codigo=codigo,
                descripcion=descripcion or None,
                costo_compra=costo,
                precio_venta=precio,
                cantidad_stock=cantidad,
                cantidad_minima=stock_min
            )
            self.repuesto_use_cases.crear_repuesto(dto)
            mostrar_mensaje(self, "Repuesto guardado exitosamente", "success")
            self._limpiar_formulario()
            self._cargar_repuestos()
        except Exception as e:
            mostrar_mensaje(self, f"Error: {str(e)}", "error")
    
    def _limpiar_formulario(self):
        self.entry_nombre.delete(0, "end")
        self.entry_codigo.delete(0, "end")
        self.entry_descripcion.delete(0, "end")
        self.entry_costo.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_cantidad.delete(0, "end")
        self.entry_stock_min.delete(0, "end")
    
    def _cargar_repuestos(self):
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()
        
        repuestos = self.repuesto_use_cases.listar_repuestos()
        
        if not repuestos:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No hay repuestos registrados",
                text_color="gray"
            ).grid(row=1, column=0, columnspan=7, pady=20)
            return
        
        for i, r in enumerate(repuestos, 1):
            margen = r.get_margen()
            color_margen = "#27ae60" if margen > 0 else "#e74c3c"
            color_stock = "#e74c3c" if r.necesita_reorden() else "white"
            
            ctk.CTkLabel(self.scroll_frame, text=r.codigo).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=r.nombre[:25]).grid(row=i, column=1, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"${r.costo_compra:.2f}").grid(row=i, column=2, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"${r.precio_venta:.2f}").grid(row=i, column=3, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=str(r.cantidad_stock), text_color=color_stock).grid(row=i, column=4, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"{margen:.1f}%", text_color=color_margen).grid(row=i, column=5, padx=5, pady=5, sticky="w")
            
            btn = ctk.CTkButton(
                self.scroll_frame,
                text="Ajustar",
                command=lambda rep=r: self._ajustar_stock(rep),
                width=70,
                height=25,
                fg_color="#3498db",
                hover_color="#2980b9"
            )
            btn.grid(row=i, column=6, padx=5, pady=5)
    
    def _buscar_repuesto(self):
        termino = self.entry_buscar.get().strip()
        
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()
        
        if termino:
            repuestos = self.repuesto_use_cases.buscar_por_nombre(termino)
            if not repuestos:
                repuesto = self.repuesto_use_cases.buscar_por_codigo(termino)
                repuestos = [repuesto] if repuesto else []
        else:
            repuestos = self.repuesto_use_cases.listar_repuestos()
        
        if not repuestos:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No se encontraron resultados",
                text_color="gray"
            ).grid(row=1, column=0, columnspan=7, pady=20)
            return
        
        for i, r in enumerate(repuestos, 1):
            if r:
                margen = r.get_margen()
                color_margen = "#27ae60" if margen > 0 else "#e74c3c"
                color_stock = "#e74c3c" if r.necesita_reorden() else "white"
                
                ctk.CTkLabel(self.scroll_frame, text=r.codigo).grid(row=i, column=0, padx=5, pady=5, sticky="w")
                ctk.CTkLabel(self.scroll_frame, text=r.nombre[:25]).grid(row=i, column=1, padx=5, pady=5, sticky="w")
                ctk.CTkLabel(self.scroll_frame, text=f"${r.costo_compra:.2f}").grid(row=i, column=2, padx=5, pady=5, sticky="w")
                ctk.CTkLabel(self.scroll_frame, text=f"${r.precio_venta:.2f}").grid(row=i, column=3, padx=5, pady=5, sticky="w")
                ctk.CTkLabel(self.scroll_frame, text=str(r.cantidad_stock), text_color=color_stock).grid(row=i, column=4, padx=5, pady=5, sticky="w")
                ctk.CTkLabel(self.scroll_frame, text=f"{margen:.1f}%", text_color=color_margen).grid(row=i, column=5, padx=5, pady=5, sticky="w")
                
                btn = ctk.CTkButton(
                    self.scroll_frame,
                    text="Ajustar",
                    command=lambda rep=r: self._ajustar_stock(rep),
                    width=70,
                    height=25,
                    fg_color="#3498db",
                    hover_color="#2980b9"
                )
                btn.grid(row=i, column=6, padx=5, pady=5)
    
    def _ajustar_stock(self, repuesto):
        from ..dialogs.mensaje_dialog import mostrar_mensaje
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Ajustar Stock - {repuesto.nombre}")
        dialog.geometry("350x180")
        dialog.transient(self)
        dialog.update()
        
        ctk.CTkLabel(dialog, text=f"Stock actual: {repuesto.cantidad_stock}", font=ctk.CTkFont(size=14)).pack(pady=15)
        
        ctk.CTkLabel(dialog, text="Cantidad a agregar (negativo para quitar):").pack(pady=5)
        entry_cantidad = ctk.CTkEntry(dialog, width=200)
        entry_cantidad.pack(pady=5)
        
        def ajustar():
            try:
                cantidad = int(entry_cantidad.get().strip())
                self.repuesto_use_cases.ajustar_stock(repuesto.id, cantidad)
                dialog.destroy()
                mostrar_mensaje(self, "Stock actualizado", "success")
                self._cargar_repuestos()
            except Exception as e:
                mostrar_mensaje(self, f"Error: {str(e)}", "error")
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="Guardar", command=ajustar, fg_color="#27ae60", hover_color="#229954").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancelar", command=dialog.destroy, fg_color="#e74c3c", hover_color="#c0392b").pack(side="left", padx=5)