"""
Schemas de Pydantic para validación de datos de REPUESTO
"""
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


class RepuestoBase(BaseModel):
    nombre: str
    stock: Optional[int] = 0
    stock_minimo: Optional[int] = 0
    id_tecnologia: Optional[int] = None


class RepuestoCreate(RepuestoBase):
    pass


class RepuestoUpdate(BaseModel):
    nombre: Optional[str] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    id_tecnologia: Optional[int] = None


class Repuesto(RepuestoBase):
    id_repuesto: int

    class Config:
        from_attributes = True
