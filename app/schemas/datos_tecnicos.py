"""
Schemas de Pydantic para validación de datos de DATOS_TECNICOS
"""
from typing import Optional
from pydantic import BaseModel


class DatosTecnicosBase(BaseModel):
    id_equipo: int
    voltaje_operacion: Optional[str] = None
    potencia: Optional[str] = None
    frecuencia: Optional[str] = None
    peso: Optional[str] = None
    dimensiones: Optional[str] = None
    vida_util: Optional[str] = None
    manual_operacion: Optional[str] = None
    observaciones: Optional[str] = None


class DatosTecnicosCreate(DatosTecnicosBase):
    pass


class DatosTecnicosUpdate(BaseModel):
    voltaje_operacion: Optional[str] = None
    potencia: Optional[str] = None
    frecuencia: Optional[str] = None
    peso: Optional[str] = None
    dimensiones: Optional[str] = None
    vida_util: Optional[str] = None
    manual_operacion: Optional[str] = None
    observaciones: Optional[str] = None


class DatosTecnicos(DatosTecnicosBase):
    id_dato_tecnico: int

    class Config:
        from_attributes = True


class DatosTecnicosConEquipo(DatosTecnicos):
    """Datos técnicos con información del equipo"""
    equipo: Optional["EquipoSimple"] = None

    class Config:
        from_attributes = True


class EquipoSimple(BaseModel):
    """Schema simplificado de Equipo para evitar importaciones circulares"""
    id_equipo: int
    nombre_equipo: str
    modelo: Optional[str] = None

    class Config:
        from_attributes = True
