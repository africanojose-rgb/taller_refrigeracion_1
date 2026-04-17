from domain.entities.tecnico import Tecnico
from domain.repositories.tecnico_repository import TecnicoRepository
from application.dto.tecnico_dto import TecnicoCreateDTO, TecnicoUpdateDTO
from typing import List, Optional


class TecnicoUseCases:
    """Casos de uso para la gestión de técnicos."""
    
    def __init__(self, repository: TecnicoRepository):
        self._repository = repository
    
    def crear_tecnico(self, dto: TecnicoCreateDTO) -> Tecnico:
        tecnico = Tecnico(
            nombre=dto.nombre.strip(),
            especialidad=dto.especialidad.strip(),
            telefono=dto.telefono.strip()
        )
        return self._repository.crear(tecnico)
    
    def obtener_tecnico(self, tecnico_id: int) -> Optional[Tecnico]:
        return self._repository.obtener_por_id(tecnico_id)
    
    def listar_tecnicos(self) -> List[Tecnico]:
        return self._repository.obtener_todos()
    
    def buscar_por_especialidad(self, especialidad: str) -> List[Tecnico]:
        return self._repository.buscar_por_especialidad(especialidad.strip())
    
    def actualizar_tecnico(self, tecnico_id: int, dto: TecnicoUpdateDTO) -> Tecnico:
        tecnico = self._repository.obtener_por_id(tecnico_id)
        if not tecnico:
            raise ValueError(f"Técnico con ID {tecnico_id} no encontrado")
        
        if dto.nombre is not None:
            tecnico.actualizar(nombre=dto.nombre)
        if dto.especialidad is not None:
            tecnico.actualizar(especialidad=dto.especialidad)
        if dto.telefono is not None:
            tecnico.actualizar(telefono=dto.telefono)
        
        return self._repository.actualizar(tecnico)
    
    def eliminar_tecnico(self, tecnico_id: int) -> bool:
        return self._repository.eliminar(tecnico_id)