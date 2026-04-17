from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class ClienteCreateDTO(BaseModel):
    """DTO para crear un cliente."""
    nombre: str = Field(..., min_length=1, max_length=255)
    telefono: str = Field(..., min_length=1, max_length=50)
    direccion: Optional[str] = Field(None, max_length=500)
    email: Optional[EmailStr] = None


class ClienteUpdateDTO(BaseModel):
    """DTO para actualizar un cliente."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    telefono: Optional[str] = Field(None, min_length=1, max_length=50)
    direccion: Optional[str] = Field(None, max_length=500)
    email: Optional[EmailStr] = None


class ClienteResponseDTO(BaseModel):
    """DTO para responder con datos de cliente."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    direccion: str
    email: str