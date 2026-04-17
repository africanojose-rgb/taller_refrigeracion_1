from domain.entities.orden_servicio import EstadoOrden
from domain.repositories.cliente_repository import ClienteRepository
from domain.repositories.equipo_repository import EquipoRepository
from domain.repositories.orden_repository import OrdenRepository
from domain.repositories.tecnico_repository import TecnicoRepository
from domain.entities.reporte import ReporteEstadistico, ReporteCliente, ReporteTecnico
from typing import List, Optional


class ReporteUseCases:
    """Casos de uso para generación de reportes."""
    
    def __init__(
        self,
        cliente_repo: ClienteRepository,
        equipo_repo: EquipoRepository,
        orden_repo: OrdenRepository,
        tecnico_repo: TecnicoRepository
    ):
        self._cliente_repo = cliente_repo
        self._equipo_repo = equipo_repo
        self._orden_repo = orden_repo
        self._tecnico_repo = tecnico_repo
    
    def obtener_estadisticas_generales(self) -> ReporteEstadistico:
        """Obtiene estadísticas generales del taller."""
        clientes = self._cliente_repo.obtener_todos()
        equipos = self._equipo_repo.obtener_todos()
        ordenes = self._orden_repo.obtener_todos()
        
        pendientes = len([o for o in ordenes if o.estado == EstadoOrden.PENDIENTE])
        en_proceso = len([o for o in ordenes if o.estado == EstadoOrden.EN_PROCESO])
        terminadas = len([o for o in ordenes if o.estado == EstadoOrden.TERMINADO])
        
        ingreso_total = sum(o.costo for o in ordenes if o.estado == EstadoOrden.TERMINADO)
        promedio = ingreso_total / terminadas if terminadas > 0 else 0.0
        
        return ReporteEstadistico(
            total_clientes=len(clientes),
            total_equipos=len(equipos),
            total_ordenes=len(ordenes),
            ordenes_pendientes=pendientes,
            ordenes_en_proceso=en_proceso,
            ordenes_terminadas=terminadas,
            ingreso_total=ingreso_total,
            promedio_orden=promedio
        )
    
    def obtener_reporte_cliente(self, cliente_id: int) -> Optional[ReporteCliente]:
        """Obtiene reporte detallado de un cliente."""
        cliente = self._cliente_repo.obtener_por_id(cliente_id)
        if not cliente:
            return None
        
        equipos = self._equipo_repo.obtener_por_cliente(cliente_id)
        ordenes = self._orden_repo.obtener_por_cliente(cliente_id)
        gasto_total = sum(o.costo for o in ordenes)
        
        return ReporteCliente(
            cliente_id=cliente_id,
            nombre=cliente.nombre,
            total_equipos=len(equipos),
            total_ordenes=len(ordenes),
            gasto_total=gasto_total
        )
    
    def obtener_reporte_tecnico(self, tecnico_id: int) -> Optional[ReporteTecnico]:
        """Obtiene reporte de rendimiento de un técnico."""
        tecnico = self._tecnico_repo.obtener_por_id(tecnico_id)
        if not tecnico:
            return None
        
        ordenes = self._orden_repo.obtener_todos()
        ordenes_tecnico = [o for o in ordenes if o.tecnico_id == tecnico_id and o.estado == EstadoOrden.TERMINADO]
        
        ingreso_total = sum(o.costo for o in ordenes_tecnico)
        
        return ReporteTecnico(
            tecnico_id=tecnico_id,
            nombre=tecnico.nombre,
            especialidad=tecnico.especialidad,
            ordenes_completadas=len(ordenes_tecnico),
            ingreso_total=ingreso_total
        )
    
    def listar_top_clientes(self, limite: int = 10) -> List[ReporteCliente]:
        """Lista los clientes con más gasto."""
        clientes = self._cliente_repo.obtener_todos()
        reportes = []
        
        for cliente in clientes:
            ordenes = self._orden_repo.obtener_por_cliente(cliente.id)
            gasto_total = sum(o.costo for o in ordenes)
            reportes.append(ReporteCliente(
                cliente_id=cliente.id,
                nombre=cliente.nombre,
                total_equipos=len(self._equipo_repo.obtener_por_cliente(cliente.id)),
                total_ordenes=len(ordenes),
                gasto_total=gasto_total
            ))
        
        reportes.sort(key=lambda r: r.gasto_total, reverse=True)
        return reportes[:limite]
    
    def listar_top_tecnicos(self, limite: int = 10) -> List[ReporteTecnico]:
        """Lista los técnicos con más órdenes completadas."""
        tecnicos = self._tecnico_repo.obtener_todos()
        ordenes = self._orden_repo.obtener_todos()
        reportes = []
        
        for tecnico in tecnicos:
            ordenes_tecnico = [o for o in ordenes if o.tecnico_id == tecnico.id and o.estado == EstadoOrden.TERMINADO]
            reportes.append(ReporteTecnico(
                tecnico_id=tecnico.id,
                nombre=tecnico.nombre,
                especialidad=tecnico.especialidad,
                ordenes_completadas=len(ordenes_tecnico),
                ingreso_total=sum(o.costo for o in ordenes_tecnico)
            ))
        
        reportes.sort(key=lambda r: r.ordenes_completadas, reverse=True)
        return reportes[:limite]