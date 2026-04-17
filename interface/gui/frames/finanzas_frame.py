"""
Vista de Finanzas - Reportes de ingresos, egresos y utilidades.
"""

import customtkinter as ctk


class FinanzasFrame(ctk.CTkFrame):
    """Frame para gestión financiera del taller."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self._init_ui()
        self._cargar_datos()

    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_tarjetas()
        self._crear_detalles()

    def _crear_tarjetas(self):
        """Crea las tarjetas de resumen financiero."""
        tarjetas_frame = ctk.CTkFrame(self)
        tarjetas_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        tarjetas_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_ingresos = self._crear_tarjeta(
            tarjetas_frame, "Ingresos Totales", "$0.00", "#27ae60", 0
        )
        self.card_egresos = self._crear_tarjeta(
            tarjetas_frame, "Egresos", "$0.00", "#e74c3c", 1
        )
        self.card_utilidad = self._crear_tarjeta(
            tarjetas_frame, "Utilidad Neta", "$0.00", "#3498db", 2
        )
        self.card_tecnicos = self._crear_tarjeta(
            tarjetas_frame, "Pago Técnicos", "$0.00", "#9b59b6", 3
        )

    def _crear_tarjeta(self, parent, titulo, valor, color, col):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="ew")

        label_titulo = ctk.CTkLabel(
            frame, text=titulo, font=ctk.CTkFont(size=12), text_color="gray"
        )
        label_titulo.pack(pady=(0, 5))

        label_valor = ctk.CTkLabel(
            frame,
            text=valor,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=color,
        )
        label_valor.pack(pady=5)

        return label_valor

    def _crear_detalles(self):
        """Crea la sección de detalles."""
        detalles_frame = ctk.CTkFrame(self)
        detalles_frame.grid(row=1, column=0, sticky="nsew")
        detalles_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            detalles_frame,
            text="Detalle de Órdenes Terminadas",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        header.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.scroll_frame = ctk.CTkScrollableFrame(detalles_frame, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self._crear_encabezado_detalle()

    def _crear_encabezado_detalle(self):
        columnas = ["ID", "Fecha", "Equipo", "Técnico", "Costo"]

        headers = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        headers.grid(row=0, column=0, sticky="ew", columnspan=5)

        for i, col in enumerate(columnas):
            ctk.CTkLabel(
                headers, text=col, font=ctk.CTkFont(weight="bold"), text_color="#3498db"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")

    def _cargar_datos(self):
        """Carga los datos financieros desde el backend."""
        ordenes = self.orden_use_cases.listar_ordenes()
        ordenes_terminadas = [o for o in ordenes if o.estado.value == "terminado"]

        total_materiales = 0
        total_mano_obra = 0

        for o in ordenes_terminadas:
            items = self.orden_use_cases.obtener_materiales(o.id)
            total_materiales += sum(item.get_subtotal() for item in items)
            total_mano_obra += o.mano_obra

        ingresos = total_mano_obra + total_materiales
        costo_materiales = sum(
            item.cantidad * self._get_costo_repuesto(item.repuesto_id)
            for o in ordenes_terminadas
            for item in self.orden_use_cases.obtener_materiales(o.id)
        )
        utilidad = ingresos - costo_materiales
        pago_tecnicos = total_mano_obra * 0.5

        self.card_ingresos.configure(text=f"${ingresos:.2f}")
        self.card_egresos.configure(text=f"${costo_materiales:.2f}")
        self.card_utilidad.configure(text=f"${utilidad:.2f}")
        self.card_tecnicos.configure(text=f"${pago_tecnicos:.2f}")

        self._cargar_detalle_ordenes()

    def _get_costo_repuesto(self, repuesto_id):
        """Obtiene el costo de compra de un repuesto."""
        if self.repuesto_use_cases:
            repuesto = self.repuesto_use_cases.obtener_repuesto(repuesto_id)
            return repuesto.costo_compra if repuesto else 0
        return 0

    @property
    def orden_use_cases(self):
        return self.master.orden_use_cases

    @property
    def repuesto_use_cases(self):
        return getattr(self.master, "repuesto_use_cases", None)

    def _cargar_detalle_ordenes(self):
        """Carga el detalle de órdenes terminadas."""
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()

        ordenes = self.orden_use_cases.listar_ordenes()
        ordenes_terminadas = [o for o in ordenes if o.estado.value == "terminado"]

        if not ordenes_terminadas:
            ctk.CTkLabel(
                self.scroll_frame, text="No hay órdenes terminadas", text_color="gray"
            ).grid(row=1, column=0, columnspan=5, pady=20)
            return

        from domain.entities.orden_servicio import EstadoOrden

        for i, o in enumerate(ordenes_terminadas, 1):
            items = self.orden_use_cases.obtener_materiales(o.id)
            total_materiales = sum(item.get_subtotal() for item in items)
            total_orden = o.mano_obra + total_materiales

            ctk.CTkLabel(self.scroll_frame, text=str(o.id)).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )
            ctk.CTkLabel(
                self.scroll_frame, text=str(o.fecha_entrega or o.fecha_ingreso)
            ).grid(row=i, column=1, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(self.scroll_frame, text=f"M.Obra: ${o.mano_obra:.2f}").grid(
                row=i, column=2, padx=5, pady=5, sticky="w"
            )
            ctk.CTkLabel(self.scroll_frame, text=f"Mat: ${total_materiales:.2f}").grid(
                row=i, column=3, padx=5, pady=5, sticky="w"
            )
            ctk.CTkLabel(
                self.scroll_frame, text=f"${total_orden:.2f}", text_color="#27ae60"
            ).grid(row=i, column=4, padx=5, pady=5, sticky="w")
