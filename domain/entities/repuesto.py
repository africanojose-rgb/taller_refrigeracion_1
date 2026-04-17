from dataclasses import dataclass
from typing import Optional


@dataclass
class Repuesto:
    """Entidad de dominio para Repuestos/Inventario."""
    
    id: Optional[int] = None
    nombre: str = ""
    codigo: str = ""
    descripcion: str = ""
    costo_compra: float = 0.0
    precio_venta: float = 0.0
    cantidad_stock: int = 0
    cantidad_minima: int = 5
    
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del repuesto es obligatorio")
        if not self.codigo or not self.codigo.strip():
            raise ValueError("El código del repuesto es obligatorio")
        if self.costo_compra < 0:
            raise ValueError("El costo de compra no puede ser negativo")
        if self.precio_venta < 0:
            raise ValueError("El precio de venta no puede ser negativo")
        if self.cantidad_stock < 0:
            raise ValueError("La cantidad en stock no puede ser negativa")
    
    def actualizar_precio(self, costo_compra: float = None, precio_venta: float = None):
        if costo_compra is not None:
            self.costo_compra = max(0, costo_compra)
        if precio_venta is not None:
            self.precio_venta = max(0, precio_venta)
    
    def ajustar_stock(self, cantidad: int):
        nuevo_stock = self.cantidad_stock + cantidad
        if nuevo_stock < 0:
            raise ValueError("No hay suficiente stock")
        self.cantidad_stock = nuevo_stock
    
    def necesita_reorden(self) -> bool:
        return self.cantidad_stock <= self.cantidad_minima
    
    def get_margen(self) -> float:
        if self.costo_compra > 0:
            return ((self.precio_venta - self.costo_compra) / self.costo_compra) * 100
        return 0.0
    
    def __str__(self):
        return f"Repuesto({self.id}): {self.nombre} - Stock: {self.cantidad_stock}"