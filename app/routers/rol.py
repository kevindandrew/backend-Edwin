"""
Router para operaciones CRUD de Roles
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rol import Rol as RolModel
from app.schemas.rol import Rol, RolCreate, RolUpdate
from app.auth import require_admin

router = APIRouter(
    prefix="/roles",
    tags=[" Módulo 1: Seguridad y Roles"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Rol, status_code=status.HTTP_201_CREATED)
def crear_rol(
    rol: RolCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear un nuevo rol (Solo Administrador)
    """
    try:
        # Verificar si ya existe un rol con ese nombre
        db_rol = db.query(RolModel).filter(
            RolModel.nombre_rol == rol.nombre_rol).first()
        if db_rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un rol con ese nombre"
            )

        # Crear nuevo rol
        db_rol = RolModel(**rol.model_dump())
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        return db_rol
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear rol: {str(e)}"
        )


@router.get("/", response_model=List[Rol])
def obtener_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de roles (Solo Administrador)
    """
    try:
        roles = db.query(RolModel).offset(skip).limit(limit).all()
        return roles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener roles: {str(e)}"
        )


@router.get("/{rol_id}", response_model=Rol)
def obtener_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener un rol específico por ID (Solo Administrador)
    """
    try:
        db_rol = db.query(RolModel).filter(RolModel.id_rol == rol_id).first()
        if db_rol is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return db_rol
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener rol: {str(e)}"
        )


@router.put("/{rol_id}", response_model=Rol)
def actualizar_rol(
    rol_id: int,
    rol: RolUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Actualizar un rol existente (Solo Administrador)
    """
    try:
        db_rol = db.query(RolModel).filter(RolModel.id_rol == rol_id).first()
        if db_rol is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )

        # Actualizar solo los campos que no son None
        rol_data = rol.model_dump(exclude_unset=True)
        for key, value in rol_data.items():
            setattr(db_rol, key, value)

        db.commit()
        db.refresh(db_rol)
        return db_rol
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar rol: {str(e)}"
        )


@router.delete("/{rol_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Eliminar un rol (Solo Administrador)
    """
    try:
        db_rol = db.query(RolModel).filter(RolModel.id_rol == rol_id).first()
        if db_rol is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )

        db.delete(db_rol)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar rol: {str(e)}"
        )


@router.get("/test/conexion")
def probar_conexion_db(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Endpoint para probar la conexión a la base de datos EXISTENTE (sin modificar)
    """
    try:
        # Intentar hacer una consulta simple sin modificar datos
        result = db.execute("SELECT 1 as test")
        test_value = result.fetchone()

        # Contar roles existentes SIN modificar
        count_result = db.execute("SELECT COUNT(*) as total FROM rol")
        roles_count = count_result.fetchone()

        return {
            "mensaje": "✅ Conexión exitosa a la base de datos EXISTENTE",
            "database": "Edwin",
            "test_query": test_value[0] if test_value else None,
            "roles_existentes": roles_count[0] if roles_count else 0,
            "status": "connected",
            "warning": "⚠️ Base de datos existente - NO se modificarán datos"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"❌ Error de conexión: {str(e)}"
        )
