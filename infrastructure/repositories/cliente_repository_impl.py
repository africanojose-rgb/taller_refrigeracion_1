from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository
from infrastructure.models.models import ClienteModel


class ClienteRepositoryImpl(ClienteRepository):
    """Implementación del repositorio de clientes usando SQLAlchemy."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: ClienteModel) -> Cliente:
        return Cliente(
            id=model.id,
            nombre=model.nombre,
            telefono=model.telefono,
            direccion=model.direccion or "",
            email=model.email or ""
        )
    
    def _to_model(self, entity: Cliente) -> ClienteModel:
        if entity.id:
            return self._session.query(ClienteModel).filter(ClienteModel.id == entity.id).first()
        return ClienteModel(
            nombre=entity.nombre,
            telefono=entity.telefono,
            direccion=entity.direccion,
            email=entity.email
        )
    
    def crear(self, cliente: Cliente) -> Cliente:
        model = ClienteModel(
            nombre=cliente.nombre,
            telefono=cliente.telefono,
            direccion=cliente.direccion,
            email=cliente.email
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, cliente_id: int) -> Optional[Cliente]:
        model = self._session.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
        return self._to_entity(model) if model else None
    
    def obtener_todos(self) -> List[Cliente]:
        models = self._session.query(ClienteModel).order_by(ClienteModel.nombre).all()
        return [self._to_entity(m) for m in models]
    
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        models = self._session.query(ClienteModel).filter(
            ClienteModel.nombre.like(f"%{nombre}%")
        ).all()
        return [self._to_entity(m) for m in models]
    
    def actualizar(self, cliente: Cliente) -> Cliente:
        model = self._session.query(ClienteModel).filter(ClienteModel.id == cliente.id).first()
        if not model:
            raise ValueError(f"Cliente con ID {cliente.id} no encontrado")
        
        model.nombre = cliente.nombre
        model.telefono = cliente.telefono
        model.direccion = cliente.direccion
        model.email = cliente.email
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, cliente_id: int) -> bool:
        model = self._session.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True