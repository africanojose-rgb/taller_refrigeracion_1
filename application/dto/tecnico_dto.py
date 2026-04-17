from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TecnicoCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    especialidad: str = Field(..., min_length=1, max_length=100)
    telefono: str = Field(..., min_length=1, max_length=50)


class TecnicoUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    especialidad: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, min_length=1, max_length=50)


class TecnicoResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    especialidad: str
    telefono: str