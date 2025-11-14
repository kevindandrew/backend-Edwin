"""
Router para operaciones CRUD de Fabricantes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.fabricante import Fabricante as FabricanteModel
from app.schemas.fabricante import Fabricante, FabricanteCreate, FabricanteUpdate
from app.auth import require_admin

router = APIRouter(
    prefix="/fabricantes",
    tags=[" Módulo 3: Catálogos de Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Fabricante, status_code=status.HTTP_201_CREATED)
def crear_fabricante(
    fabricante: FabricanteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear un nuevo fabricante (Solo Administrador)
    """
    try:
        db_fabricante = FabricanteModel(**fabricante.model_dump())
        db.add(db_fabricante)
        db.commit()
        db.refresh(db_fabricante)
        return db_fabricante
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear fabricante: {str(e)}"
        )


@router.get("/", response_model=List[Fabricante])
def obtener_fabricantes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de fabricantes (Solo Administrador)
    """
    try:
        fabricantes = db.query(FabricanteModel).offset(skip).limit(limit).all()
        return fabricantes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener fabricantes: {str(e)}"
        )


@router.get("/{fabricante_id}", response_model=Fabricante)
def obtener_fabricante(
    fabricante_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener un fabricante específico por ID (Solo Administrador)
    """
    try:
        db_fabricante = db.query(FabricanteModel).filter(
            FabricanteModel.id_fabricante == fabricante_id
        ).first()
        if db_fabricante is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fabricante no encontrado"
            )
        return db_fabricante
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener fabricante: {str(e)}"
        )


@router.put("/{fabricante_id}", response_model=Fabricante)
def actualizar_fabricante(
    fabricante_id: int,
    fabricante: FabricanteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Actualizar un fabricante existente (Solo Administrador)
    """
    try:
        db_fabricante = db.query(FabricanteModel).filter(
            FabricanteModel.id_fabricante == fabricante_id
        ).first()
        if db_fabricante is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fabricante no encontrado"
            )

        fabricante_data = fabricante.model_dump(exclude_unset=True)
        for key, value in fabricante_data.items():
            setattr(db_fabricante, key, value)

        db.commit()
        db.refresh(db_fabricante)
        return db_fabricante
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar fabricante: {str(e)}"
        )


@router.delete("/{fabricante_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_fabricante(
    fabricante_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Eliminar un fabricante (Solo Administrador)
    """
    try:
        db_fabricante = db.query(FabricanteModel).filter(
            FabricanteModel.id_fabricante == fabricante_id
        ).first()
        if db_fabricante is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fabricante no encontrado"
            )

        db.delete(db_fabricante)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar fabricante: {str(e)}"
        )
