from infrastructure.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    Enum as SQLEnum,
    Text,
)
from sqlalchemy.orm import relationship
import enum


class EstadoOrdenEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    TERMINADO = "terminado"
    CANCELADO = "cancelado"


class EstadoFacturaEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    PAGADA = "pagada"
    ANULADA = "anulada"


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(50), nullable=False)
    direccion = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)

    equipos = relationship("EquipoModel", back_populates="cliente")


class EquipoModel(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_equipo = Column(String(100), nullable=False)
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=True)
    serial = Column(String(100), nullable=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("ClienteModel", back_populates="equipos")
    ordenes = relationship("OrdenModel", back_populates="equipo")


class TecnicoModel(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    especialidad = Column(String(100), nullable=False)
    telefono = Column(String(50), nullable=False)

    ordenes = relationship("OrdenModel", back_populates="tecnico")


class OrdenModel(Base):
    __tablename__ = "ordenes_servicio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(Date, nullable=False)
    fecha_entrega = Column(Date, nullable=True)
    estado = Column(
        SQLEnum(EstadoOrdenEnum), nullable=False, default=EstadoOrdenEnum.PENDIENTE
    )
    descripcion_falla = Column(String(1000), nullable=True)
    diagnostico = Column(String(1000), nullable=True)
    solucion = Column(String(1000), nullable=True)
    mano_obra = Column(Float, nullable=False, default=0.0)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=False)

    equipo = relationship("EquipoModel", back_populates="ordenes")
    tecnico = relationship("TecnicoModel", back_populates="ordenes")
    items = relationship("ItemOrdenModel", back_populates="orden")


class RepuestoModel(Base):
    __tablename__ = "repuestos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(500), nullable=True)
    costo_compra = Column(Float, nullable=False, default=0.0)
    precio_venta = Column(Float, nullable=False, default=0.0)
    cantidad_stock = Column(Integer, nullable=False, default=0)
    cantidad_minima = Column(Integer, nullable=False, default=5)

    items = relationship("ItemOrdenModel", back_populates="repuesto")


class ItemOrdenModel(Base):
    __tablename__ = "items_orden"

    id = Column(Integer, primary_key=True, autoincrement=True)
    orden_id = Column(Integer, ForeignKey("ordenes_servicio.id"), nullable=False)
    repuesto_id = Column(Integer, ForeignKey("repuestos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Float, nullable=False, default=0.0)

    orden = relationship("OrdenModel", back_populates="items")
    repuesto = relationship("RepuestoModel", back_populates="items")


class FacturaModel(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_factura = Column(String(50), nullable=False, unique=True)
    fecha = Column(Date, nullable=False)
    orden_id = Column(Integer, ForeignKey("ordenes_servicio.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("tecnicos.id"), nullable=False)
    subtotal = Column(Float, nullable=False, default=0.0)
    iva = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    estado = Column(
        SQLEnum(EstadoFacturaEnum), nullable=False, default=EstadoFacturaEnum.PENDIENTE
    )
    ruta_pdf = Column(String(500), nullable=True)
    observaciones = Column(Text, nullable=True)
