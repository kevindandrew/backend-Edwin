"""
Schemas de Pydantic para validación de datos de MANTENIMIENTO
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class MantenimientoBase(BaseModel):
    id_equipo: int
    tipo_mantenimiento: Optional[str] = None
    fecha_programada: Optional[date] = None
    fecha_realizacion: Optional[date] = None
    descripcion_trabajo: Optional[str] = None
    costo_total: Optional[Decimal] = None
    id_tecnico: Optional[int] = None


class MantenimientoCreate(MantenimientoBase):
    pass


class MantenimientoUpdate(BaseModel):
    id_equipo: Optional[int] = None
    tipo_mantenimiento: Optional[str] = None
    fecha_programada: Optional[date] = None
    fecha_realizacion: Optional[date] = None
    descripcion_trabajo: Optional[str] = None
    costo_total: Optional[Decimal] = None
    id_tecnico: Optional[int] = None


class Mantenimiento(MantenimientoBase):
    id_mantenimiento: int

    class Config:
        from_attributes = True


class MantenimientoDetallado(Mantenimiento):
    """Mantenimiento con relaciones incluidas"""
    equipo: Optional["EquipoSimple"] = None
    uso_repuestos: Optional[List["UsoRepuestoDetallado"]] = None

    class Config:
        from_attributes = True


# Schemas simplificados para evitar importaciones circulares
class EquipoSimple(BaseModel):
    id_equipo: int
    nombre_equipo: str
    modelo: Optional[str] = None

    class Config:
        from_attributes = True


class UsoRepuestoDetallado(BaseModel):
    id_repuesto: int
    cantidad_usada: Optional[int] = None
    repuesto: Optional["RepuestoSimple"] = None

    class Config:
        from_attributes = True


class RepuestoSimple(BaseModel):
    id_repuesto: int
    nombre: str

    class Config:
        from_attributes = True
