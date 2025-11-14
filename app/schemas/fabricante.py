"""
Schemas de Pydantic para validación de datos de FABRICANTE
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class FabricanteBase(BaseModel):
    nombre_fabricante: str
    pais_origen: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    sitio_web: Optional[str] = None


class FabricanteCreate(FabricanteBase):
    pass


class FabricanteUpdate(BaseModel):
    nombre_fabricante: Optional[str] = None
    pais_origen: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    sitio_web: Optional[str] = None


class Fabricante(FabricanteBase):
    id_fabricante: int

    class Config:
        from_attributes = True
