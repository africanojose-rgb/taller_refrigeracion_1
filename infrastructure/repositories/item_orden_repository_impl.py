from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.item_orden import ItemOrden
from domain.repositories.item_orden_repository import ItemOrdenRepository
from infrastructure.models.models import ItemOrdenModel


class ItemOrdenRepositoryImpl(ItemOrdenRepository):
    
    def __init__(self, session: Session):
        self._session = session
    
    def _to_entity(self, model: ItemOrdenModel) -> ItemOrden:
        return ItemOrden(
            id=model.id,
            orden_id=model.orden_id,
            repuesto_id=model.repuesto_id,
            cantidad=model.cantidad,
            precio_unitario=model.precio_unitario
        )
    
    def crear(self, item: ItemOrden) -> ItemOrden:
        model = ItemOrdenModel(
            orden_id=item.orden_id,
            repuesto_id=item.repuesto_id,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def obtener_por_id(self, item_id: int) -> Optional[ItemOrden]:
        model = self._session.query(ItemOrdenModel).filter(ItemOrdenModel.id == item_id).first()
        return self._to_entity(model) if model else None
    
    def obtener_por_orden(self, orden_id: int) -> List[ItemOrden]:
        models = self._session.query(ItemOrdenModel).filter(
            ItemOrdenModel.orden_id == orden_id
        ).all()
        return [self._to_entity(m) for m in models]
    
    def obtener_por_repuesto(self, repuesto_id: int) -> List[ItemOrden]:
        models = self._session.query(ItemOrdenModel).filter(
            ItemOrdenModel.repuesto_id == repuesto_id
        ).all()
        return [self._to_entity(m) for m in models]
    
    def actualizar(self, item: ItemOrden) -> ItemOrden:
        model = self._session.query(ItemOrdenModel).filter(ItemOrdenModel.id == item.id).first()
        if not model:
            raise ValueError(f"Item con ID {item.id} no encontrado")
        
        model.cantidad = item.cantidad
        model.precio_unitario = item.precio_unitario
        
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)
    
    def eliminar(self, item_id: int) -> bool:
        model = self._session.query(ItemOrdenModel).filter(ItemOrdenModel.id == item_id).first()
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True
    
    def eliminar_por_orden(self, orden_id: int) -> bool:
        self._session.query(ItemOrdenModel).filter(
            ItemOrdenModel.orden_id == orden_id
        ).delete()
        self._session.commit()
        return True