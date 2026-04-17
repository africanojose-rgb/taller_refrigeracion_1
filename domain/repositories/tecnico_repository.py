from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.tecnico import Tecnico


class TecnicoRepository(ABC):
    """Interfaz del repositorio de técnicos (Puerto)."""
    
    @abstractmethod
    def crear(self, tecnico: Tecnico) -> Tecnico:
        pass
    
    @abstractmethod
    def obtener_por_id(self, tecnico_id: int) -> Optional[Tecnico]:
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Tecnico]:
        pass
    
    @abstractmethod
    def buscar_por_especialidad(self, especialidad: str) -> List[Tecnico]:
        pass
    
    @abstractmethod
    def actualizar(self, tecnico: Tecnico) -> Tecnico:
        pass
    
    @abstractmethod
    def eliminar(self, tecnico_id: int) -> bool:
        pass