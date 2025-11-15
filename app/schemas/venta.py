"""
Schemas de Pydantic para validación de datos de VENTA
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class VentaBase(BaseModel):
    id_cliente: int
    id_usuario_vendedor: Optional[int] = None
    fecha_venta: Optional[date] = None
    monto_total: Optional[Decimal] = None
    estado_venta: Optional[str] = None


class VentaCreate(VentaBase):
    pass


class VentaUpdate(BaseModel):
    id_cliente: Optional[int] = None
    id_usuario_vendedor: Optional[int] = None
    fecha_venta: Optional[date] = None
    monto_total: Optional[Decimal] = None
    estado_venta: Optional[str] = None


class Venta(VentaBase):
    id_venta: int

    class Config:
        from_attributes = True


class VentaDetallada(Venta):
    """Venta con detalles de los ítems y cliente incluidos"""
    cliente: Optional["ClienteSimple"] = None
    detalles: Optional[List["DetalleVentaSimple"]] = None

    class Config:
        from_attributes = True


# Schemas simplificados
class ClienteSimple(BaseModel):
    id_cliente: int
    nombre_institucion: str

    class Config:
        from_attributes = True


class DetalleVentaSimple(BaseModel):
    id_detalle_venta: int
    id_equipo: int
    precio_venta: Optional[Decimal] = None

    class Config:
        from_attributes = True
