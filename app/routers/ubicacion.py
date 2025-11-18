"""
Router para operaciones CRUD de Ubicaciones
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ubicacion import Ubicacion as UbicacionModel
from app.models.cliente import Cliente as ClienteModel
from app.schemas.ubicacion import Ubicacion, UbicacionCreate, UbicacionUpdate, UbicacionConCliente
from app.auth import require_admin_or_gestor, require_any_authenticated

router = APIRouter(
    prefix="/ubicaciones",
    tags=[" Módulo 2: Clientes y Ubicaciones"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Ubicacion, status_code=status.HTTP_201_CREATED)
def crear_ubicacion(
    ubicacion: UbicacionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Crear una nueva ubicación (Administrador o Gestor Biomédico)
    """
    try:
        # Verificar que el cliente existe si se proporciona id_cliente
        if ubicacion.id_cliente:
            db_cliente = db.query(ClienteModel).filter(
                ClienteModel.id_cliente == ubicacion.id_cliente
            ).first()
            if not db_cliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cliente con ID {ubicacion.id_cliente} no encontrado"
                )

        # Crear ubicación
        db_ubicacion = UbicacionModel(**ubicacion.model_dump())
        db.add(db_ubicacion)
        db.commit()
        db.refresh(db_ubicacion)
        return db_ubicacion
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear ubicación: {str(e)}"
        )


@router.get("/", response_model=List[UbicacionConCliente])
def obtener_ubicaciones(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener lista de ubicaciones con información del cliente
    """
    try:
        ubicaciones = db.query(UbicacionModel).offset(skip).limit(limit).all()
        return ubicaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicaciones: {str(e)}"
        )


@router.get("/{ubicacion_id}", response_model=UbicacionConCliente)
def obtener_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener una ubicación específica por ID con información del cliente
    """
    try:
        db_ubicacion = db.query(UbicacionModel).filter(
            UbicacionModel.id_ubicacion == ubicacion_id
        ).first()
        if db_ubicacion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ubicación no encontrada"
            )
        return db_ubicacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicación: {str(e)}"
        )


@router.put("/{ubicacion_id}", response_model=Ubicacion)
def actualizar_ubicacion(
    ubicacion_id: int,
    ubicacion: UbicacionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Actualizar una ubicación existente (Administrador o Gestor Biomédico)
    """
    try:
        db_ubicacion = db.query(UbicacionModel).filter(
            UbicacionModel.id_ubicacion == ubicacion_id
        ).first()
        if db_ubicacion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ubicación no encontrada"
            )

        # Verificar que el cliente existe si se está cambiando
        ubicacion_data = ubicacion.model_dump(exclude_unset=True)
        if 'id_cliente' in ubicacion_data and ubicacion_data['id_cliente']:
            db_cliente = db.query(ClienteModel).filter(
                ClienteModel.id_cliente == ubicacion_data['id_cliente']
            ).first()
            if not db_cliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cliente con ID {ubicacion_data['id_cliente']} no encontrado"
                )

        for key, value in ubicacion_data.items():
            setattr(db_ubicacion, key, value)

        db.commit()
        db.refresh(db_ubicacion)
        return db_ubicacion
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar ubicación: {str(e)}"
        )


@router.delete("/{ubicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Eliminar una ubicación (Administrador o Gestor Biomédico)
    """
    try:
        db_ubicacion = db.query(UbicacionModel).filter(
            UbicacionModel.id_ubicacion == ubicacion_id
        ).first()
        if db_ubicacion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ubicación no encontrada"
            )

        db.delete(db_ubicacion)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar ubicación: {str(e)}"
        )


@router.get("/cliente/{cliente_id}", response_model=List[Ubicacion])
def obtener_ubicaciones_por_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todas las ubicaciones de un cliente específico
    """
    try:
        # Verificar que el cliente existe
        db_cliente = db.query(ClienteModel).filter(
            ClienteModel.id_cliente == cliente_id
        ).first()
        if not db_cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        ubicaciones = db.query(UbicacionModel).filter(
            UbicacionModel.id_cliente == cliente_id
        ).all()
        return ubicaciones
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicaciones: {str(e)}"
        )


@router.get("/almacen/sin-cliente", response_model=List[Ubicacion])
def obtener_ubicaciones_almacen(
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todas las ubicaciones que no tienen cliente asignado (almacén)
    """
    try:
        ubicaciones = db.query(UbicacionModel).filter(
            UbicacionModel.id_cliente.is_(None)
        ).all()
        return ubicaciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ubicaciones de almacén: {str(e)}"
        )
