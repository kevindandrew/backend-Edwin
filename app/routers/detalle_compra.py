"""
Router para operaciones CRUD de Detalles de Compra
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.detalle_compra import DetalleCompra as DetalleCompraModel
from app.models.compra_adquisicion import CompraAdquisicion as CompraModel
from app.models.equipo_biomedico import EquipoBiomedico as EquipoModel
from app.models.repuesto import Repuesto as RepuestoModel
from app.schemas.detalle_compra import DetalleCompra, DetalleCompraCreate, DetalleCompraUpdate, DetalleCompraConRelaciones
from app.auth import require_admin_or_compras, require_any_authenticated

router = APIRouter(
    prefix="/detalles-compra",
    tags=[" Módulo 6: Compras y Adquisiciones"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=DetalleCompra, status_code=status.HTTP_201_CREATED)
def crear_detalle_compra(
    detalle: DetalleCompraCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_compras)
):
    """
    Crear un nuevo detalle de compra - ítem en la compra (Solo Administrador)
    """
    try:
        # Validar que la compra existe
        db_compra = db.query(CompraModel).filter(
            CompraModel.id_compra == detalle.id_compra
        ).first()
        if not db_compra:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra con ID {detalle.id_compra} no encontrada"
            )

        # Validar que al menos uno (repuesto o equipo) esté presente
        if not detalle.id_repuesto and not detalle.id_equipo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debe especificar un repuesto o un equipo"
            )

        # Validar que el repuesto existe si se proporciona
        if detalle.id_repuesto:
            db_repuesto = db.query(RepuestoModel).filter(
                RepuestoModel.id_repuesto == detalle.id_repuesto
            ).first()
            if not db_repuesto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Repuesto con ID {detalle.id_repuesto} no encontrado"
                )

        # Validar que el equipo existe si se proporciona
        if detalle.id_equipo:
            db_equipo = db.query(EquipoModel).filter(
                EquipoModel.id_equipo == detalle.id_equipo
            ).first()
            if not db_equipo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipo con ID {detalle.id_equipo} no encontrado"
                )

        # Crear detalle
        db_detalle = DetalleCompraModel(**detalle.model_dump())
        db.add(db_detalle)
        db.commit()
        db.refresh(db_detalle)
        return db_detalle
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear detalle de compra: {str(e)}"
        )


@router.get("/", response_model=List[DetalleCompraConRelaciones])
def obtener_detalles_compra(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_compras)
):
    """
    Obtener lista de detalles de compra con relaciones
    """
    try:
        detalles = db.query(DetalleCompraModel).offset(skip).limit(limit).all()
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles de compra: {str(e)}"
        )


@router.get("/{detalle_id}", response_model=DetalleCompraConRelaciones)
def obtener_detalle_compra(
    detalle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener un detalle de compra específico por ID
    """
    try:
        db_detalle = db.query(DetalleCompraModel).filter(
            DetalleCompraModel.id_detalle == detalle_id
        ).first()
        if db_detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de compra no encontrado"
            )
        return db_detalle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalle de compra: {str(e)}"
        )


@router.get("/compra/{compra_id}", response_model=List[DetalleCompraConRelaciones])
def obtener_detalles_por_compra(
    compra_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los detalles de una compra específica (Solo Administrador)
    """
    try:
        detalles = db.query(DetalleCompraModel).filter(
            DetalleCompraModel.id_compra == compra_id
        ).all()
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles de compra: {str(e)}"
        )


@router.put("/{detalle_id}", response_model=DetalleCompra)
def actualizar_detalle_compra(
    detalle_id: int,
    detalle: DetalleCompraUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_compras)
):
    """
    Actualizar un detalle de compra existente (Solo Administrador)
    """
    try:
        db_detalle = db.query(DetalleCompraModel).filter(
            DetalleCompraModel.id_detalle == detalle_id
        ).first()
        if db_detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de compra no encontrado"
            )

        detalle_data = detalle.model_dump(exclude_unset=True)

        # Validar equipo si se está cambiando
        if 'id_equipo' in detalle_data and detalle_data['id_equipo']:
            if not db.query(EquipoModel).filter(EquipoModel.id_equipo == detalle_data['id_equipo']).first():
                raise HTTPException(
                    status_code=404, detail="Equipo no encontrado")

        for key, value in detalle_data.items():
            setattr(db_detalle, key, value)

        db.commit()
        db.refresh(db_detalle)
        return db_detalle
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar detalle de compra: {str(e)}"
        )


@router.delete("/{detalle_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_detalle_compra(
    detalle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_compras)
):
    """
    Eliminar un detalle de compra (Solo Administrador)
    """
    try:
        db_detalle = db.query(DetalleCompraModel).filter(
            DetalleCompraModel.id_detalle == detalle_id
        ).first()
        if db_detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de compra no encontrado"
            )

        db.delete(db_detalle)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar detalle de compra: {str(e)}"
        )
