"""
Schemas de Pydantic para validación de datos de AUDITORIA
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class AuditoriaBase(BaseModel):
    tabla: str
    id_registro: int
    operacion: str
    id_usuario: Optional[int] = None
    datos_anteriores: Optional[Dict[str, Any]] = None
    datos_nuevos: Optional[Dict[str, Any]] = None
    ip_origen: Optional[str] = None


class AuditoriaCreate(AuditoriaBase):
    pass


class Auditoria(AuditoriaBase):
    id_auditoria: int
    fecha_operacion: datetime

    class Config:
        from_attributes = True


class AuditoriaConUsuario(Auditoria):
    """Auditoría con información del usuario que realizó la operación"""
    usuario: Optional["UsuarioSimple"] = None

    class Config:
        from_attributes = True


# Schema simplificado para usuario
class UsuarioSimple(BaseModel):
    id_usuario: int
    nombre_completo: Optional[str] = None
    nombre_usuario: str

    class Config:
        from_attributes = True
