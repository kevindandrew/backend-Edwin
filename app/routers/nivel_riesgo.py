"""
Router para operaciones CRUD de Niveles de Riesgo
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.nivel_riesgo import NivelRiesgo as NivelRiesgoModel
from app.schemas.nivel_riesgo import NivelRiesgo, NivelRiesgoCreate, NivelRiesgoUpdate
from app.auth import require_admin

router = APIRouter(
    prefix="/niveles-riesgo",
    tags=[" Módulo 3: Catálogos de Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=NivelRiesgo, status_code=status.HTTP_201_CREATED)
def crear_nivel_riesgo(
    nivel: NivelRiesgoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear un nuevo nivel de riesgo (Solo Administrador)
    """
    try:
        db_nivel = NivelRiesgoModel(**nivel.model_dump())
        db.add(db_nivel)
        db.commit()
        db.refresh(db_nivel)
        return db_nivel
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear nivel de riesgo: {str(e)}"
        )


@router.get("/", response_model=List[NivelRiesgo])
def obtener_niveles_riesgo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de niveles de riesgo (Solo Administrador)
    """
    try:
        niveles = db.query(NivelRiesgoModel).offset(skip).limit(limit).all()
        return niveles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener niveles de riesgo: {str(e)}"
        )


@router.get("/{nivel_id}", response_model=NivelRiesgo)
def obtener_nivel_riesgo(
    nivel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener un nivel de riesgo específico por ID (Solo Administrador)
    """
    try:
        db_nivel = db.query(NivelRiesgoModel).filter(
            NivelRiesgoModel.id_riesgo == nivel_id
        ).first()
        if db_nivel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nivel de riesgo no encontrado"
            )
        return db_nivel
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener nivel de riesgo: {str(e)}"
        )


@router.put("/{nivel_id}", response_model=NivelRiesgo)
def actualizar_nivel_riesgo(
    nivel_id: int,
    nivel: NivelRiesgoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Actualizar un nivel de riesgo existente (Solo Administrador)
    """
    try:
        db_nivel = db.query(NivelRiesgoModel).filter(
            NivelRiesgoModel.id_riesgo == nivel_id
        ).first()
        if db_nivel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nivel de riesgo no encontrado"
            )

        nivel_data = nivel.model_dump(exclude_unset=True)
        for key, value in nivel_data.items():
            setattr(db_nivel, key, value)

        db.commit()
        db.refresh(db_nivel)
        return db_nivel
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar nivel de riesgo: {str(e)}"
        )


@router.delete("/{nivel_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_nivel_riesgo(
    nivel_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Eliminar un nivel de riesgo (Solo Administrador)
    """
    try:
        db_nivel = db.query(NivelRiesgoModel).filter(
            NivelRiesgoModel.id_riesgo == nivel_id
        ).first()
        if db_nivel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nivel de riesgo no encontrado"
            )

        db.delete(db_nivel)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar nivel de riesgo: {str(e)}"
        )
