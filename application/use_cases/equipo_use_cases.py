from domain.entities.equipo import Equipo
from domain.repositories.equipo_repository import EquipoRepository
from application.dto.equipo_dto import EquipoCreateDTO, EquipoUpdateDTO
from typing import List, Optional


class EquipoUseCases:
    """Casos de uso para la gestión de equipos."""
    
    def __init__(self, repository: EquipoRepository):
        self._repository = repository
    
    def crear_equipo(self, dto: EquipoCreateDTO) -> Equipo:
        """Crea un nuevo equipo."""
        equipo = Equipo(
            tipo_equipo=dto.tipo_equipo.strip(),
            marca=dto.marca.strip(),
            modelo=dto.modelo.strip() if dto.modelo else "",
            serial=dto.serial.strip() if dto.serial else "",
            cliente_id=dto.cliente_id
        )
        return self._repository.crear(equipo)
    
    def obtener_equipo(self, equipo_id: int) -> Optional[Equipo]:
        return self._repository.obtener_por_id(equipo_id)
    
    def listar_equipos(self) -> List[Equipo]:
        return self._repository.obtener_todos()
    
    def listar_equipos_por_cliente(self, cliente_id: int) -> List[Equipo]:
        return self._repository.obtener_por_cliente(cliente_id)
    
    def buscar_por_serial(self, serial: str) -> Optional[Equipo]:
        return self._repository.buscar_por_serial(serial)
    
    def actualizar_equipo(self, equipo_id: int, dto: EquipoUpdateDTO) -> Equipo:
        equipo = self._repository.obtener_por_id(equipo_id)
        if not equipo:
            raise ValueError(f"Equipo con ID {equipo_id} no encontrado")
        
        if dto.tipo_equipo is not None:
            equipo.actualizar(tipo_equipo=dto.tipo_equipo)
        if dto.marca is not None:
            equipo.actualizar(marca=dto.marca)
        if dto.modelo is not None:
            equipo.actualizar(modelo=dto.modelo)
        if dto.serial is not None:
            equipo.actualizar(serial=dto.serial)
        
        return self._repository.actualizar(equipo)
    
    def eliminar_equipo(self, equipo_id: int) -> bool:
        return self._repository.eliminar(equipo_id)