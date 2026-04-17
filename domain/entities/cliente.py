from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Entidad de dominio para Cliente del taller de refrigeración."""
    
    id: Optional[int] = None
    nombre: str = ""
    telefono: str = ""
    direccion: str = ""
    email: str = ""
    
    def __post_init__(self):
        """Validaciones de negocio después de la inicialización."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del cliente es obligatorio")
        if not self.telefono or not self.telefono.strip():
            raise ValueError("El teléfono del cliente es obligatorio")
    
    def actualizar_informacion(self, nombre: str = None, telefono: str = None, 
                                direccion: str = None, email: str = None):
        """Actualiza la información del cliente manteniendo la integridad."""
        if nombre is not None:
            self.nombre = nombre.strip()
        if telefono is not None:
            self.telefono = telefono.strip()
        if direccion is not None:
            self.direccion = direccion.strip()
        if email is not None:
            self.email = email.strip()
    
    def __str__(self):
        return f"Cliente({self.id}): {self.nombre} - {self.telefono}"