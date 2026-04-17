from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.orden_servicio import OrdenServicio, EstadoOrden
from domain.repositories.orden_repository import OrdenRepository
from infrastructure.models.models import OrdenModel
from datetime import date


class OrdenRepositoryImpl(OrdenRepository):
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: OrdenModel) -> OrdenServicio:
        return OrdenServicio(
            id=model.id,
            fecha_ingreso=model.fecha_ingreso,
            fecha_entrega=model.fecha_entrega,
            estado=EstadoOrden(model.estado.value),
            descripcion_falla=model.descripcion_falla or "",
            diagnostico=model.diagnostico or "",
            solucion=model.solucion or "",
            mano_obra=model.mano_obra,
            equipo_id=model.equipo_id,
            tecnico_id=model.tecnico_id
        )
    
    def crear(self, orden: OrdenServicio) -> OrdenServicio:
        model = OrdenModel(
            fecha_ingreso=orden.fecha_ingreso or date.today(),
            fecha_entrega=orden.fecha_entrega,
            estado=orden.estado.value,
            descripcion_falla=orden.descripcion_falla,
            diagnostico=orden.diagnostico,
            solucion=orden.solucion,
            mano_obra=orden.mano_obra,
            equipo_id=orden.equipo_id,
            tecnico_id=orden.tecnico_id
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, orden_id: int) -> Optional[OrdenServicio]:
        model = self._session.query(OrdenModel).filter(OrdenModel.id == orden_id).first()
        return self._to_entity(model) if model else None
    
    def obtener_todos(self) -> List[OrdenServicio]:
        models = self._session.query(OrdenModel).order_by(OrdenModel.fecha_ingreso.desc()).all()
        return [self._to_entity(m) for m in models]
    
    def obtener_por_estado(self, estado: EstadoOrden) -> List[OrdenServicio]:
        models = self._session.query(OrdenModel).filter(
            OrdenModel.estado == estado.value
        ).order_by(OrdenModel.fecha_ingreso.desc()).all()
        return [self._to_entity(m) for m in models]
    
    def obtener_por_equipo(self, equipo_id: int) -> List[OrdenServicio]:
        models = self._session.query(OrdenModel).filter(
            OrdenModel.equipo_id == equipo_id
        ).order_by(OrdenModel.fecha_ingreso.desc()).all()
        return [self._to_entity(m) for m in models]
    
    def obtener_por_cliente(self, cliente_id: int) -> List[OrdenServicio]:
        from infrastructure.models.models import EquipoModel
        models = self._session.query(OrdenModel).join(
            EquipoModel, OrdenModel.equipo_id == EquipoModel.id
        ).filter(EquipoModel.cliente_id == cliente_id).order_by(OrdenModel.fecha_ingreso.desc()).all()
        return [self._to_entity(m) for m in models]
    
    def actualizar(self, orden: OrdenServicio) -> OrdenServicio:
        model = self._session.query(OrdenModel).filter(OrdenModel.id == orden.id).first()
        if not model:
            raise ValueError(f"Orden con ID {orden.id} no encontrada")
        
        model.fecha_ingreso = orden.fecha_ingreso
        model.fecha_entrega = orden.fecha_entrega
        model.estado = orden.estado.value
        model.descripcion_falla = orden.descripcion_falla
        model.diagnostico = orden.diagnostico
        model.solucion = orden.solucion
        model.mano_obra = orden.mano_obra
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, orden_id: int) -> bool:
        model = self._session.query(OrdenModel).filter(OrdenModel.id == orden_id).first()
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True