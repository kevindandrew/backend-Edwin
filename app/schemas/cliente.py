"""
Schemas de Pydantic para validación de datos de CLIENTE
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nombre_institucion: str
    nit_ruc: Optional[str] = None
    direccion: Optional[str] = None
    telefono_contacto: Optional[str] = None
    email_contacto: Optional[str] = None
    persona_contacto: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre_institucion: Optional[str] = None
    nit_ruc: Optional[str] = None
    direccion: Optional[str] = None
    telefono_contacto: Optional[str] = None
    email_contacto: Optional[str] = None
    persona_contacto: Optional[str] = None


class Cliente(ClienteBase):
    id_cliente: int

    class Config:
        from_attributes = True


class ClienteConUbicaciones(Cliente):
    """Cliente con sus ubicaciones incluidas"""
    ubicaciones: list["UbicacionSimple"] = []

    class Config:
        from_attributes = True


class UbicacionSimple(BaseModel):
    """Schema simplificado de Ubicación para evitar importaciones circulares"""
    id_ubicacion: int
    nombre_ubicacion: Optional[str] = None

    class Config:
        from_attributes = True
