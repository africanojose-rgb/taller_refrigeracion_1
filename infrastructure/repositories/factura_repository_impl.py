from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.factura import Factura, EstadoFactura
from domain.repositories.factura_repository import FacturaRepository
from infrastructure.models.models import FacturaModel, EstadoFacturaEnum


class FacturaRepositoryImpl(FacturaRepository):
    def __init__(self, session: Session):
        self._session = session

    def _to_entity(self, model: FacturaModel) -> Factura:
        return Factura(
            id=model.id,
            numero_factura=model.numero_factura,
            fecha=model.fecha,
            orden_id=model.orden_id,
            cliente_id=model.cliente_id,
            equipo_id=model.equipo_id,
            tecnico_id=model.tecnico_id,
            subtotal=model.subtotal,
            iva=model.iva,
            total=model.total,
            estado=EstadoFactura(model.estado.value),
            ruta_pdf=model.ruta_pdf or "",
            observaciones=model.observaciones or "",
        )

    def _to_model(self, factura: Factura) -> FacturaModel:
        return FacturaModel(
            id=factura.id,
            numero_factura=factura.numero_factura,
            fecha=factura.fecha,
            orden_id=factura.orden_id,
            cliente_id=factura.cliente_id,
            equipo_id=factura.equipo_id,
            tecnico_id=factura.tecnico_id,
            subtotal=factura.subtotal,
            iva=factura.iva,
            total=factura.total,
            estado=EstadoFacturaEnum(factura.estado.value),
            ruta_pdf=factura.ruta_pdf,
            observaciones=factura.observaciones,
        )

    def crear(self, factura: Factura) -> Factura:
        model = self._to_model(factura)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def obtener_por_id(self, factura_id: int) -> Optional[Factura]:
        model = (
            self._session.query(FacturaModel)
            .filter(FacturaModel.id == factura_id)
            .first()
        )
        return self._to_entity(model) if model else None

    def obtener_por_numero(self, numero_factura: str) -> Optional[Factura]:
        model = (
            self._session.query(FacturaModel)
            .filter(FacturaModel.numero_factura == numero_factura)
            .first()
        )
        return self._to_entity(model) if model else None

    def obtener_por_orden(self, orden_id: int) -> Optional[Factura]:
        model = (
            self._session.query(FacturaModel)
            .filter(FacturaModel.orden_id == orden_id)
            .first()
        )
        return self._to_entity(model) if model else None

    def obtener_todos(self) -> List[Factura]:
        models = (
            self._session.query(FacturaModel).order_by(FacturaModel.fecha.desc()).all()
        )
        return [self._to_entity(m) for m in models]

    def buscar_por_cliente(self, cliente_id: int) -> List[Factura]:
        models = (
            self._session.query(FacturaModel)
            .filter(FacturaModel.cliente_id == cliente_id)
            .order_by(FacturaModel.fecha.desc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    def obtener_por_estado(self, estado: str) -> List[Factura]:
        models = (
            self._session.query(FacturaModel)
            .filter(FacturaModel.estado == EstadoFacturaEnum(estado))
            .order_by(FacturaModel.fecha.desc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    def obtener_ultimo_numero(self) -> Optional[str]:
        model = (
            self._session.query(FacturaModel).order_by(FacturaModel.id.desc()).first()
        )
        return model.numero_factura if model else None

    def actualizar(self, factura: Factura) -> Factura:
        model = (
            self._session.query(FacturaModel)
            .filter(FacturaModel.id == factura.id)
            .first()
        )
        if not model:
            raise ValueError(f"Factura con ID {factura.id} no encontrada")

        model.numero_factura = factura.numero_factura
        model.fecha = factura.fecha
        model.orden_id = factura.orden_id
        model.cliente_id = factura.cliente_id
        model.equipo_id = factura.equipo_id
        model.tecnico_id = factura.tecnico_id
        model.subtotal = factura.subtotal
        model.iva = factura.iva
        model.total = factura.total
        model.estado = EstadoFacturaEnum(factura.estado.value)
        model.ruta_pdf = factura.ruta_pdf
        model.observaciones = factura.observaciones

        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def eliminar(self, factura_id: int) -> bool:
        model = (
            self._session.query(FacturaModel)
            .filter(FacturaModel.id == factura_id)
            .first()
        )
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True
