from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from ..entities.orden_servicio import OrdenServicio, EstadoOrden


class OrdenRepository(ABC):
    """Interfaz del repositorio de órdenes de servicio (Puerto)."""
    
    @abstractmethod
    def crear(self, orden: OrdenServicio) -> OrdenServicio:
        pass
    
    @abstractmethod
    def obtener_por_id(self, orden_id: int) -> Optional[OrdenServicio]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[OrdenServicio]:
        pass
    
    @abstractmethod
    def obtener_por_estado(self, estado: EstadoOrden) -> List[OrdenServicio]:
        pass
    
    @abstractmethod
    def obtener_por_equipo(self, equipo_id: int) -> List[OrdenServicio]:
        pass
    
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: int) -> List[OrdenServicio]:
        pass
    
    @abstractmethod
    def actualizar(self, orden: OrdenServicio) -> OrdenServicio:
        pass
    
    @abstractmethod
    def eliminar(self, orden_id: int) -> bool:
        pass