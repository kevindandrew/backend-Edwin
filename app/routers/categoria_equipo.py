"""
Router para operaciones CRUD de Categorías de Equipo
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.categoria_equipo import CategoriaEquipo as CategoriaEquipoModel
from app.schemas.categoria_equipo import CategoriaEquipo, CategoriaEquipoCreate, CategoriaEquipoUpdate
from app.auth import require_admin_or_gestor, require_any_authenticated

router = APIRouter(
    prefix="/categorias-equipo",
    tags=["Módulo 3: Catálogos de Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=CategoriaEquipo, status_code=status.HTTP_201_CREATED)
def crear_categoria_equipo(
    categoria: CategoriaEquipoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Crear una nueva categoría de equipo (Administrador o Gestor Biomédico)
    """
    try:
        db_categoria = CategoriaEquipoModel(**categoria.model_dump())
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        return db_categoria
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}"
        )


@router.get("/", response_model=List[CategoriaEquipo])
def obtener_categorias_equipo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener lista de categorías de equipo
    """
    try:
        categorias = db.query(CategoriaEquipoModel).offset(
            skip).limit(limit).all()
        return categorias
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}"
        )


@router.get("/{categoria_id}", response_model=CategoriaEquipo)
def obtener_categoria_equipo(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener una categoría de equipo específica por ID
    """
    try:
        db_categoria = db.query(CategoriaEquipoModel).filter(
            CategoriaEquipoModel.id_categoria == categoria_id
        ).first()
        if db_categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        return db_categoria
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}"
        )


@router.put("/{categoria_id}", response_model=CategoriaEquipo)
def actualizar_categoria_equipo(
    categoria_id: int,
    categoria: CategoriaEquipoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Actualizar una categoría de equipo existente (Administrador o Gestor Biomédico)
    """
    try:
        db_categoria = db.query(CategoriaEquipoModel).filter(
            CategoriaEquipoModel.id_categoria == categoria_id
        ).first()
        if db_categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )

        categoria_data = categoria.model_dump(exclude_unset=True)
        for key, value in categoria_data.items():
            setattr(db_categoria, key, value)

        db.commit()
        db.refresh(db_categoria)
        return db_categoria
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar categoría: {str(e)}"
        )


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria_equipo(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Eliminar una categoría de equipo (Administrador o Gestor Biomédico)
    """
    try:
        db_categoria = db.query(CategoriaEquipoModel).filter(
            CategoriaEquipoModel.id_categoria == categoria_id
        ).first()
        if db_categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )

        db.delete(db_categoria)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}"
        )
