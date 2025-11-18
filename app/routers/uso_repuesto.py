"""
Router para operaciones CRUD de Uso de Repuestos
Gestiona la relación many-to-many entre Mantenimientos y Repuestos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.uso_repuesto import UsoRepuesto as UsoRepuestoModel
from app.models.mantenimiento import Mantenimiento as MantenimientoModel
from app.models.repuesto import Repuesto as RepuestoModel
from app.schemas.uso_repuesto import UsoRepuesto, UsoRepuestoCreate, UsoRepuestoUpdate, UsoRepuestoConDetalles
from app.auth import require_admin_or_tecnico, require_any_authenticated

router = APIRouter(
    prefix="/uso-repuestos",
    tags=[" Módulo 5: Mantenimiento y Repuestos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=UsoRepuesto, status_code=status.HTTP_201_CREATED)
def registrar_uso_repuesto(
    uso: UsoRepuestoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Registrar el uso de un repuesto en un mantenimiento
    """
    try:
        # Validar que el mantenimiento existe
        db_mantenimiento = db.query(MantenimientoModel).filter(
            MantenimientoModel.id_mantenimiento == uso.id_mantenimiento
        ).first()
        if not db_mantenimiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mantenimiento con ID {uso.id_mantenimiento} no encontrado"
            )

        # Validar que el repuesto existe
        db_repuesto = db.query(RepuestoModel).filter(
            RepuestoModel.id_repuesto == uso.id_repuesto
        ).first()
        if not db_repuesto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repuesto con ID {uso.id_repuesto} no encontrado"
            )

        # Verificar que no exista ya este registro
        db_uso_existente = db.query(UsoRepuestoModel).filter(
            UsoRepuestoModel.id_mantenimiento == uso.id_mantenimiento,
            UsoRepuestoModel.id_repuesto == uso.id_repuesto
        ).first()
        if db_uso_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este repuesto ya está registrado en este mantenimiento"
            )

        # Verificar stock disponible
        if db_repuesto.stock < uso.cantidad_usada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente. Disponible: {db_repuesto.stock}, Requerido: {uso.cantidad_usada}"
            )

        # Crear registro de uso
        db_uso = UsoRepuestoModel(**uso.model_dump())
        db.add(db_uso)

        # Actualizar stock del repuesto
        db_repuesto.stock -= uso.cantidad_usada

        db.commit()
        db.refresh(db_uso)
        return db_uso
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar uso de repuesto: {str(e)}"
        )


@router.get("/", response_model=List[UsoRepuestoConDetalles])
def obtener_uso_repuestos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Obtener lista de uso de repuestos con detalles
    """
    try:
        usos = db.query(UsoRepuestoModel).offset(skip).limit(limit).all()
        return usos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener uso de repuestos: {str(e)}"
        )


@router.get("/mantenimiento/{mantenimiento_id}", response_model=List[UsoRepuestoConDetalles])
def obtener_repuestos_por_mantenimiento(
    mantenimiento_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los repuestos usados en un mantenimiento específico
    """
    try:
        usos = db.query(UsoRepuestoModel).filter(
            UsoRepuestoModel.id_mantenimiento == mantenimiento_id
        ).all()
        return usos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener repuestos: {str(e)}"
        )


@router.get("/repuesto/{repuesto_id}", response_model=List[UsoRepuestoConDetalles])
def obtener_mantenimientos_por_repuesto(
    repuesto_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los mantenimientos donde se usó un repuesto específico
    """
    try:
        usos = db.query(UsoRepuestoModel).filter(
            UsoRepuestoModel.id_repuesto == repuesto_id
        ).all()
        return usos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener mantenimientos: {str(e)}"
        )


@router.get("/{mantenimiento_id}/{repuesto_id}", response_model=UsoRepuestoConDetalles)
def obtener_uso_repuesto_especifico(
    mantenimiento_id: int,
    repuesto_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Obtener el registro de uso específico de un repuesto en un mantenimiento
    """
    try:
        db_uso = db.query(UsoRepuestoModel).filter(
            UsoRepuestoModel.id_mantenimiento == mantenimiento_id,
            UsoRepuestoModel.id_repuesto == repuesto_id
        ).first()
        if db_uso is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de uso de repuesto no encontrado"
            )
        return db_uso
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener uso de repuesto: {str(e)}"
        )


@router.put("/{mantenimiento_id}/{repuesto_id}", response_model=UsoRepuesto)
def actualizar_uso_repuesto(
    mantenimiento_id: int,
    repuesto_id: int,
    uso: UsoRepuestoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Actualizar un registro de uso de repuesto
    """
    try:
        db_uso = db.query(UsoRepuestoModel).filter(
            UsoRepuestoModel.id_mantenimiento == mantenimiento_id,
            UsoRepuestoModel.id_repuesto == repuesto_id
        ).first()
        if db_uso is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de uso de repuesto no encontrado"
            )

        uso_data = uso.model_dump(exclude_unset=True)

        # Si se está actualizando la cantidad, ajustar el stock
        if 'cantidad_usada' in uso_data:
            db_repuesto = db.query(RepuestoModel).filter(
                RepuestoModel.id_repuesto == repuesto_id
            ).first()

            diferencia = uso_data['cantidad_usada'] - db_uso.cantidad_usada

            if diferencia > 0 and db_repuesto.stock < diferencia:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para el incremento solicitado"
                )

            db_repuesto.stock -= diferencia

        for key, value in uso_data.items():
            setattr(db_uso, key, value)

        db.commit()
        db.refresh(db_uso)
        return db_uso
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar uso de repuesto: {str(e)}"
        )


@router.delete("/{mantenimiento_id}/{repuesto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_uso_repuesto(
    mantenimiento_id: int,
    repuesto_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_tecnico)
):
    """
    Eliminar un registro de uso de repuesto (devuelve el stock al inventario)
    """
    try:
        db_uso = db.query(UsoRepuestoModel).filter(
            UsoRepuestoModel.id_mantenimiento == mantenimiento_id,
            UsoRepuestoModel.id_repuesto == repuesto_id
        ).first()
        if db_uso is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de uso de repuesto no encontrado"
            )

        # Devolver el stock al repuesto
        db_repuesto = db.query(RepuestoModel).filter(
            RepuestoModel.id_repuesto == repuesto_id
        ).first()
        if db_repuesto:
            db_repuesto.stock += db_uso.cantidad_usada

        db.delete(db_uso)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar uso de repuesto: {str(e)}"
        )
