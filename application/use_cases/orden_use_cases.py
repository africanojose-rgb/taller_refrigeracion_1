from domain.entities.orden_servicio import OrdenServicio, EstadoOrden
from domain.entities.item_orden import ItemOrden
from domain.repositories.orden_repository import OrdenRepository
from domain.repositories.item_orden_repository import ItemOrdenRepository
from domain.repositories.repuesto_repository import RepuestoRepository
from application.dto.orden_dto import OrdenCreateDTO, OrdenUpdateDTO, OrdenCompletarDTO, ItemOrdenDTO
from typing import List, Optional
from datetime import date


class OrdenUseCases:
    """Casos de uso para la gestión de órdenes de servicio."""
    
    def __init__(self, orden_repo: OrdenRepository, item_repo: ItemOrdenRepository, repuesto_repo: RepuestoRepository):
        self._orden_repo = orden_repo
        self._item_repo = item_repo
        self._repuesto_repo = repuesto_repo
    
    def crear_orden(self, dto: OrdenCreateDTO) -> OrdenServicio:
        """Crea una nueva orden de servicio."""
        orden = OrdenServicio(
            fecha_ingreso=date.today(),
            estado=EstadoOrden.PENDIENTE,
            descripcion_falla=dto.descripcion_falla or "",
            equipo_id=dto.equipo_id,
            tecnico_id=dto.tecnico_id
        )
        return self._orden_repo.crear(orden)
    
    def obtener_orden(self, orden_id: int) -> Optional[OrdenServicio]:
        return self._orden_repo.obtener_por_id(orden_id)
    
    def listar_ordenes(self) -> List[OrdenServicio]:
        return self._orden_repo.obtener_todos()
    
    def listar_por_estado(self, estado: str) -> List[OrdenServicio]:
        return self._orden_repo.obtener_por_estado(EstadoOrden(estado))
    
    def listar_por_equipo(self, equipo_id: int) -> List[OrdenServicio]:
        return self._orden_repo.obtener_por_equipo(equipo_id)
    
    def listar_por_cliente(self, cliente_id: int) -> List[OrdenServicio]:
        return self._orden_repo.obtener_por_cliente(cliente_id)
    
    def actualizar_orden(self, orden_id: int, dto: OrdenUpdateDTO) -> OrdenServicio:
        orden = self._orden_repo.obtener_por_id(orden_id)
        if not orden:
            raise ValueError(f"Orden con ID {orden_id} no encontrada")
        
        if dto.descripcion_falla is not None:
            orden.descripcion_falla = dto.descripcion_falla.strip()
        if dto.diagnostico is not None:
            orden.diagnostico = dto.diagnostico.strip()
        if dto.solucion is not None:
            orden.solucion = dto.solucion.strip()
        if dto.mano_obra is not None:
            orden.mano_obra = dto.mano_obra
        if dto.estado is not None:
            orden.cambiar_estado(EstadoOrden(dto.estado))
        
        return self._orden_repo.actualizar(orden)
    
    def completar_orden(self, orden_id: int, dto: OrdenCompletarDTO) -> OrdenServicio:
        orden = self._orden_repo.obtener_por_id(orden_id)
        if not orden:
            raise ValueError(f"Orden con ID {orden_id} no encontrada")
        
        orden.completar(
            diagnostico=dto.diagnostico,
            solucion=dto.solucion,
            mano_obra=dto.mano_obra,
            fecha_entrega=dto.fecha_entrega
        )
        return self._orden_repo.actualizar(orden)
    
    def iniciar_orden(self, orden_id: int) -> OrdenServicio:
        orden = self._orden_repo.obtener_por_id(orden_id)
        if not orden:
            raise ValueError(f"Orden con ID {orden_id} no encontrada")
        
        orden.cambiar_estado(EstadoOrden.EN_PROCESO)
        return self._orden_repo.actualizar(orden)
    
    def eliminar_orden(self, orden_id: int) -> bool:
        self._item_repo.eliminar_por_orden(orden_id)
        return self._orden_repo.eliminar(orden_id)
    
    def agregar_material(self, orden_id: int, dto: ItemOrdenDTO) -> ItemOrden:
        orden = self._orden_repo.obtener_por_id(orden_id)
        if not orden:
            raise ValueError(f"Orden con ID {orden_id} no encontrada")
        
        repuesto = self._repuesto_repo.obtener_por_id(dto.repuesto_id)
        if not repuesto:
            raise ValueError(f"Repuesto con ID {dto.repuesto_id} no encontrado")
        
        if repuesto.cantidad_stock < dto.cantidad:
            raise ValueError(f"No hay suficiente stock. Disponible: {repuesto.cantidad_stock}")
        
        self._repuesto_repo.ajustar_stock(dto.repuesto_id, -dto.cantidad)
        
        item = ItemOrden(
            orden_id=orden_id,
            repuesto_id=dto.repuesto_id,
            cantidad=dto.cantidad,
            precio_unitario=dto.precio_unitario
        )
        return self._item_repo.crear(item)
    
    def obtener_materiales(self, orden_id: int) -> List[ItemOrden]:
        return self._item_repo.obtener_por_orden(orden_id)
    
    def calcular_total(self, orden_id: int) -> float:
        orden = self._orden_repo.obtener_por_id(orden_id)
        if not orden:
            return 0.0
        
        items = self._item_repo.obtener_por_orden(orden_id)
        total_materiales = sum(item.get_subtotal() for item in items)
        return orden.mano_obra + total_materiales