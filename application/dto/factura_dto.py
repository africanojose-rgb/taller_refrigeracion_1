from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class FacturaCreateDTO(BaseModel):
    orden_id: int = Field(..., gt=0)
    cliente_id: int = Field(..., gt=0)
    equipo_id: int = Field(..., gt=0)
    tecnico_id: int = Field(..., gt=0)
    subtotal: float = Field(..., ge=0)
    iva: float = Field(0, ge=0)
    observaciones: Optional[str] = Field(None, max_length=1000)


class FacturaUpdateDTO(BaseModel):
    subtotal: Optional[float] = Field(None, ge=0)
    iva: Optional[float] = Field(None, ge=0)
    observaciones: Optional[str] = Field(None, max_length=1000)


class FacturaResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_factura: str
    fecha: date
    orden_id: int
    cliente_id: int
    equipo_id: int
    tecnico_id: int
    subtotal: float
    iva: float
    total: float
    estado: str
    ruta_pdf: str
    observaciones: str


class GenerarFacturaDTO(BaseModel):
    orden_id: int = Field(..., gt=0)
    iva: float = Field(0, ge=0, le=1)
    observaciones: Optional[str] = Field(None, max_length=1000)
