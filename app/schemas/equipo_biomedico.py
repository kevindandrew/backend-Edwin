"""
Schemas de Pydantic para validación de datos de EQUIPO_BIOMEDICO
"""
from typing import Optional
from pydantic import BaseModel
from datetime import date


class EquipoBiomedicoBase(BaseModel):
    nombre_equipo: str
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    garantia: Optional[str] = None
    proveedor: Optional[str] = None
    estado: Optional[str] = None
    id_ubicacion: Optional[int] = None
    id_fabricante: Optional[int] = None
    id_categoria: Optional[int] = None
    id_riesgo: Optional[int] = None
    id_tecnologia: Optional[int] = None
    id_usuario_registro: Optional[int] = None


class EquipoBiomedicoCreate(EquipoBiomedicoBase):
    pass


class EquipoBiomedicoUpdate(BaseModel):
    nombre_equipo: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    garantia: Optional[str] = None
    proveedor: Optional[str] = None
    estado: Optional[str] = None
    id_ubicacion: Optional[int] = None
    id_fabricante: Optional[int] = None
    id_categoria: Optional[int] = None
    id_riesgo: Optional[int] = None
    id_tecnologia: Optional[int] = None
    id_usuario_registro: Optional[int] = None


class EquipoBiomedico(EquipoBiomedicoBase):
    id_equipo: int

    class Config:
        from_attributes = True


class EquipoBiomedicoDetallado(EquipoBiomedico):
    """Equipo con relaciones incluidas"""
    ubicacion: Optional["UbicacionSimple"] = None
    fabricante: Optional["FabricanteSimple"] = None
    categoria: Optional["CategoriaSimple"] = None
    nivel_riesgo: Optional["NivelRiesgoSimple"] = None
    tecnologia: Optional["TecnologiaSimple"] = None
    datos_tecnicos: Optional["DatosTecnicosSimple"] = None

    class Config:
        from_attributes = True


# Schemas simplificados para evitar importaciones circulares
class UbicacionSimple(BaseModel):
    id_ubicacion: int
    nombre_ubicacion: Optional[str] = None

    class Config:
        from_attributes = True


class FabricanteSimple(BaseModel):
    id_fabricante: int
    nombre_fabricante: str

    class Config:
        from_attributes = True


class CategoriaSimple(BaseModel):
    id_categoria: int
    nombre_categoria: str

    class Config:
        from_attributes = True


class NivelRiesgoSimple(BaseModel):
    id_riesgo: int
    nombre_riesgo: str

    class Config:
        from_attributes = True


class TecnologiaSimple(BaseModel):
    id_tecnologia: int
    nombre_tecnologia: str

    class Config:
        from_attributes = True


class DatosTecnicosSimple(BaseModel):
    id_dato_tecnico: int
    voltaje_operacion: Optional[str] = None
    potencia: Optional[str] = None
    frecuencia: Optional[str] = None

    class Config:
        from_attributes = True
