"""
Schemas de Pydantic para validación de datos de DETALLE_COMPRA
"""
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import date


class DetalleCompraBase(BaseModel):
    id_compra: int
    id_repuesto: Optional[int] = None
    id_equipo: Optional[int] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[Decimal] = None


class DetalleCompraCreate(DetalleCompraBase):
    pass


class DetalleCompraUpdate(BaseModel):
    id_repuesto: Optional[int] = None
    id_equipo: Optional[int] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[Decimal] = None


class DetalleCompra(DetalleCompraBase):
    id_detalle: int

    class Config:
        from_attributes = True


class DetalleCompraConRelaciones(DetalleCompra):
    """Detalle de compra con información de la compra y equipo"""
    compra: Optional["CompraSimple"] = None
    equipo: Optional["EquipoSimple"] = None

    class Config:
        from_attributes = True


# Schemas simplificados
class CompraSimple(BaseModel):
    id_compra: int
    fecha_solicitud: Optional[date] = None
    estado_compra: Optional[str] = None

    class Config:
        from_attributes = True


class EquipoSimple(BaseModel):
    id_equipo: int
    nombre_equipo: str
    modelo: Optional[str] = None

    class Config:
        from_attributes = True
