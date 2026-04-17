import pytest
from unittest.mock import Mock, MagicMock
from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository
from application.use_cases.cliente_use_cases import ClienteUseCases
from application.dto.cliente_dto import ClienteCreateDTO, ClienteUpdateDTO


class TestClienteUseCases:
    
    @pytest.fixture
    def mock_repo(self):
        return Mock(spec=ClienteRepository)
    
    @pytest.fixture
    def use_cases(self, mock_repo):
        return ClienteUseCases(mock_repo)
    
    def test_crear_cliente(self, use_cases, mock_repo):
        dto = ClienteCreateDTO(nombre="Juan Pérez", telefono="555-1234")
        
        mock_repo.crear.return_value = Cliente(id=1, nombre="Juan Pérez", telefono="555-1234")
        
        resultado = use_cases.crear_cliente(dto)
        
        mock_repo.crear.assert_called_once()
        assert resultado.id == 1
        assert resultado.nombre == "Juan Pérez"
    
    def test_obtener_cliente_existente(self, use_cases, mock_repo):
        mock_repo.obtener_por_id.return_value = Cliente(id=1, nombre="Juan", telefono="555-1234")
        
        resultado = use_cases.obtener_cliente(1)
        
        assert resultado is not None
        assert resultado.id == 1
    
    def test_obtener_cliente_inexistente(self, use_cases, mock_repo):
        mock_repo.obtener_por_id.return_value = None
        
        resultado = use_cases.obtener_cliente(999)
        
        assert resultado is None
    
    def test_listar_clientes(self, use_cases, mock_repo):
        mock_repo.obtener_todos.return_value = [
            Cliente(id=1, nombre="Juan", telefono="555-1234"),
            Cliente(id=2, nombre="María", telefono="555-5678")
        ]
        
        resultados = use_cases.listar_clientes()
        
        assert len(resultados) == 2
    
    def test_buscar_clientes_por_nombre(self, use_cases, mock_repo):
        mock_repo.buscar_por_nombre.return_value = [
            Cliente(id=1, nombre="Juan Pérez", telefono="555-1234")
        ]
        
        resultados = use_cases.buscar_clientes("Juan")
        
        assert len(resultados) == 1
        mock_repo.buscar_por_nombre.assert_called_once_with("Juan")
    
    def test_actualizar_cliente(self, use_cases, mock_repo):
        cliente_existente = Cliente(id=1, nombre="Juan", telefono="555-1234", direccion="Calle 1")
        mock_repo.obtener_por_id.return_value = cliente_existente
        mock_repo.actualizar.return_value = cliente_existente
        
        dto = ClienteUpdateDTO(nombre="Juan Actualizado")
        resultado = use_cases.actualizar_cliente(1, dto)
        
        assert resultado is not None
    
    def test_actualizar_cliente_inexistente(self, use_cases, mock_repo):
        mock_repo.obtener_por_id.return_value = None
        
        dto = ClienteUpdateDTO(nombre="Nuevo")
        
        with pytest.raises(ValueError, match="no encontrado"):
            use_cases.actualizar_cliente(999, dto)
    
    def test_eliminar_cliente(self, use_cases, mock_repo):
        mock_repo.eliminar.return_value = True
        
        resultado = use_cases.eliminar_cliente(1)
        
        assert resultado is True
        mock_repo.eliminar.assert_called_once_with(1)