"""
Router para operaciones CRUD de Ventas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.venta import Venta as VentaModel
from app.models.cliente import Cliente as ClienteModel
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.venta import Venta, VentaCreate, VentaUpdate, VentaDetallada
from app.auth import require_admin_or_gestor, require_any_authenticated

router = APIRouter(
    prefix="/ventas",
    tags=[" Módulo 7: Ventas"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Venta, status_code=status.HTTP_201_CREATED)
def crear_venta(
    venta: VentaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Crear un nuevo registro de venta (Solo Administrador)
    """
    try:
        # Validar cliente (requerido)
        if not db.query(ClienteModel).filter(ClienteModel.id_cliente == venta.id_cliente).first():
            raise HTTPException(
                status_code=404, detail="Cliente no encontrado")

        # Validar usuario vendedor si se proporciona
        if venta.id_usuario_vendedor:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == venta.id_usuario_vendedor).first():
                raise HTTPException(
                    status_code=404, detail="Usuario vendedor no encontrado")

        # Crear venta
        db_venta = VentaModel(**venta.model_dump())
        db.add(db_venta)
        db.commit()
        db.refresh(db_venta)
        return db_venta
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear venta: {str(e)}"
        )


@router.get("/", response_model=List[Venta])
def obtener_ventas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Obtener lista de ventas
    """
    try:
        ventas = db.query(VentaModel).offset(skip).limit(limit).all()
        return ventas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ventas: {str(e)}"
        )


@router.get("/filtrar/cliente/{cliente_id}", response_model=List[Venta])
def obtener_ventas_por_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todas las ventas de un cliente específico (Solo Administrador)
    """
    try:
        ventas = db.query(VentaModel).filter(
            VentaModel.id_cliente == cliente_id
        ).all()
        return ventas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ventas: {str(e)}"
        )


@router.get("/filtrar/estado/{estado}", response_model=List[Venta])
def obtener_ventas_por_estado(
    estado: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todas las ventas por estado (pendiente, completada, cancelada, etc.) (Solo Administrador)
    """
    try:
        ventas = db.query(VentaModel).filter(
            VentaModel.estado_venta == estado
        ).all()
        return ventas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ventas: {str(e)}"
        )


@router.get("/{venta_id}", response_model=VentaDetallada)
def obtener_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener una venta específica por ID con todos sus detalles
    """
    try:
        db_venta = db.query(VentaModel).filter(
            VentaModel.id_venta == venta_id
        ).first()
        if db_venta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )
        return db_venta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener venta: {str(e)}"
        )


@router.put("/{venta_id}", response_model=Venta)
def actualizar_venta(
    venta_id: int,
    venta: VentaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Actualizar una venta existente
    """
    try:
        db_venta = db.query(VentaModel).filter(
            VentaModel.id_venta == venta_id
        ).first()
        if db_venta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )

        venta_data = venta.model_dump(exclude_unset=True)

        # Validar cliente si se está cambiando
        if 'id_cliente' in venta_data and venta_data['id_cliente']:
            if not db.query(ClienteModel).filter(ClienteModel.id_cliente == venta_data['id_cliente']).first():
                raise HTTPException(
                    status_code=404, detail="Cliente no encontrado")

        # Validar vendedor si se está cambiando
        if 'id_usuario_vendedor' in venta_data and venta_data['id_usuario_vendedor']:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == venta_data['id_usuario_vendedor']).first():
                raise HTTPException(
                    status_code=404, detail="Usuario vendedor no encontrado")

        for key, value in venta_data.items():
            setattr(db_venta, key, value)

        db.commit()
        db.refresh(db_venta)
        return db_venta
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar venta: {str(e)}"
        )


@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Eliminar una venta (también eliminará sus detalles en cascada)
    """
    try:
        db_venta = db.query(VentaModel).filter(
            VentaModel.id_venta == venta_id
        ).first()
        if db_venta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )

        db.delete(db_venta)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar venta: {str(e)}"
        )
