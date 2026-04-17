from domain.entities.factura import Factura, EstadoFactura
from domain.repositories.factura_repository import FacturaRepository
from domain.repositories.orden_repository import OrdenRepository
from domain.repositories.item_orden_repository import ItemOrdenRepository
from application.dto.factura_dto import (
    FacturaCreateDTO,
    FacturaUpdateDTO,
    GenerarFacturaDTO,
)
from typing import List, Optional
from datetime import date
import os
from pathlib import Path


class FacturaUseCases:
    """Casos de uso para la gestión de facturas."""

    def __init__(
        self,
        factura_repo: FacturaRepository,
        orden_repo: OrdenRepository,
        item_repo: ItemOrdenRepository,
    ):
        self._factura_repo = factura_repo
        self._orden_repo = orden_repo
        self._item_repo = item_repo

    def _generar_numero_factura(self) -> str:
        """Genera el siguiente número de factura secuencial."""
        ultimo = self._factura_repo.obtener_ultimo_numero()

        if ultimo and ultimo.startswith("FAC-"):
            try:
                num = int(ultimo.split("-")[1])
                return f"FAC-{num + 1:04d}"
            except (ValueError, IndexError):
                pass

        return "FAC-0001"

    def generar_factura(self, dto: GenerarFacturaDTO) -> Factura:
        """Genera una nueva factura a partir de una orden terminada."""
        orden = self._orden_repo.obtener_por_id(dto.orden_id)
        if not orden:
            raise ValueError(f"Orden con ID {dto.orden_id} no encontrada")

        if orden.estado.value != "terminado":
            raise ValueError("Solo se pueden facturar órdenes terminadas")

        existente = self._factura_repo.obtener_por_orden(dto.orden_id)
        if existente:
            raise ValueError(f"Ya existe una factura para la orden {dto.orden_id}")

        items = self._item_repo.obtener_por_orden(dto.orden_id)

        subtotal = orden.mano_obra
        for item in items:
            subtotal += item.get_subtotal()

        iva = round(subtotal * dto.iva, 2)
        total = subtotal + iva

        numero = self._generar_numero_factura()

        factura = Factura(
            numero_factura=numero,
            fecha=date.today(),
            orden_id=dto.orden_id,
            cliente_id=orden.equipo_id,
            equipo_id=orden.equipo_id,
            tecnico_id=orden.tecnico_id,
            subtotal=subtotal,
            iva=iva,
            total=total,
            estado=EstadoFactura.PENDIENTE,
            observaciones=dto.observaciones or "",
        )

        return self._factura_repo.crear(factura)

    def obtener_factura(self, factura_id: int) -> Optional[Factura]:
        return self._factura_repo.obtener_por_id(factura_id)

    def obtener_por_orden(self, orden_id: int) -> Optional[Factura]:
        return self._factura_repo.obtener_por_orden(orden_id)

    def listar_facturas(self) -> List[Factura]:
        return self._factura_repo.obtener_todos()

    def listar_por_cliente(self, cliente_id: int) -> List[Factura]:
        return self._factura_repo.buscar_por_cliente(cliente_id)

    def listar_por_estado(self, estado: str) -> List[Factura]:
        return self._factura_repo.obtener_por_estado(estado)

    def marcar_pagada(self, factura_id: int) -> Factura:
        factura = self._factura_repo.obtener_por_id(factura_id)
        if not factura:
            raise ValueError(f"Factura con ID {factura_id} no encontrada")

        factura.marcar_pagada()
        return self._factura_repo.actualizar(factura)

    def marcar_pendiente(self, factura_id: int) -> Factura:
        factura = self._factura_repo.obtener_por_id(factura_id)
        if not factura:
            raise ValueError(f"Factura con ID {factura_id} no encontrada")

        factura.marcar_pendiente()
        return self._factura_repo.actualizar(factura)

    def actualizar(self, factura_id: int, dto: FacturaUpdateDTO) -> Factura:
        factura = self._factura_repo.obtener_por_id(factura_id)
        if not factura:
            raise ValueError(f"Factura con ID {factura_id} no encontrada")

        if dto.subtotal is not None:
            factura.subtotal = dto.subtotal
        if dto.iva is not None:
            factura.iva = dto.iva
        if dto.observaciones is not None:
            factura.observaciones = dto.observaciones

        factura.calcular_total()
        return self._factura_repo.actualizar(factura)

    def eliminar(self, factura_id: int) -> bool:
        factura = self._factura_repo.obtener_por_id(factura_id)
        if not factura:
            return False

        if factura.estado == EstadoFactura.PAGADA:
            raise ValueError("No se puede eliminar una factura pagada")

        return self._factura_repo.eliminar(factura_id)
