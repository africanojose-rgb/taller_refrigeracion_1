from dataclasses import dataclass
from typing import Optional


@dataclass
class Equipo:
    """Entidad de dominio para Equipo de refrigeración."""
    
    id: Optional[int] = None
    tipo_equipo: str = ""
    marca: str = ""
    modelo: str = ""
    serial: str = ""
    cliente_id: int = 0
    
    def __post_init__(self):
        if not self.tipo_equipo or not self.tipo_equipo.strip():
            raise ValueError("El tipo de equipo es obligatorio")
        if not self.marca or not self.marca.strip():
            raise ValueError("La marca del equipo es obligatoria")
        if self.cliente_id is None or self.cliente_id <= 0:
            raise ValueError("El cliente es obligatorio para el equipo")
    
    def actualizar(self, tipo_equipo: str = None, marca: str = None,
                   modelo: str = None, serial: str = None):
        if tipo_equipo is not None:
            self.tipo_equipo = tipo_equipo.strip()
        if marca is not None:
            self.marca = marca.strip()
        if modelo is not None:
            self.modelo = modelo.strip()
        if serial is not None:
            self.serial = serial.strip()
    
    def __str__(self):
        return f"Equipo({self.id}): {self.tipo_equipo} {self.marca} - {self.serial}"