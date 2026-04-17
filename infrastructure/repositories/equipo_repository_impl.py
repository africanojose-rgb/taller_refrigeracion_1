from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.equipo import Equipo
from domain.repositories.equipo_repository import EquipoRepository
from infrastructure.models.models import EquipoModel


class EquipoRepositoryImpl(EquipoRepository):
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: EquipoModel) -> Equipo:
        return Equipo(
            id=model.id,
            tipo_equipo=model.tipo_equipo,
            marca=model.marca,
            modelo=model.modelo or "",
            serial=model.serial or "",
            cliente_id=model.cliente_id
        )
    
    def crear(self, equipo: Equipo) -> Equipo:
        model = EquipoModel(
            tipo_equipo=equipo.tipo_equipo,
            marca=equipo.marca,
            modelo=equipo.modelo,
            serial=equipo.serial,
            cliente_id=equipo.cliente_id
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, equipo_id: int) -> Optional[Equipo]:
        model = self._session.query(EquipoModel).filter(EquipoModel.id == equipo_id).first()
        return self._to_entity(model) if model else None
    
    def obtener_todos(self) -> List[Equipo]:
        models = self._session.query(EquipoModel).order_by(EquipoModel.marca).all()
        return [self._to_entity(m) for m in models]
    
    def obtener_por_cliente(self, cliente_id: int) -> List[Equipo]:
        models = self._session.query(EquipoModel).filter(EquipoModel.cliente_id == cliente_id).all()
        return [self._to_entity(m) for m in models]
    
    def buscar_por_serial(self, serial: str) -> Optional[Equipo]:
        model = self._session.query(EquipoModel).filter(EquipoModel.serial == serial).first()
        return self._to_entity(model) if model else None
    
    def actualizar(self, equipo: Equipo) -> Equipo:
        model = self._session.query(EquipoModel).filter(EquipoModel.id == equipo.id).first()
        if not model:
            raise ValueError(f"Equipo con ID {equipo.id} no encontrado")
        
        model.tipo_equipo = equipo.tipo_equipo
        model.marca = equipo.marca
        model.modelo = equipo.modelo
        model.serial = equipo.serial
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, equipo_id: int) -> bool:
        model = self._session.query(EquipoModel).filter(EquipoModel.id == equipo_id).first()
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True