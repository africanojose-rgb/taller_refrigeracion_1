from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.tecnico import Tecnico
from domain.repositories.tecnico_repository import TecnicoRepository
from infrastructure.models.models import TecnicoModel


class TecnicoRepositoryImpl(TecnicoRepository):
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: TecnicoModel) -> Tecnico:
        return Tecnico(
            id=model.id,
            nombre=model.nombre,
            especialidad=model.especialidad,
            telefono=model.telefono
        )
    
    def crear(self, tecnico: Tecnico) -> Tecnico:
        model = TecnicoModel(
            nombre=tecnico.nombre,
            especialidad=tecnico.especialidad,
            telefono=tecnico.telefono
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, tecnico_id: int) -> Optional[Tecnico]:
        model = self._session.query(TecnicoModel).filter(TecnicoModel.id == tecnico_id).first()
        return self._to_entity(model) if model else None
    
    def obtener_todos(self) -> List[Tecnico]:
        models = self._session.query(TecnicoModel).order_by(TecnicoModel.nombre).all()
        return [self._to_entity(m) for m in models]
    
    def buscar_por_especialidad(self, especialidad: str) -> List[Tecnico]:
        models = self._session.query(TecnicoModel).filter(
            TecnicoModel.especialidad.like(f"%{especialidad}%")
        ).all()
        return [self._to_entity(m) for m in models]
    
    def actualizar(self, tecnico: Tecnico) -> Tecnico:
        model = self._session.query(TecnicoModel).filter(TecnicoModel.id == tecnico.id).first()
        if not model:
            raise ValueError(f"Técnico con ID {tecnico.id} no encontrado")
        
        model.nombre = tecnico.nombre
        model.especialidad = tecnico.especialidad
        model.telefono = tecnico.telefono
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, tecnico_id: int) -> bool:
        model = self._session.query(TecnicoModel).filter(TecnicoModel.id == tecnico_id).first()
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True