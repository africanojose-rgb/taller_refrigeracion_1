from dataclasses import dataclass
from typing import Optional


@dataclass
class ItemOrden:
    """Entidad para materiales/repuestos usados en una orden de servicio."""
    
    id: Optional[int] = None
    orden_id: int = 0
    repuesto_id: int = 0
    cantidad: int = 1
    precio_unitario: float = 0.0
    
    def __post_init__(self):
        if self.orden_id <= 0:
            raise ValueError("La orden es obligatoria")
        if self.repuesto_id <= 0:
            raise ValueError("El repuesto es obligatorio")
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        if self.precio_unitario < 0:
            raise ValueError("El precio no puede ser negativo")
    
    def get_subtotal(self) -> float:
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"ItemOrden({self.id}): Repuesto {self.repuesto_id} x{self.cantidad}"