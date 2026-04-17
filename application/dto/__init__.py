from .cliente_dto import ClienteCreateDTO, ClienteUpdateDTO, ClienteResponseDTO
from .equipo_dto import EquipoCreateDTO, EquipoUpdateDTO, EquipoResponseDTO
from .orden_dto import OrdenCreateDTO, OrdenUpdateDTO, OrdenCompletarDTO, OrdenResponseDTO, ItemOrdenDTO
from .tecnico_dto import TecnicoCreateDTO, TecnicoUpdateDTO, TecnicoResponseDTO
from .repuesto_dto import RepuestoCreateDTO, RepuestoUpdateDTO, RepuestoResponseDTO

__all__ = [
    "ClienteCreateDTO", "ClienteUpdateDTO", "ClienteResponseDTO",
    "EquipoCreateDTO", "EquipoUpdateDTO", "EquipoResponseDTO",
    "OrdenCreateDTO", "OrdenUpdateDTO", "OrdenCompletarDTO", "OrdenResponseDTO", "ItemOrdenDTO",
    "TecnicoCreateDTO", "TecnicoUpdateDTO", "TecnicoResponseDTO",
    "RepuestoCreateDTO", "RepuestoUpdateDTO", "RepuestoResponseDTO"
]