from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RepuestoCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    codigo: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=500)
    costo_compra: float = Field(..., ge=0)
    precio_venta: float = Field(..., ge=0)
    cantidad_stock: int = Field(0, ge=0)
    cantidad_minima: int = Field(5, ge=0)


class RepuestoUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = Field(None, max_length=500)
    costo_compra: Optional[float] = Field(None, ge=0)
    precio_venta: Optional[float] = Field(None, ge=0)
    cantidad_stock: Optional[int] = Field(None, ge=0)
    cantidad_minima: Optional[int] = Field(None, ge=0)


class RepuestoResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    codigo: str
    descripcion: str
    costo_compra: float
    precio_venta: float
    cantidad_stock: int
    cantidad_minima: int