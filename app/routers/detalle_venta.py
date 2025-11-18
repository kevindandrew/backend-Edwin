"""
Router para operaciones CRUD de Detalles de Venta
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.detalle_venta import DetalleVenta as DetalleVentaModel
from app.models.venta import Venta as VentaModel
from app.models.equipo_biomedico import EquipoBiomedico as EquipoModel
from app.schemas.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate, DetalleVentaConRelaciones
from app.auth import require_admin_or_gestor, require_any_authenticated

router = APIRouter(
    prefix="/detalles-venta",
    tags=[" Módulo 7: Ventas"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=DetalleVenta, status_code=status.HTTP_201_CREATED)
def crear_detalle_venta(
    detalle: DetalleVentaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Crear un nuevo detalle de venta (ítem en la venta)
    """
    try:
        # Validar que la venta existe
        db_venta = db.query(VentaModel).filter(
            VentaModel.id_venta == detalle.id_venta
        ).first()
        if not db_venta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Venta con ID {detalle.id_venta} no encontrada"
            )

        # Validar que el equipo existe (OBLIGATORIO)
        db_equipo = db.query(EquipoModel).filter(
            EquipoModel.id_equipo == detalle.id_equipo
        ).first()
        if not db_equipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo con ID {detalle.id_equipo} no encontrado"
            )

        # Crear detalle
        db_detalle = DetalleVentaModel(**detalle.model_dump())
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
            detail=f"Error al crear detalle de venta: {str(e)}"
        )


@router.get("/", response_model=List[DetalleVentaConRelaciones])
def obtener_detalles_venta(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Obtener lista de detalles de venta con relaciones
    """
    try:
        detalles = db.query(DetalleVentaModel).offset(skip).limit(limit).all()
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles de venta: {str(e)}"
        )


@router.get("/venta/{venta_id}", response_model=List[DetalleVentaConRelaciones])
def obtener_detalles_por_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los detalles de una venta específica
    """
    try:
        detalles = db.query(DetalleVentaModel).filter(
            DetalleVentaModel.id_venta == venta_id
        ).all()
        return detalles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalles de venta: {str(e)}"
        )


@router.get("/{detalle_id}", response_model=DetalleVentaConRelaciones)
def obtener_detalle_venta(
    detalle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener un detalle de venta específico por ID
    """
    try:
        db_detalle = db.query(DetalleVentaModel).filter(
            DetalleVentaModel.id_detalle_venta == detalle_id
        ).first()
        if db_detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de venta no encontrado"
            )
        return db_detalle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalle de venta: {str(e)}"
        )


@router.put("/{detalle_id}", response_model=DetalleVenta)
def actualizar_detalle_venta(
    detalle_id: int,
    detalle: DetalleVentaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Actualizar un detalle de venta existente
    """
    try:
        db_detalle = db.query(DetalleVentaModel).filter(
            DetalleVentaModel.id_detalle_venta == detalle_id
        ).first()
        if db_detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de venta no encontrado"
            )

        detalle_data = detalle.model_dump(exclude_unset=True)

        # Validar equipo si se está cambiando (OBLIGATORIO)
        if 'id_equipo' in detalle_data:
            db_equipo = db.query(EquipoModel).filter(
                EquipoModel.id_equipo == detalle_data['id_equipo']
            ).first()
            if not db_equipo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Equipo con ID {detalle_data['id_equipo']} no encontrado"
                )

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
            detail=f"Error al actualizar detalle de venta: {str(e)}"
        )


@router.delete("/{detalle_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_detalle_venta(
    detalle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Eliminar un detalle de venta
    """
    try:
        db_detalle = db.query(DetalleVentaModel).filter(
            DetalleVentaModel.id_detalle_venta == detalle_id
        ).first()
        if db_detalle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle de venta no encontrado"
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
            detail=f"Error al eliminar detalle de venta: {str(e)}"
        )
