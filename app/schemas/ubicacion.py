"""
Schemas de Pydantic para validación de datos de UBICACION
"""
from typing import Optional
from pydantic import BaseModel


class UbicacionBase(BaseModel):
    nombre_ubicacion: Optional[str] = None
    id_cliente: Optional[int] = None


class UbicacionCreate(UbicacionBase):
    pass


class UbicacionUpdate(BaseModel):
    nombre_ubicacion: Optional[str] = None
    id_cliente: Optional[int] = None


class Ubicacion(UbicacionBase):
    id_ubicacion: int

    class Config:
        from_attributes = True


class UbicacionConCliente(Ubicacion):
    """Ubicación con información del cliente incluida"""
    cliente: Optional["ClienteSimple"] = None

    class Config:
        from_attributes = True


class ClienteSimple(BaseModel):
    """Schema simplificado de Cliente para evitar importaciones circulares"""
    id_cliente: int
    nombre_institucion: str

    class Config:
        from_attributes = True
