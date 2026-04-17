from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from enum import Enum


class EstadoOrden(str, Enum):
    """Estados posibles de una orden de servicio."""
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    TERMINADO = "terminado"
    CANCELADO = "cancelado"


@dataclass
class OrdenServicio:
    """Entidad de dominio para Órden de Servicio."""
    
    id: Optional[int] = None
    fecha_ingreso: Optional[date] = None
    fecha_entrega: Optional[date] = None
    estado: EstadoOrden = EstadoOrden.PENDIENTE
    descripcion_falla: str = ""
    diagnostico: str = ""
    solucion: str = ""
    mano_obra: float = 0.0
    equipo_id: int = 0
    tecnico_id: int = 0
    
    def __post_init__(self):
        if self.equipo_id is None or self.equipo_id <= 0:
            raise ValueError("El equipo es obligatorio")
        if self.tecnico_id is None or self.tecnico_id <= 0:
            raise ValueError("El técnico es obligatorio")
        if self.mano_obra < 0:
            raise ValueError("El costo de mano de obra no puede ser negativo")
    
    def cambiar_estado(self, nuevo_estado: EstadoOrden):
        """Cambia el estado de la orden con validación de flujo."""
        transiciones_permitidas = {
            EstadoOrden.PENDIENTE: [EstadoOrden.EN_PROCESO, EstadoOrden.CANCELADO],
            EstadoOrden.EN_PROCESO: [EstadoOrden.TERMINADO, EstadoOrden.CANCELADO],
            EstadoOrden.TERMINADO: [],
            EstadoOrden.CANCELADO: []
        }
        
        if nuevo_estado in transiciones_permitidas.get(self.estado, []):
            self.estado = nuevo_estado
        else:
            raise ValueError(f"No se puede cambiar de {self.estado.value} a {nuevo_estado.value}")
    
    def completar(self, diagnostico: str, solucion: str, mano_obra: float, fecha_entrega: date = None):
        """Completa la orden de servicio."""
        if not diagnostico or not diagnostico.strip():
            raise ValueError("El diagnóstico es obligatorio")
        if not solucion or not solucion.strip():
            raise ValueError("La solución es obligatoria")
        
        self.diagnostico = diagnostico.strip()
        self.solucion = solucion.strip()
        self.mano_obra = mano_obra
        self.estado = EstadoOrden.TERMINADO
        self.fecha_entrega = fecha_entrega or date.today()
    
    def __str__(self):
        return f"Orden({self.id}): {self.estado.value}"