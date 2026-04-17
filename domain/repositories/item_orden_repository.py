from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.item_orden import ItemOrden


class ItemOrdenRepository(ABC):
    """Interfaz del repositorio de items de orden (Puerto)."""
    
    @abstractmethod
    def crear(self, item: ItemOrden) -> ItemOrden:
        pass
    
    @abstractmethod
    def obtener_por_id(self, item_id: int) -> Optional[ItemOrden]:
        pass
    
    @abstractmethod
    def obtener_por_orden(self, orden_id: int) -> List[ItemOrden]:
        pass
    
    @abstractmethod
    def obtener_por_repuesto(self, repuesto_id: int) -> List[ItemOrden]:
        pass
    
    @abstractmethod
    def actualizar(self, item: ItemOrden) -> ItemOrden:
        pass
    
    @abstractmethod
    def eliminar(self, item_id: int) -> bool:
        pass
    
    @abstractmethod
    def eliminar_por_orden(self, orden_id: int) -> bool:
        pass