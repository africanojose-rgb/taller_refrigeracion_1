from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.repuesto import Repuesto
from domain.repositories.repuesto_repository import RepuestoRepository
from infrastructure.models.models import RepuestoModel


class RepuestoRepositoryImpl(RepuestoRepository):
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: RepuestoModel) -> Repuesto:
        return Repuesto(
            id=model.id,
            nombre=model.nombre,
            codigo=model.codigo,
            descripcion=model.descripcion or "",
            costo_compra=model.costo_compra,
            precio_venta=model.precio_venta,
            cantidad_stock=model.cantidad_stock,
            cantidad_minima=model.cantidad_minima
        )
    
    def crear(self, repuesto: Repuesto) -> Repuesto:
        model = RepuestoModel(
            nombre=repuesto.nombre,
            codigo=repuesto.codigo,
            descripcion=repuesto.descripcion,
            costo_compra=repuesto.costo_compra,
            precio_venta=repuesto.precio_venta,
            cantidad_stock=repuesto.cantidad_stock,
            cantidad_minima=repuesto.cantidad_minima
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, repuesto_id: int) -> Optional[Repuesto]:
        model = self._session.query(RepuestoModel).filter(RepuestoModel.id == repuesto_id).first()
        return self._to_entity(model) if model else None
    
    def obtener_todos(self) -> List[Repuesto]:
        models = self._session.query(RepuestoModel).order_by(RepuestoModel.nombre).all()
        return [self._to_entity(m) for m in models]
    
    def buscar_por_codigo(self, codigo: str) -> Optional[Repuesto]:
        model = self._session.query(RepuestoModel).filter(RepuestoModel.codigo == codigo).first()
        return self._to_entity(model) if model else None
    
    def buscar_por_nombre(self, nombre: str) -> List[Repuesto]:
        models = self._session.query(RepuestoModel).filter(
            RepuestoModel.nombre.like(f"%{nombre}%")
        ).all()
        return [self._to_entity(m) for m in models]
    
    def obtener_bajo_stock(self) -> List[Repuesto]:
        models = self._session.query(RepuestoModel).filter(
            RepuestoModel.cantidad_stock <= RepuestoModel.cantidad_minima
        ).all()
        return [self._to_entity(m) for m in models]
    
    def actualizar(self, repuesto: Repuesto) -> Repuesto:
        model = self._session.query(RepuestoModel).filter(RepuestoModel.id == repuesto.id).first()
        if not model:
            raise ValueError(f"Repuesto con ID {repuesto.id} no encontrado")
        
        model.nombre = repuesto.nombre
        model.codigo = repuesto.codigo
        model.descripcion = repuesto.descripcion
        model.costo_compra = repuesto.costo_compra
        model.precio_venta = repuesto.precio_venta
        model.cantidad_stock = repuesto.cantidad_stock
        model.cantidad_minima = repuesto.cantidad_minima
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def ajustar_stock(self, repuesto_id: int, cantidad: int) -> Repuesto:
        model = self._session.query(RepuestoModel).filter(RepuestoModel.id == repuesto_id).first()
        if not model:
            raise ValueError(f"Repuesto con ID {repuesto_id} no encontrado")
        
        model.cantidad_stock += cantidad
        if model.cantidad_stock < 0:
            raise ValueError("No hay suficiente stock")
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, repuesto_id: int) -> bool:
        model = self._session.query(RepuestoModel).filter(RepuestoModel.id == repuesto_id).first()
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True