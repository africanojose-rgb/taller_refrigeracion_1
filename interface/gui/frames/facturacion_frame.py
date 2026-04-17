"""
Vista de Facturación - Generar facturas y gestionar facturación.
"""

import customtkinter as ctk
import os
import subprocess
import platform
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


class FacturacionFrame(ctk.CTkFrame):
    """Frame para facturación y gestión de facturas."""

    def __init__(
        self,
        master,
        factura_use_cases,
        orden_use_cases,
        cliente_use_cases,
        equipo_use_cases,
        tecnico_use_cases,
        repuesto_use_cases=None,
    ):
        super().__init__(master, fg_color="transparent")

        self.factura_use_cases = factura_use_cases
        self.orden_use_cases = orden_use_cases
        self.cliente_use_cases = cliente_use_cases
        self.equipo_use_cases = equipo_use_cases
        self.tecnico_use_cases = tecnico_use_cases
        self.repuesto_use_cases = repuesto_use_cases

        self.facturas_folder = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            ),
            "data",
            "facturas",
        )

        if not os.path.exists(self.facturas_folder):
            os.makedirs(self.facturas_folder)

        self._init_ui()
        self._cargar_ordenes()
        self._cargar_facturas()

    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)

        self._crear_formulario()
        self._crear_tabla()

    def _crear_formulario(self):
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        form_frame.grid_columnconfigure(1, weight=1)

        titulo = ctk.CTkLabel(
            form_frame, text="Generar Factura", font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo.grid(row=0, column=0, columnspan=4, pady=10)

        ctk.CTkLabel(form_frame, text="Orden:*").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.combo_orden = ctk.CTkComboBox(form_frame)
        self.combo_orden.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(form_frame, text="IVA (%):").grid(
            row=1, column=2, padx=10, pady=5, sticky="w"
        )
        self.entry_iva = ctk.CTkEntry(form_frame, width=80)
        self.entry_iva.insert(0, "0")
        self.entry_iva.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Generar Factura",
            command=self._generar_factura,
            fg_color="#27ae60",
            hover_color="#229954",
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Abrir Carpeta",
            command=self._abrir_carpeta_facturas,
            fg_color="#3498db",
            hover_color="#2980b9",
        ).pack(side="left", padx=5)

    def _crear_tabla(self):
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            table_frame,
            text="Facturas Registradas",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.scroll_frame = ctk.CTkScrollableFrame(table_frame, label_text="")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self._crear_encabezado()

    def _crear_encabezado(self):
        columnas = ["Número", "Fecha", "Orden", "Cliente", "Total", "Estado"]

        headers = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        headers.grid(row=0, column=0, sticky="ew", columnspan=6)

        for i, col in enumerate(columnas):
            ctk.CTkLabel(
                headers, text=col, font=ctk.CTkFont(weight="bold"), text_color="#3498db"
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")

    def _cargar_ordenes(self):
        ordenes = self.orden_use_cases.listar_ordenes()
        ordenes_terminadas = [o for o in ordenes if o.estado.value == "terminado"]

        facturas_existentes = self.factura_use_cases.listar_facturas()
        ordenes_facturadas = {f.orden_id for f in facturas_existentes}

        self.ordenes_dict = {}
        for o in ordenes_terminadas:
            if o.id in ordenes_facturadas:
                continue
            try:
                equipo = self.equipo_use_cases.obtener_equipo(o.equipo_id)
                cliente = (
                    self.cliente_use_cases.obtener_cliente(equipo.cliente_id)
                    if equipo
                    else None
                )
                nombre_cliente = cliente.nombre if cliente else "Unknown"
                key = f"Orden #{o.id} - {nombre_cliente}"
                self.ordenes_dict[key] = o
            except:
                pass

        if self.ordenes_dict:
            self.combo_orden.configure(values=list(self.ordenes_dict.keys()))
            self.combo_orden.set(list(self.ordenes_dict.keys())[0])
        else:
            self.combo_orden.configure(values=["No hay órdenes para facturar"])
            self.combo_orden.set("No hay órdenes para facturar")

    def _cargar_facturas(self):
        for widget in self.scroll_frame.winfo_children():
            if widget.winfo_class() != "Frame":
                widget.destroy()

        facturas = self.factura_use_cases.listar_facturas()

        if not facturas:
            ctk.CTkLabel(
                self.scroll_frame, text="No hay facturas registradas", text_color="gray"
            ).grid(row=1, column=0, columnspan=6, pady=20)
            return

        for i, factura in enumerate(facturas[:20], 1):
            try:
                orden = self.orden_use_cases.obtener_orden(factura.orden_id)
                equipo = (
                    self.equipo_use_cases.obtener_equipo(factura.equipo_id)
                    if orden
                    else None
                )
                cliente = (
                    self.cliente_use_cases.obtener_cliente(equipo.cliente_id)
                    if equipo
                    else None
                )
                nombre_cliente = cliente.nombre if cliente else "-"
            except:
                nombre_cliente = "-"

            estado_color = (
                "#27ae60"
                if factura.estado.value == "pagada"
                else ("#e74c3c" if factura.estado.value == "anulada" else "#f39c12")
            )

            ctk.CTkLabel(self.scroll_frame, text=factura.numero_factura).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )
            ctk.CTkLabel(self.scroll_frame, text=str(factura.fecha)).grid(
                row=i, column=1, padx=5, pady=5, sticky="w"
            )
            ctk.CTkLabel(self.scroll_frame, text=f"Orden #{factura.orden_id}").grid(
                row=i, column=2, padx=5, pady=5, sticky="w"
            )
            ctk.CTkLabel(self.scroll_frame, text=nombre_cliente[:20]).grid(
                row=i, column=3, padx=5, pady=5, sticky="w"
            )
            ctk.CTkLabel(
                self.scroll_frame, text=f"${factura.total:.2f}", text_color="#27ae60"
            ).grid(row=i, column=4, padx=5, pady=5, sticky="w")
            ctk.CTkLabel(
                self.scroll_frame,
                text=factura.estado.value.upper(),
                text_color=estado_color,
            ).grid(row=i, column=5, padx=5, pady=5, sticky="w")

    def _generar_factura(self):
        from ..dialogs.mensaje_dialog import mostrar_mensaje

        orden_key = self.combo_orden.get()
        orden = self.ordenes_dict.get(orden_key)

        if not orden:
            mostrar_mensaje(self, "Seleccione una orden para facturar", "error")
            return

        try:
            iva = float(self.entry_iva.get() or 0) / 100

            from application.dto.factura_dto import GenerarFacturaDTO

            dto = GenerarFacturaDTO(orden_id=orden.id, iva=iva)

            factura = self.factura_use_cases.generar_factura(dto)

            equipo = self.equipo_use_cases.obtener_equipo(orden.equipo_id)
            cliente = (
                self.cliente_use_cases.obtener_cliente(equipo.cliente_id)
                if equipo
                else None
            )
            tecnico = self.tecnico_use_cases.obtener_tecnico(orden.tecnico_id)

            items = self.orden_use_cases.obtener_materiales(orden.id)

            ruta_pdf = self._generar_pdf(
                factura, orden, equipo, cliente, tecnico, items
            )

            factura.ruta_pdf = ruta_pdf
            from application.dto.factura_dto import FacturaUpdateDTO

            self.factura_use_cases.actualizar(factura.id, FacturaUpdateDTO())

            mostrar_mensaje(
                self,
                f"Factura {factura.numero_factura} generada exitosamente",
                "success",
            )
            self._cargar_ordenes()
            self._cargar_facturas()

        except Exception as e:
            mostrar_mensaje(self, f"Error al generar factura: {str(e)}", "error")

    def _generar_pdf(self, factura, orden, equipo, cliente, tecnico, items):
        nombre_archivo = (
            f"{factura.numero_factura}_{factura.fecha.strftime('%Y-%m-%d')}.pdf"
        )
        ruta_pdf = os.path.join(self.facturas_folder, nombre_archivo)

        c = canvas.Canvas(ruta_pdf, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 24)
        c.drawString(1 * inch, height - 1 * inch, "FACTURA")

        c.setFont("Helvetica-Bold", 16)
        c.drawString(5.5 * inch, height - 0.8 * inch, f"N° {factura.numero_factura}")

        c.setFont("Helvetica", 12)
        c.drawString(1 * inch, height - 1.5 * inch, f"Taller de Refrigeración Africano")
        c.drawString(
            1 * inch,
            height - 1.7 * inch,
            f"Fecha: {factura.fecha.strftime('%Y-%m-%d')}",
        )
        c.drawString(1 * inch, height - 1.9 * inch, f"Orden #: {orden.id}")

        c.line(1 * inch, height - 2 * inch, 7.5 * inch, height - 2 * inch)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(1 * inch, height - 2.5 * inch, "Datos del Cliente")

        c.setFont("Helvetica", 12)
        y = height - 2.8 * inch
        c.drawString(1 * inch, y, f"Cliente: {cliente.nombre if cliente else 'N/A'}")
        y -= 0.2 * inch
        c.drawString(1 * inch, y, f"Teléfono: {cliente.telefono if cliente else 'N/A'}")
        y -= 0.2 * inch
        c.drawString(
            1 * inch,
            y,
            f"Dirección: {cliente.direccion if cliente and cliente.direccion else 'N/A'}",
        )

        c.setFont("Helvetica-Bold", 14)
        y -= 0.5 * inch
        c.drawString(1 * inch, y, "Datos del Equipo")

        c.setFont("Helvetica", 12)
        y -= 0.3 * inch
        c.drawString(
            1 * inch,
            y,
            f"Equipo: {equipo.tipo_equipo} {equipo.marca} {equipo.modelo or ''}",
        )
        y -= 0.2 * inch
        c.drawString(1 * inch, y, f"Serial: {equipo.serial or 'N/A'}")
        y -= 0.2 * inch
        c.drawString(1 * inch, y, f"Técnico: {tecnico.nombre if tecnico else 'N/A'}")

        c.setFont("Helvetica-Bold", 14)
        y -= 0.5 * inch
        c.drawString(1 * inch, y, "Descripción de la Falla")

        c.setFont("Helvetica", 12)
        y -= 0.3 * inch
        c.drawString(1 * inch, y, f"{orden.descripcion_falla or 'N/A'}")

        c.setFont("Helvetica-Bold", 14)
        y -= 0.5 * inch
        c.drawString(1 * inch, y, "Diagnóstico y Solución")

        c.setFont("Helvetica", 12)
        y -= 0.3 * inch
        c.drawString(1 * inch, y, f"Diagnóstico: {orden.diagnostico or 'N/A'}")
        y -= 0.2 * inch
        c.drawString(1 * inch, y, f"Solución: {orden.solucion or 'N/A'}")

        c.setFont("Helvetica-Bold", 14)
        y -= 0.5 * inch
        c.drawString(1 * inch, y, "Detalle de Servicios")

        y -= 0.3 * inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(1 * inch, y, "Descripción")
        c.drawString(4 * inch, y, "Cantidad")
        c.drawString(5 * inch, y, "P. Unitario")
        c.drawString(6.5 * inch, y, "Subtotal")

        y -= 0.25 * inch
        c.line(1 * inch, y, 7.5 * inch, y)
        y -= 0.2 * inch

        c.setFont("Helvetica", 11)
        c.drawString(1 * inch, y, "Mano de Obra")
        c.drawString(4 * inch, y, "1")
        c.drawString(5 * inch, y, f"${orden.mano_obra:.2f}")
        c.drawString(6.5 * inch, y, f"${orden.mano_obra:.2f}")

        y -= 0.3 * inch

        for item in items:
            c.drawString(1 * inch, y, f"Repuesto #{item.repuesto_id}")
            c.drawString(4 * inch, y, str(item.cantidad))
            c.drawString(5 * inch, y, f"${item.precio_unitario:.2f}")
            c.drawString(6.5 * inch, y, f"${item.get_subtotal():.2f}")
            y -= 0.25 * inch

        y += 0.1 * inch
        c.line(1 * inch, y, 7.5 * inch, y)
        y -= 0.25 * inch

        c.setFont("Helvetica-Bold", 12)
        c.drawString(5 * inch, y, "SUBTOTAL:")
        c.drawString(6.5 * inch, y, f"${factura.subtotal:.2f}")

        y -= 0.25 * inch
        c.drawString(5 * inch, y, f"IVA ({factura.iva / factura.subtotal * 100:.0f}%):")
        c.drawString(6.5 * inch, y, f"${factura.iva:.2f}")

        y -= 0.3 * inch
        c.setFont("Helvetica-Bold", 14)
        c.drawString(5 * inch, y, "TOTAL:")
        c.drawString(6.5 * inch, y, f"${factura.total:.2f}")

        c.save()

        return ruta_pdf

    def _abrir_carpeta_facturas(self):
        from ..dialogs.mensaje_dialog import mostrar_mensaje

        if not os.path.exists(self.facturas_folder):
            os.makedirs(self.facturas_folder)

        try:
            if platform.system() == "Windows":
                os.startfile(self.facturas_folder)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", self.facturas_folder])
            else:
                subprocess.Popen(["xdg-open", self.facturas_folder])
        except Exception as e:
            mostrar_mensaje(self, f"Error al abrir carpeta: {str(e)}", "error")
