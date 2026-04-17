from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from enum import Enum


class EstadoFactura(str, Enum):
    """Estados posibles de una factura."""

    PENDIENTE = "pendiente"
    PAGADA = "pagada"
    ANULADA = "anulada"


@dataclass
class Factura:
    """Entidad de dominio para Factura."""

    id: Optional[int] = None
    numero_factura: str = ""
    fecha: Optional[date] = None
    orden_id: int = 0
    cliente_id: int = 0
    equipo_id: int = 0
    tecnico_id: int = 0
    subtotal: float = 0.0
    iva: float = 0.0
    total: float = 0.0
    estado: EstadoFactura = EstadoFactura.PENDIENTE
    ruta_pdf: str = ""
    observaciones: str = ""

    def __post_init__(self):
        if self.orden_id is None or self.orden_id <= 0:
            raise ValueError("La orden es obligatoria")
        if self.cliente_id is None or self.cliente_id <= 0:
            raise ValueError("El cliente es obligatorio")
        if self.subtotal < 0:
            raise ValueError("El subtotal no puede ser negativo")
        if self.iva < 0:
            raise ValueError("El IVA no puede ser negativo")
        if self.total < 0:
            raise ValueError("El total no puede ser negativo")

    def calcular_total(self):
        """Calcula el total sumando subtotal e IVA."""
        self.total = self.subtotal + self.iva

    def marcar_pagada(self):
        """Marca la factura como pagada."""
        self.estado = EstadoFactura.PAGADA

    def marcar_pendiente(self):
        """Marca la factura como pendiente."""
        self.estado = EstadoFactura.PENDIENTE

    def anular(self):
        """Anula la factura."""
        if self.estado == EstadoFactura.PAGADA:
            raise ValueError("No se puede anular una factura pagada")
        self.estado = EstadoFactura.ANULADA

    def __str__(self):
        return f"Factura({self.numero_factura}): {self.estado.value}"
