from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.factura import Factura


class FacturaRepository(ABC):
    """Interfaz del repositorio de facturas (Puerto)."""

    @abstractmethod
    def crear(self, factura: Factura) -> Factura:
        pass

    @abstractmethod
    def obtener_por_id(self, factura_id: int) -> Optional[Factura]:
        pass

    @abstractmethod
    def obtener_por_numero(self, numero_factura: str) -> Optional[Factura]:
        pass

    @abstractmethod
    def obtener_por_orden(self, orden_id: int) -> Optional[Factura]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Factura]:
        pass

    @abstractmethod
    def buscar_por_cliente(self, cliente_id: int) -> List[Factura]:
        pass

    @abstractmethod
    def obtener_por_estado(self, estado: str) -> List[Factura]:
        pass

    @abstractmethod
    def obtener_ultimo_numero(self) -> Optional[str]:
        pass

    @abstractmethod
    def actualizar(self, factura: Factura) -> Factura:
        pass

    @abstractmethod
    def eliminar(self, factura_id: int) -> bool:
        pass
