"""
Schemas de Pydantic para validación de datos de NIVEL_RIESGO
"""
from typing import Optional
from pydantic import BaseModel


class NivelRiesgoBase(BaseModel):
    nombre_riesgo: str
    descripcion: Optional[str] = None


class NivelRiesgoCreate(NivelRiesgoBase):
    pass


class NivelRiesgoUpdate(BaseModel):
    nombre_riesgo: Optional[str] = None
    descripcion: Optional[str] = None


class NivelRiesgo(NivelRiesgoBase):
    id_riesgo: int

    class Config:
        from_attributes = True
