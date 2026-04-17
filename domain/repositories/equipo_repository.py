from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.equipo import Equipo


class EquipoRepository(ABC):
    """Interfaz del repositorio de equipos (Puerto)."""
    
    @abstractmethod
    def crear(self, equipo: Equipo) -> Equipo:
        pass
    
    @abstractmethod
    def obtener_por_id(self, equipo_id: int) -> Optional[Equipo]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Equipo]:
        pass
    
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: int) -> List[Equipo]:
        pass
    
    @abstractmethod
    def buscar_por_serial(self, serial: str) -> Optional[Equipo]:
        pass
    
    @abstractmethod
    def actualizar(self, equipo: Equipo) -> Equipo:
        pass
    
    @abstractmethod
    def eliminar(self, equipo_id: int) -> bool:
        pass