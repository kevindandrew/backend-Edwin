"""
Router para operaciones CRUD de Usuarios
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioConRol
from app.auth import require_admin

# Configuración para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/usuarios",
    tags=[" Módulo 1: Seguridad y Roles"],
    responses={404: {"description": "No encontrado"}},
)


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear un nuevo usuario con contraseña hasheada (Solo Administrador)
    """
    try:
        # Verificar si ya existe un usuario con ese nombre
        db_usuario = db.query(UsuarioModel).filter(
            UsuarioModel.nombre_usuario == usuario.nombre_usuario
        ).first()
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con ese nombre de usuario"
            )

        # Verificar que el rol existe
        from app.models.rol import Rol as RolModel
        db_rol = db.query(RolModel).filter(
            RolModel.id_rol == usuario.id_rol).first()
        if not db_rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rol con ID {usuario.id_rol} no encontrado"
            )

        # Crear usuario con contraseña hasheada
        usuario_dict = usuario.model_dump(exclude={'contrasena'})
        usuario_dict['contrasena_hash'] = hash_password(usuario.contrasena)

        db_usuario = UsuarioModel(**usuario_dict)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )


@router.get("/", response_model=List[UsuarioConRol])
def obtener_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de usuarios con información de rol (Solo Administrador)
    """
    try:
        usuarios = db.query(UsuarioModel).offset(skip).limit(limit).all()
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}"
        )


@router.get("/{usuario_id}", response_model=UsuarioConRol)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener un usuario específico por ID con información de rol (Solo Administrador)
    """
    try:
        db_usuario = db.query(UsuarioModel).filter(
            UsuarioModel.id_usuario == usuario_id
        ).first()
        if db_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return db_usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}"
        )


@router.put("/{usuario_id}", response_model=Usuario)
def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Actualizar un usuario existente (Solo Administrador)
    """
    try:
        db_usuario = db.query(UsuarioModel).filter(
            UsuarioModel.id_usuario == usuario_id
        ).first()
        if db_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Actualizar campos
        usuario_data = usuario.model_dump(
            exclude_unset=True, exclude={'contrasena'})

        # Si se proporciona nueva contraseña, hashearla
        if usuario.contrasena:
            usuario_data['contrasena_hash'] = hash_password(usuario.contrasena)

        # Verificar nombre de usuario único si se está cambiando
        if 'nombre_usuario' in usuario_data and usuario_data['nombre_usuario'] != db_usuario.nombre_usuario:
            existing = db.query(UsuarioModel).filter(
                UsuarioModel.nombre_usuario == usuario_data['nombre_usuario']
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un usuario con ese nombre de usuario"
                )

        # Verificar que el rol existe si se está cambiando
        if 'id_rol' in usuario_data:
            from app.models.rol import Rol as RolModel
            db_rol = db.query(RolModel).filter(
                RolModel.id_rol == usuario_data['id_rol']).first()
            if not db_rol:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rol con ID {usuario_data['id_rol']} no encontrado"
                )

        for key, value in usuario_data.items():
            setattr(db_usuario, key, value)

        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}"
        )


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Eliminar un usuario (Solo Administrador)
    """
    try:
        db_usuario = db.query(UsuarioModel).filter(
            UsuarioModel.id_usuario == usuario_id
        ).first()
        if db_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        db.delete(db_usuario)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}"
        )


@router.get("/username/{nombre_usuario}", response_model=UsuarioConRol)
def obtener_usuario_por_nombre(
    nombre_usuario: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener un usuario por nombre de usuario (Solo Administrador)
    """
    try:
        db_usuario = db.query(UsuarioModel).filter(
            UsuarioModel.nombre_usuario == nombre_usuario
        ).first()
        if db_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return db_usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}"
        )
