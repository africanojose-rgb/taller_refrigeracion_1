import pytest
from domain.entities.cliente import Cliente


class TestClienteEntity:
    
    def test_crear_cliente_valido(self):
        cliente = Cliente(nombre="Juan Pérez", telefono="555-1234", direccion="Calle 123", email="juan@test.com")
        assert cliente.nombre == "Juan Pérez"
        assert cliente.telefono == "555-1234"
    
    def test_cliente_sin_nombre_lanza_error(self):
        with pytest.raises(ValueError, match="nombre.*obligatorio"):
            Cliente(nombre="", telefono="555-1234")
    
    def test_cliente_sin_telefono_lanza_error(self):
        with pytest.raises(ValueError, match="teléfono.*obligatorio"):
            Cliente(nombre="Juan", telefono="")
    
    def test_actualizar_informacion(self):
        cliente = Cliente(nombre="Juan", telefono="555-1234")
        cliente.actualizar_informacion(telefono="555-9999", email="nuevo@test.com")
        assert cliente.telefono == "555-9999"
        assert cliente.email == "nuevo@test.com"