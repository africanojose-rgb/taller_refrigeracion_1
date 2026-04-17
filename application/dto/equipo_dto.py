from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class EquipoCreateDTO(BaseModel):
    tipo_equipo: str = Field(..., min_length=1, max_length=100)
    marca: str = Field(..., min_length=1, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    serial: Optional[str] = Field(None, max_length=100)
    cliente_id: int = Field(..., gt=0)


class EquipoUpdateDTO(BaseModel):
    tipo_equipo: Optional[str] = Field(None, min_length=1, max_length=100)
    marca: Optional[str] = Field(None, min_length=1, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    serial: Optional[str] = Field(None, max_length=100)


class EquipoResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    tipo_equipo: str
    marca: str
    modelo: str
    serial: str
    cliente_id: int