from domain.entities.repuesto import Repuesto
from domain.repositories.repuesto_repository import RepuestoRepository
from application.dto.repuesto_dto import RepuestoCreateDTO, RepuestoUpdateDTO
from typing import List, Optional


class RepuestoUseCases:
    """Casos de uso para gestión de repuestos/inventario."""
    
    def __init__(self, repository: RepuestoRepository):
        self._repository = repository
    
    def crear_repuesto(self, dto: RepuestoCreateDTO) -> Repuesto:
        repuesto = Repuesto(
            nombre=dto.nombre.strip(),
            codigo=dto.codigo.strip().upper(),
            descripcion=dto.descripcion.strip() if dto.descripcion else "",
            costo_compra=dto.costo_compra,
            precio_venta=dto.precio_venta,
            cantidad_stock=dto.cantidad_stock,
            cantidad_minima=dto.cantidad_minima
        )
        return self._repository.crear(repuesto)
    
    def obtener_repuesto(self, repuesto_id: int) -> Optional[Repuesto]:
        return self._repository.obtener_por_id(repuesto_id)
    
    def listar_repuestos(self) -> List[Repuesto]:
        return self._repository.obtener_todos()
    
    def buscar_por_codigo(self, codigo: str) -> Optional[Repuesto]:
        return self._repository.buscar_por_codigo(codigo.strip().upper())
    
    def buscar_por_nombre(self, nombre: str) -> List[Repuesto]:
        return self._repository.buscar_por_nombre(nombre.strip())
    
    def listar_bajo_stock(self) -> List[Repuesto]:
        return self._repository.obtener_bajo_stock()
    
    def actualizar_repuesto(self, repuesto_id: int, dto: RepuestoUpdateDTO) -> Repuesto:
        repuesto = self._repository.obtener_por_id(repuesto_id)
        if not repuesto:
            raise ValueError(f"Repuesto con ID {repuesto_id} no encontrado")
        
        if dto.nombre is not None:
            repuesto.nombre = dto.nombre.strip()
        if dto.descripcion is not None:
            repuesto.descripcion = dto.descripcion.strip()
        if dto.costo_compra is not None:
            repuesto.costo_compra = dto.costo_compra
        if dto.precio_venta is not None:
            repuesto.precio_venta = dto.precio_venta
        if dto.cantidad_stock is not None:
            repuesto.cantidad_stock = dto.cantidad_stock
        if dto.cantidad_minima is not None:
            repuesto.cantidad_minima = dto.cantidad_minima
        
        return self._repository.actualizar(repuesto)
    
    def ajustar_stock(self, repuesto_id: int, cantidad: int) -> Repuesto:
        return self._repository.ajustar_stock(repuesto_id, cantidad)
    
    def eliminar_repuesto(self, repuesto_id: int) -> bool:
        return self._repository.eliminar(repuesto_id)