"""
Schemas de Pydantic para validación de datos de COMPRA_ADQUISICION
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class CompraAdquisicionBase(BaseModel):
    fecha_solicitud: Optional[date] = None
    fecha_aprobacion: Optional[date] = None
    estado_compra: Optional[str] = None
    monto_total: Optional[Decimal] = None
    id_usuario_admin: Optional[int] = None


class CompraAdquisicionCreate(CompraAdquisicionBase):
    pass


class CompraAdquisicionUpdate(BaseModel):
    fecha_solicitud: Optional[date] = None
    fecha_aprobacion: Optional[date] = None
    estado_compra: Optional[str] = None
    monto_total: Optional[Decimal] = None
    id_usuario_admin: Optional[int] = None


class CompraAdquisicion(CompraAdquisicionBase):
    id_compra: int

    class Config:
        from_attributes = True


class CompraAdquisicionDetallada(CompraAdquisicion):
    """Compra con detalles de los ítems incluidos"""
    detalles: Optional[List["DetalleCompraSimple"]] = None

    class Config:
        from_attributes = True


# Schemas simplificados
class DetalleCompraSimple(BaseModel):
    id_detalle: int
    cantidad: Optional[int] = None
    precio_unitario: Optional[Decimal] = None
    id_repuesto: Optional[int] = None
    id_equipo: Optional[int] = None

    class Config:
        from_attributes = True
