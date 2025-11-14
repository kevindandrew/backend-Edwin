"""
Schemas de Pydantic para validación de datos de USO_REPUESTO
"""
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


class UsoRepuestoBase(BaseModel):
    id_mantenimiento: int
    id_repuesto: int
    cantidad_usada: int
    precio_unitario: Optional[Decimal] = None


class UsoRepuestoCreate(UsoRepuestoBase):
    pass


class UsoRepuestoUpdate(BaseModel):
    cantidad_usada: Optional[int] = None
    precio_unitario: Optional[Decimal] = None


class UsoRepuesto(UsoRepuestoBase):

    class Config:
        from_attributes = True


class UsoRepuestoConDetalles(UsoRepuesto):
    """Uso de repuesto con información del mantenimiento y repuesto"""
    mantenimiento: Optional["MantenimientoSimple"] = None
    repuesto: Optional["RepuestoSimple"] = None

    class Config:
        from_attributes = True


# Schemas simplificados para evitar importaciones circulares
class MantenimientoSimple(BaseModel):
    id_mantenimiento: int
    tipo_mantenimiento: Optional[str] = None
    fecha_mantenimiento: Optional[str] = None

    class Config:
        from_attributes = True


class RepuestoSimple(BaseModel):
    id_repuesto: int
    nombre_repuesto: str
    stock_disponible: Optional[int] = None

    class Config:
        from_attributes = True
