"""
Schemas de Pydantic para validación de datos de VENTA
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class VentaBase(BaseModel):
    numero_factura: Optional[str] = None
    fecha_venta: Optional[date] = None
    id_cliente: Optional[int] = None
    total_venta: Optional[Decimal] = None
    metodo_pago: Optional[str] = None
    estado_venta: Optional[str] = None
    observaciones: Optional[str] = None
    id_usuario_registro: Optional[int] = None


class VentaCreate(VentaBase):
    pass


class VentaUpdate(BaseModel):
    numero_factura: Optional[str] = None
    fecha_venta: Optional[date] = None
    id_cliente: Optional[int] = None
    total_venta: Optional[Decimal] = None
    metodo_pago: Optional[str] = None
    estado_venta: Optional[str] = None
    observaciones: Optional[str] = None
    id_usuario_registro: Optional[int] = None


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
    nombre_cliente: str
    nit_ruc: Optional[str] = None

    class Config:
        from_attributes = True


class DetalleVentaSimple(BaseModel):
    id_detalle_venta: int
    cantidad: int
    precio_unitario: Optional[Decimal] = None
    subtotal: Optional[Decimal] = None
    descripcion: Optional[str] = None
    equipo: Optional["EquipoSimple"] = None

    class Config:
        from_attributes = True


class EquipoSimple(BaseModel):
    id_equipo: int
    nombre_equipo: str
    modelo: Optional[str] = None

    class Config:
        from_attributes = True
