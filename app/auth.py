"""
Utilidades para autenticación y autorización con JWT
"""
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.database import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol

load_dotenv()

# Configuración
SECRET_KEY = os.getenv(
    "SECRET_KEY", "tu-clave-secreta-super-segura-cambiar-en-produccion")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash de contraseña"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtener usuario actual desde el token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Verificar que el usuario esté activo"""
    # Aquí puedes agregar validación de usuario activo si tienes ese campo
    return current_user


class RoleChecker:
    """Clase para verificar roles de usuario"""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        current_user: Usuario = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> Usuario:
        """Verificar que el usuario tenga uno de los roles permitidos"""
        # Obtener el rol del usuario
        if current_user.id_rol:
            rol = db.query(Rol).filter(
                Rol.id_rol == current_user.id_rol).first()
            if rol and rol.nombre_rol in self.allowed_roles:
                return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tiene permisos. Se requiere uno de estos roles: {', '.join(self.allowed_roles)}"
        )


# ============================================================
# FUNCIONES DE AUTORIZACIÓN POR ROL
# ============================================================

# Rol 1: ADMINISTRADOR - Acceso total
def require_admin(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Requiere rol de Administrador"""
    checker = RoleChecker(["Administrador", "administrador", "ADMINISTRADOR"])
    return checker(current_user, db)


# Rol 2: TÉCNICO DE MANTENIMIENTO - Mantenimientos, repuestos, equipos
def require_tecnico(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Requiere rol de Técnico de Mantenimiento"""
    checker = RoleChecker([
        "Técnico de Mantenimiento",
        "TÉCNICO DE MANTENIMIENTO",
        "tecnico de mantenimiento",
        "Tecnico de Mantenimiento",
        "Tecnico De Mantenimiento"  # Forma exacta en BD
    ])
    return checker(current_user, db)


# Rol 3: RESPONSABLE DE COMPRAS - Compras, proveedores, repuestos
def require_compras(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Requiere rol de Responsable de Compras"""
    checker = RoleChecker([
        "Responsable de Compras",
        "RESPONSABLE DE COMPRAS",
        "responsable de compras"
    ])
    return checker(current_user, db)


# Rol 4: GESTOR BIOMÉDICO - Equipos, clientes, ventas, inventario
def require_gestor(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Requiere rol de Gestor Biomédico"""
    checker = RoleChecker([
        "Gestor Biomédico",
        "GESTOR BIOMÉDICO",
        "gestor biomedico",
        "Gestor Biomedico"  # Forma exacta en BD (sin tilde)
    ])
    return checker(current_user, db)


# Rol 5: USUARIO CONSULTA - Solo lectura
def require_consulta(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Requiere rol de Usuario Consulta (solo lectura)"""
    checker = RoleChecker([
        "Usuario Consulta",
        "USUARIO CONSULTA",
        "usuario consulta"
    ])
    return checker(current_user, db)


# ============================================================
# COMBINACIONES DE ROLES (para endpoints que aceptan varios roles)
# ============================================================

def require_admin_or_tecnico(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Administrador o Técnico de Mantenimiento"""
    checker = RoleChecker([
        "Administrador", "ADMINISTRADOR",
        "Técnico de Mantenimiento", "TÉCNICO DE MANTENIMIENTO",
        "Tecnico De Mantenimiento"  # Forma exacta en BD
    ])
    return checker(current_user, db)


def require_admin_or_compras(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Administrador o Responsable de Compras"""
    checker = RoleChecker([
        "Administrador", "ADMINISTRADOR",
        "Responsable de Compras", "RESPONSABLE DE COMPRAS"
    ])
    return checker(current_user, db)


def require_admin_or_gestor(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Administrador o Gestor Biomédico"""
    checker = RoleChecker([
        "Administrador", "ADMINISTRADOR",
        "Gestor Biomédico", "GESTOR BIOMÉDICO",
        "Gestor Biomedico"  # Forma exacta en BD (sin tilde)
    ])
    return checker(current_user, db)


def require_admin_gestor_or_compras(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Administrador, Gestor Biomédico o Responsable de Compras"""
    checker = RoleChecker([
        "Administrador", "ADMINISTRADOR",
        "Gestor Biomédico", "GESTOR BIOMÉDICO",
        "Gestor Biomedico",  # Forma exacta en BD (sin tilde)
        "Responsable de Compras", "RESPONSABLE DE COMPRAS"
    ])
    return checker(current_user, db)


def require_admin_tecnico_or_compras(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Usuario:
    """Administrador, Técnico de Mantenimiento o Responsable de Compras"""
    checker = RoleChecker([
        "Administrador", "ADMINISTRADOR",
        "Técnico de Mantenimiento", "TÉCNICO DE MANTENIMIENTO",
        "Tecnico De Mantenimiento",  # Forma exacta en BD
        "Responsable de Compras", "RESPONSABLE DE COMPRAS"
    ])
    return checker(current_user, db)


def require_any_authenticated(
    current_user: Usuario = Depends(get_current_active_user)
) -> Usuario:
    """Cualquier usuario autenticado (todos los roles)"""
    return current_user
