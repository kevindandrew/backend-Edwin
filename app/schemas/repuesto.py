"""
Schemas de Pydantic para validación de datos de REPUESTO
"""
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


class RepuestoBase(BaseModel):
    nombre_repuesto: str
    descripcion: Optional[str] = None
    precio_unitario: Optional[Decimal] = None
    stock_disponible: Optional[int] = 0
    proveedor: Optional[str] = None


class RepuestoCreate(RepuestoBase):
    pass


class RepuestoUpdate(BaseModel):
    nombre_repuesto: Optional[str] = None
    descripcion: Optional[str] = None
    precio_unitario: Optional[Decimal] = None
    stock_disponible: Optional[int] = None
    proveedor: Optional[str] = None


class Repuesto(RepuestoBase):
    id_repuesto: int

    class Config:
        from_attributes = True
