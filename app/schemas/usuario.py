"""
Schemas de Pydantic para validación de datos de USUARIO
"""
from typing import Optional
from pydantic import BaseModel


class UsuarioBase(BaseModel):
    nombre_completo: Optional[str] = None
    nombre_usuario: str
    id_rol: int


class UsuarioCreate(UsuarioBase):
    contrasena: str  # Contraseña sin hashear (se hasheará en el backend)


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    nombre_usuario: Optional[str] = None
    id_rol: Optional[int] = None
    contrasena: Optional[str] = None  # Opcional para cambiar contraseña


class Usuario(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True


class UsuarioConRol(Usuario):
    """Usuario con información del rol incluida"""
    rol: Optional["RolSimple"] = None

    class Config:
        from_attributes = True


class RolSimple(BaseModel):
    """Schema simplificado de Rol para evitar importaciones circulares"""
    id_rol: int
    nombre_rol: str

    class Config:
        from_attributes = True
