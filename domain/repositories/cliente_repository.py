from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.cliente import Cliente


class ClienteRepository(ABC):
    """Interfaz del repositorio de clientes (Puerto)."""
    
    @abstractmethod
    def crear(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente y retorna la entidad con ID asignado."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, cliente_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre (búsqueda parcial)."""
        pass
    
    @abstractmethod
    def actualizar(self, cliente: Cliente) -> Cliente:
        """Actualiza un cliente existente."""
        pass
    
    @abstractmethod
    def eliminar(self, cliente_id: int) -> bool:
        """Elimina un cliente por su ID."""
        pass