"""
Schemas de Pydantic para validación de datos de TIPO_TECNOLOGIA
"""
from typing import Optional
from pydantic import BaseModel


class TipoTecnologiaBase(BaseModel):
    nombre_tecnologia: str
    descripcion: Optional[str] = None


class TipoTecnologiaCreate(TipoTecnologiaBase):
    pass


class TipoTecnologiaUpdate(BaseModel):
    nombre_tecnologia: Optional[str] = None
    descripcion: Optional[str] = None


class TipoTecnologia(TipoTecnologiaBase):
    id_tecnologia: int

    class Config:
        from_attributes = True
