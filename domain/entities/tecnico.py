from dataclasses import dataclass
from typing import Optional


@dataclass
class Tecnico:
    """Entidad de dominio para Técnico del taller."""
    
    id: Optional[int] = None
    nombre: str = ""
    especialidad: str = ""
    telefono: str = ""
    
    def __post_init__(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del técnico es obligatorio")
        if not self.especialidad or not self.especialidad.strip():
            raise ValueError("La especialidad del técnico es obligatoria")
        if not self.telefono or not self.telefono.strip():
            raise ValueError("El teléfono del técnico es obligatorio")
    
    def actualizar(self, nombre: str = None, especialidad: str = None, telefono: str = None):
        if nombre is not None:
            self.nombre = nombre.strip()
        if especialidad is not None:
            self.especialidad = especialidad.strip()
        if telefono is not None:
            self.telefono = telefono.strip()
    
    def __str__(self):
        return f"Técnico({self.id}): {self.nombre} - {self.especialidad}"