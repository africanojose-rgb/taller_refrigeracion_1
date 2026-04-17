import pytest
from unittest.mock import Mock
from domain.entities.orden_servicio import EstadoOrden
from domain.entities.reporte import ReporteEstadistico, ReporteCliente, ReporteTecnico
from application.use_cases.reporte_use_cases import ReporteUseCases


class TestReporteUseCases:
    
    @pytest.fixture
    def mock_repos(self):
        cliente_repo = Mock()
        equipo_repo = Mock()
        orden_repo = Mock()
        tecnico_repo = Mock()
        return cliente_repo, equipo_repo, orden_repo, tecnico_repo
    
    @pytest.fixture
    def use_cases(self, mock_repos):
        return ReporteUseCases(*mock_repos)
    
    def test_estadisticas_generales_vacias(self, use_cases, mock_repos):
        cliente_repo, equipo_repo, orden_repo, tecnico_repo = mock_repos
        
        cliente_repo.obtener_todos.return_value = []
        equipo_repo.obtener_todos.return_value = []
        orden_repo.obtener_todos.return_value = []
        
        resultado = use_cases.obtener_estadisticas_generales()
        
        assert resultado.total_clientes == 0
        assert resultado.total_ordenes == 0
        assert resultado.ingreso_total == 0.0
    
    def test_estadisticas_generales_con_datos(self, use_cases, mock_repos):
        from domain.entities.cliente import Cliente
        from domain.entities.equipo import Equipo
        from domain.entities.orden_servicio import OrdenServicio
        from datetime import date
        
        cliente_repo, equipo_repo, orden_repo, tecnico_repo = mock_repos
        
        cliente_repo.obtener_todos.return_value = [Cliente(id=1, nombre="Test", telefono="123")]
        equipo_repo.obtener_todos.return_value = [Equipo(id=1, tipo_equipo="Aire", marca="LG", cliente_id=1)]
        orden_repo.obtener_todos.return_value = [
            OrdenServicio(id=1, fecha_ingreso=date.today(), estado=EstadoOrden.TERMINADO, costo=100, equipo_id=1, tecnico_id=1),
            OrdenServicio(id=2, fecha_ingreso=date.today(), estado=EstadoOrden.PENDIENTE, costo=0, equipo_id=1, tecnico_id=1)
        ]
        
        resultado = use_cases.obtener_estadisticas_generales()
        
        assert resultado.total_clientes == 1
        assert resultado.total_ordenes == 2
        assert resultado.ordenes_terminadas == 1
        assert resultado.ingreso_total == 100.0
    
    def test_reporte_cliente(self, use_cases, mock_repos):
        from domain.entities.cliente import Cliente
        from domain.entities.equipo import Equipo
        from domain.entities.orden_servicio import OrdenServicio
        from datetime import date
        
        cliente_repo, equipo_repo, orden_repo, tecnico_repo = mock_repos
        
        cliente_repo.obtener_por_id.return_value = Cliente(id=1, nombre="Test", telefono="123")
        equipo_repo.obtener_por_cliente.return_value = [Equipo(id=1, tipo_equipo="Aire", marca="LG", cliente_id=1)]
        orden_repo.obtener_por_cliente.return_value = [
            OrdenServicio(id=1, fecha_ingreso=date.today(), estado=EstadoOrden.TERMINADO, costo=50, equipo_id=1, tecnico_id=1)
        ]
        
        resultado = use_cases.obtener_reporte_cliente(1)
        
        assert resultado is not None
        assert resultado.nombre == "Test"
        assert resultado.total_equipos == 1
        assert resultado.gasto_total == 50.0
    
    def test_reporte_cliente_inexistente(self, use_cases, mock_repos):
        cliente_repo, _, _, _ = mock_repos
        cliente_repo.obtener_por_id.return_value = None
        
        resultado = use_cases.obtener_reporte_cliente(999)
        
        assert resultado is None
    
    def test_top_clientes(self, use_cases, mock_repos):
        from domain.entities.cliente import Cliente
        from domain.entities.orden_servicio import OrdenServicio
        from datetime import date
        
        cliente_repo, equipo_repo, orden_repo, tecnico_repo = mock_repos
        
        cliente_repo.obtener_todos.return_value = [
            Cliente(id=1, nombre="Cliente A", telefono="1"),
            Cliente(id=2, nombre="Cliente B", telefono="2")
        ]
        equipo_repo.obtener_por_cliente.return_value = []
        orden_repo.obtener_por_cliente.side_effect = [
            [OrdenServicio(id=1, fecha_ingreso=date.today(), estado=EstadoOrden.TERMINADO, costo=100, equipo_id=1, tecnico_id=1)],
            [OrdenServicio(id=2, fecha_ingreso=date.today(), estado=EstadoOrden.TERMINADO, costo=50, equipo_id=2, tecnico_id=1)]
        ]
        
        resultado = use_cases.listar_top_clientes()
        
        assert len(resultado) == 2
        assert resultado[0].gasto_total == 100.0