"""
Schemas de Pydantic para validación de datos de COMPRA_ADQUISICION
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class CompraAdquisicionBase(BaseModel):
    numero_factura: Optional[str] = None
    fecha_compra: Optional[date] = None
    proveedor: Optional[str] = None
    total_compra: Optional[Decimal] = None
    metodo_pago: Optional[str] = None
    observaciones: Optional[str] = None
    id_usuario_registro: Optional[int] = None


class CompraAdquisicionCreate(CompraAdquisicionBase):
    pass


class CompraAdquisicionUpdate(BaseModel):
    numero_factura: Optional[str] = None
    fecha_compra: Optional[date] = None
    proveedor: Optional[str] = None
    total_compra: Optional[Decimal] = None
    metodo_pago: Optional[str] = None
    observaciones: Optional[str] = None
    id_usuario_registro: Optional[int] = None


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
    id_detalle_compra: int
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
