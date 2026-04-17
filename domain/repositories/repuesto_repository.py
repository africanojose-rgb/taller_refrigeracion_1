from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.repuesto import Repuesto


class RepuestoRepository(ABC):
    """Interfaz del repositorio de repuestos (Puerto)."""
    
    @abstractmethod
    def crear(self, repuesto: Repuesto) -> Repuesto:
        pass
    
    @abstractmethod
    def obtener_por_id(self, repuesto_id: int) -> Optional[Repuesto]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Repuesto]:
        pass
    
    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Optional[Repuesto]:
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Repuesto]:
        pass
    
    @abstractmethod
    def obtener_bajo_stock(self) -> List[Repuesto]:
        pass
    
    @abstractmethod
    def actualizar(self, repuesto: Repuesto) -> Repuesto:
        pass
    
    @abstractmethod
    def ajustar_stock(self, repuesto_id: int, cantidad: int) -> Repuesto:
        pass
    
    @abstractmethod
    def eliminar(self, repuesto_id: int) -> bool:
        pass