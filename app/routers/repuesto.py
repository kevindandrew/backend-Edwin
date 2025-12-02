"""
Router para operaciones CRUD de Repuestos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.repuesto import Repuesto as RepuestoModel
from app.models.tipo_tecnologia import TipoTecnologia as TecnologiaModel
from app.schemas.repuesto import Repuesto, RepuestoCreate, RepuestoUpdate
from app.auth import require_admin_tecnico_or_compras, require_any_authenticated

router = APIRouter(
    prefix="/repuestos",
    tags=[" Módulo 5: Mantenimiento y Repuestos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Repuesto, status_code=status.HTTP_201_CREATED)
def crear_repuesto(
    repuesto: RepuestoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_tecnico_or_compras)
):
    """
    Crear un nuevo repuesto en el inventario (Solo Administrador)
    """
    try:
        # Validar tecnología si se proporciona
        if repuesto.id_tecnologia:
            if not db.query(TecnologiaModel).filter(TecnologiaModel.id_tecnologia == repuesto.id_tecnologia).first():
                raise HTTPException(
                    status_code=404, detail=f"Tipo de tecnología no encontrado")

        db_repuesto = RepuestoModel(**repuesto.model_dump())
        db.add(db_repuesto)
        db.commit()
        db.refresh(db_repuesto)
        return db_repuesto
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear repuesto: {str(e)}"
        )


@router.get("/", response_model=List[Repuesto])
def obtener_repuestos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_tecnico_or_compras)
):
    """
    Obtener lista de repuestos (Solo Administrador)
    """
    try:
        repuestos = db.query(RepuestoModel).offset(skip).limit(limit).all()
        return repuestos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener repuestos: {str(e)}"
        )


@router.get("/{repuesto_id}", response_model=Repuesto)
def obtener_repuesto(
    repuesto_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener un repuesto específico por ID (Solo Administrador)
    """
    try:
        db_repuesto = db.query(RepuestoModel).filter(
            RepuestoModel.id_repuesto == repuesto_id
        ).first()
        if db_repuesto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repuesto no encontrado"
            )
        return db_repuesto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener repuesto: {str(e)}"
        )


@router.put("/{repuesto_id}", response_model=Repuesto)
def actualizar_repuesto(
    repuesto_id: int,
    repuesto: RepuestoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_tecnico_or_compras)
):
    """
    Actualizar un repuesto existente (Solo Administrador)
    """
    try:
        db_repuesto = db.query(RepuestoModel).filter(
            RepuestoModel.id_repuesto == repuesto_id
        ).first()
        if db_repuesto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repuesto no encontrado"
            )

        repuesto_data = repuesto.model_dump(exclude_unset=True)
        for key, value in repuesto_data.items():
            setattr(db_repuesto, key, value)

        db.commit()
        db.refresh(db_repuesto)
        return db_repuesto
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar repuesto: {str(e)}"
        )


@router.delete("/{repuesto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_repuesto(
    repuesto_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_tecnico_or_compras)
):
    """
    Eliminar un repuesto del inventario (Solo Administrador)
    """
    try:
        db_repuesto = db.query(RepuestoModel).filter(
            RepuestoModel.id_repuesto == repuesto_id
        ).first()
        if db_repuesto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repuesto no encontrado"
            )

        db.delete(db_repuesto)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar repuesto: {str(e)}"
        )


@router.get("/stock/bajo", response_model=List[Repuesto])
def obtener_repuestos_stock_bajo(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_tecnico_or_compras)
):
    """
    Obtener repuestos con stock por debajo del stock mínimo (Solo Administrador)
    """
    try:
        # Repuestos donde stock <= stock_minimo
        repuestos = db.query(RepuestoModel).filter(
            RepuestoModel.stock <= RepuestoModel.stock_minimo
        ).all()
        return repuestos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener repuestos: {str(e)}"
        )
