"""
Router para autenticación y login
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.auth import Token, LoginRequest, LoginResponse
from app.auth import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={401: {"description": "No autorizado"}},
)


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Iniciar sesión y obtener token JWT
    """
    # Buscar usuario por nombre de usuario
    user = db.query(Usuario).filter(
        Usuario.nombre_usuario == credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar contraseña
    if not verify_password(credentials.password, user.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Obtener información del rol
    rol_info = None
    if user.id_rol:
        rol = db.query(Rol).filter(Rol.id_rol == user.id_rol).first()
        if rol:
            rol_info = {
                "id_rol": rol.id_rol,
                "nombre_rol": rol.nombre_rol
            }

    # Crear token de acceso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre_usuario},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id_usuario": user.id_usuario,
            "nombre_usuario": user.nombre_usuario,
            "nombre_completo": user.nombre_completo,
            "rol": rol_info
        }
    }


@router.get("/me")
def get_current_user_info(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtener información del usuario actual autenticado
    """
    # Obtener información del rol
    rol_info = None
    if current_user.id_rol:
        rol = db.query(Rol).filter(Rol.id_rol == current_user.id_rol).first()
        if rol:
            rol_info = {
                "id_rol": rol.id_rol,
                "nombre_rol": rol.nombre_rol
            }

    return {
        "id_usuario": current_user.id_usuario,
        "nombre_usuario": current_user.nombre_usuario,
        "nombre_completo": current_user.nombre_completo,
        "rol": rol_info
    }
