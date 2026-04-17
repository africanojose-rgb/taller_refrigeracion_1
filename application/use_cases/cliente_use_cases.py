from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository
from application.dto.cliente_dto import ClienteCreateDTO, ClienteUpdateDTO
from typing import List, Optional


class ClienteUseCases:
    """Casos de uso para la gestión de clientes."""
    
    def __init__(self, repository: ClienteRepository):
        self._repository = repository
    
    def crear_cliente(self, dto: ClienteCreateDTO) -> Cliente:
        """Crea un nuevo cliente."""
        cliente = Cliente(
            nombre=dto.nombre.strip(),
            telefono=dto.telefono.strip(),
            direccion=dto.direccion.strip() if dto.direccion else "",
            email=dto.email.strip() if dto.email else ""
        )
        return self._repository.crear(cliente)
    
    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        return self._repository.obtener_por_id(cliente_id)
    
    def listar_clientes(self) -> List[Cliente]:
        """Lista todos los clientes."""
        return self._repository.obtener_todos()
    
    def buscar_clientes(self, nombre: str) -> List[Cliente]:
        """Busca clientes por nombre."""
        return self._repository.buscar_por_nombre(nombre.strip())
    
    def actualizar_cliente(self, cliente_id: int, dto: ClienteUpdateDTO) -> Cliente:
        """Actualiza un cliente existente."""
        cliente = self._repository.obtener_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente con ID {cliente_id} no encontrado")
        
        if dto.nombre is not None:
            cliente.actualizar_informacion(nombre=dto.nombre)
        if dto.telefono is not None:
            cliente.actualizar_informacion(telefono=dto.telefono)
        if dto.direccion is not None:
            cliente.actualizar_informacion(direccion=dto.direccion)
        if dto.email is not None:
            cliente.actualizar_informacion(email=dto.email)
        
        return self._repository.actualizar(cliente)
    
    def eliminar_cliente(self, cliente_id: int) -> bool:
        """Elimina un cliente."""
        return self._repository.eliminar(cliente_id)