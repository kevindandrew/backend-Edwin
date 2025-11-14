"""
Router para operaciones CRUD de Tipos de Tecnología
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tipo_tecnologia import TipoTecnologia as TipoTecnologiaModel
from app.schemas.tipo_tecnologia import TipoTecnologia, TipoTecnologiaCreate, TipoTecnologiaUpdate
from app.auth import require_admin

router = APIRouter(
    prefix="/tipos-tecnologia",
    tags=[" Módulo 3: Catálogos de Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=TipoTecnologia, status_code=status.HTTP_201_CREATED)
def crear_tipo_tecnologia(
    tipo: TipoTecnologiaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear un nuevo tipo de tecnología (Solo Administrador)
    """
    try:
        db_tipo = TipoTecnologiaModel(**tipo.model_dump())
        db.add(db_tipo)
        db.commit()
        db.refresh(db_tipo)
        return db_tipo
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear tipo de tecnología: {str(e)}"
        )


@router.get("/", response_model=List[TipoTecnologia])
def obtener_tipos_tecnologia(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de tipos de tecnología (Solo Administrador)
    """
    try:
        tipos = db.query(TipoTecnologiaModel).offset(skip).limit(limit).all()
        return tipos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipos de tecnología: {str(e)}"
        )


@router.get("/{tipo_id}", response_model=TipoTecnologia)
def obtener_tipo_tecnologia(
    tipo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener un tipo de tecnología específico por ID (Solo Administrador)
    """
    try:
        db_tipo = db.query(TipoTecnologiaModel).filter(
            TipoTecnologiaModel.id_tecnologia == tipo_id
        ).first()
        if db_tipo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de tecnología no encontrado"
            )
        return db_tipo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener tipo de tecnología: {str(e)}"
        )


@router.put("/{tipo_id}", response_model=TipoTecnologia)
def actualizar_tipo_tecnologia(
    tipo_id: int,
    tipo: TipoTecnologiaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Actualizar un tipo de tecnología existente (Solo Administrador)
    """
    try:
        db_tipo = db.query(TipoTecnologiaModel).filter(
            TipoTecnologiaModel.id_tecnologia == tipo_id
        ).first()
        if db_tipo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de tecnología no encontrado"
            )

        tipo_data = tipo.model_dump(exclude_unset=True)
        for key, value in tipo_data.items():
            setattr(db_tipo, key, value)

        db.commit()
        db.refresh(db_tipo)
        return db_tipo
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar tipo de tecnología: {str(e)}"
        )


@router.delete("/{tipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_tecnologia(
    tipo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Eliminar un tipo de tecnología (Solo Administrador)
    """
    try:
        db_tipo = db.query(TipoTecnologiaModel).filter(
            TipoTecnologiaModel.id_tecnologia == tipo_id
        ).first()
        if db_tipo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de tecnología no encontrado"
            )

        db.delete(db_tipo)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar tipo de tecnología: {str(e)}"
        )
