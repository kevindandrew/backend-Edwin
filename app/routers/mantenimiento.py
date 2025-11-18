"""
Router para operaciones CRUD de Mantenimientos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.mantenimiento import Mantenimiento as MantenimientoModel
from app.models.equipo_biomedico import EquipoBiomedico as EquipoModel
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.mantenimiento import Mantenimiento, MantenimientoCreate, MantenimientoUpdate, MantenimientoDetallado
from app.auth import require_admin_or_tecnico, require_any_authenticated

router = APIRouter(
    prefix="/mantenimientos",
    tags=[" Módulo 5: Mantenimiento y Repuestos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Mantenimiento, status_code=status.HTTP_201_CREATED)
def crear_mantenimiento(
    mantenimiento: MantenimientoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Crear un nuevo registro de mantenimiento (Solo Administrador)
    """
    try:
        # Validar que el equipo existe
        db_equipo = db.query(EquipoModel).filter(
            EquipoModel.id_equipo == mantenimiento.id_equipo
        ).first()
        if not db_equipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo con ID {mantenimiento.id_equipo} no encontrado"
            )

        # Validar técnico si se proporciona
        if mantenimiento.id_tecnico:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == mantenimiento.id_tecnico).first():
                raise HTTPException(
                    status_code=404, detail=f"Técnico no encontrado")

        # Crear mantenimiento
        db_mantenimiento = MantenimientoModel(**mantenimiento.model_dump())
        db.add(db_mantenimiento)
        db.commit()
        db.refresh(db_mantenimiento)
        return db_mantenimiento
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear mantenimiento: {str(e)}"
        )


@router.get("/", response_model=List[Mantenimiento])
def obtener_mantenimientos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener lista de mantenimientos
    """
    try:
        mantenimientos = db.query(MantenimientoModel).offset(
            skip).limit(limit).all()
        return mantenimientos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mantenimientos: {str(e)}"
        )


@router.get("/{mantenimiento_id}", response_model=MantenimientoDetallado)
def obtener_mantenimiento(
    mantenimiento_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener un mantenimiento específico por ID con detalles (Solo Administrador)
    """
    try:
        db_mantenimiento = db.query(MantenimientoModel).filter(
            MantenimientoModel.id_mantenimiento == mantenimiento_id
        ).first()
        if db_mantenimiento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mantenimiento no encontrado"
            )
        return db_mantenimiento
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mantenimiento: {str(e)}"
        )


@router.put("/{mantenimiento_id}", response_model=Mantenimiento)
def actualizar_mantenimiento(
    mantenimiento_id: int,
    mantenimiento: MantenimientoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Actualizar un mantenimiento existente (Solo Administrador)
    """
    try:
        db_mantenimiento = db.query(MantenimientoModel).filter(
            MantenimientoModel.id_mantenimiento == mantenimiento_id
        ).first()
        if db_mantenimiento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mantenimiento no encontrado"
            )

        mantenimiento_data = mantenimiento.model_dump(exclude_unset=True)

        # Validar equipo si se está cambiando
        if 'id_equipo' in mantenimiento_data and mantenimiento_data['id_equipo']:
            if not db.query(EquipoModel).filter(EquipoModel.id_equipo == mantenimiento_data['id_equipo']).first():
                raise HTTPException(
                    status_code=404, detail=f"Equipo no encontrado")

        for key, value in mantenimiento_data.items():
            setattr(db_mantenimiento, key, value)

        db.commit()
        db.refresh(db_mantenimiento)
        return db_mantenimiento
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar mantenimiento: {str(e)}"
        )


@router.delete("/{mantenimiento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mantenimiento(
    mantenimiento_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Eliminar un mantenimiento (Administrador o Técnico de Mantenimiento)
    """
    try:
        db_mantenimiento = db.query(MantenimientoModel).filter(
            MantenimientoModel.id_mantenimiento == mantenimiento_id
        ).first()
        if db_mantenimiento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mantenimiento no encontrado"
            )

        db.delete(db_mantenimiento)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar mantenimiento: {str(e)}"
        )


@router.get("/equipo/{equipo_id}", response_model=List[Mantenimiento])
def obtener_mantenimientos_por_equipo(
    equipo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los mantenimientos de un equipo específico (Solo Administrador)
    """
    try:
        mantenimientos = db.query(MantenimientoModel).filter(
            MantenimientoModel.id_equipo == equipo_id
        ).all()
        return mantenimientos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mantenimientos: {str(e)}"
        )


@router.get("/tipo/{tipo}", response_model=List[Mantenimiento])
def obtener_mantenimientos_por_tipo(
    tipo: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los mantenimientos por tipo (preventivo, correctivo, calibración, etc.) (Solo Administrador)
    """
    try:
        mantenimientos = db.query(MantenimientoModel).filter(
            MantenimientoModel.tipo_mantenimiento == tipo
        ).all()
        return mantenimientos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mantenimientos: {str(e)}"
        )
