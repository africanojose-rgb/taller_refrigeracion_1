from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class OrdenCreateDTO(BaseModel):
    descripcion_falla: Optional[str] = Field(None, max_length=1000)
    equipo_id: int = Field(..., gt=0)
    tecnico_id: int = Field(..., gt=0)


class OrdenUpdateDTO(BaseModel):
    descripcion_falla: Optional[str] = Field(None, max_length=1000)
    diagnostico: Optional[str] = Field(None, max_length=1000)
    solucion: Optional[str] = Field(None, max_length=1000)
    mano_obra: Optional[float] = Field(None, ge=0)
    estado: Optional[str] = None


class OrdenCompletarDTO(BaseModel):
    diagnostico: str = Field(..., min_length=1, max_length=1000)
    solucion: str = Field(..., min_length=1, max_length=1000)
    mano_obra: float = Field(..., ge=0)
    fecha_entrega: Optional[date] = None


class ItemOrdenDTO(BaseModel):
    repuesto_id: int = Field(..., gt=0)
    cantidad: int = Field(1, gt=0)
    precio_unitario: float = Field(..., ge=0)


class OrdenResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    fecha_ingreso: date
    fecha_entrega: Optional[date]
    estado: str
    descripcion_falla: str
    diagnostico: str
    solucion: str
    mano_obra: float
    equipo_id: int
    tecnico_id: int