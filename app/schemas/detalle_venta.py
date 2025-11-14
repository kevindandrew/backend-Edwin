"""
Schemas de Pydantic para validación de datos de DETALLE_VENTA
"""
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


class DetalleVentaBase(BaseModel):
    id_venta: int
    id_equipo: Optional[int] = None
    cantidad: int
    precio_unitario: Optional[Decimal] = None
    subtotal: Optional[Decimal] = None
    descripcion: Optional[str] = None


class DetalleVentaCreate(DetalleVentaBase):
    pass


class DetalleVentaUpdate(BaseModel):
    id_equipo: Optional[int] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[Decimal] = None
    subtotal: Optional[Decimal] = None
    descripcion: Optional[str] = None


class DetalleVenta(DetalleVentaBase):
    id_detalle_venta: int

    class Config:
        from_attributes = True


class DetalleVentaConRelaciones(DetalleVenta):
    """Detalle de venta con información de la venta y equipo"""
    venta: Optional["VentaSimple"] = None
    equipo: Optional["EquipoSimple"] = None

    class Config:
        from_attributes = True


# Schemas simplificados
class VentaSimple(BaseModel):
    id_venta: int
    numero_factura: Optional[str] = None
    fecha_venta: Optional[str] = None
    estado_venta: Optional[str] = None

    class Config:
        from_attributes = True


class EquipoSimple(BaseModel):
    id_equipo: int
    nombre_equipo: str
    modelo: Optional[str] = None

    class Config:
        from_attributes = True
