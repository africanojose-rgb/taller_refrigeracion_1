from dataclasses import dataclass
from typing import Optional


@dataclass
class ReporteEstadistico:
    """Entidad para reportes estadísticos del taller."""
    
    total_clientes: int = 0
    total_equipos: int = 0
    total_ordenes: int = 0
    ordenes_pendientes: int = 0
    ordenes_en_proceso: int = 0
    ordenes_terminadas: int = 0
    ingreso_total: float = 0.0
    promedio_orden: float = 0.0


@dataclass
class ReporteCliente:
    """Reporte de historial de cliente."""
    
    cliente_id: int
    nombre: str
    total_equipos: int = 0
    total_ordenes: int = 0
    gasto_total: float = 0.0


@dataclass
class ReporteTecnico:
    """Reporte de rendimiento de técnico."""
    
    tecnico_id: int
    nombre: str
    especialidad: str
    ordenes_completadas: int = 0
    ingreso_total: float = 0.0