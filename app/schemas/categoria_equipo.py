"""
Schemas de Pydantic para validación de datos de CATEGORIA_EQUIPO
"""
from typing import Optional
from pydantic import BaseModel


class CategoriaEquipoBase(BaseModel):
    nombre_categoria: str
    descripcion: Optional[str] = None


class CategoriaEquipoCreate(CategoriaEquipoBase):
    pass


class CategoriaEquipoUpdate(BaseModel):
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None


class CategoriaEquipo(CategoriaEquipoBase):
    id_categoria: int

    class Config:
        from_attributes = True
