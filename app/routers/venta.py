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
from app.auth import require_admin

router = APIRouter(
    prefix="/ventas",
    tags=[" Módulo 7: Ventas"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Venta, status_code=status.HTTP_201_CREATED)
def crear_venta(
    venta: VentaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear un nuevo registro de venta
    """
    try:
        # Validar número de factura único si se proporciona
        if venta.numero_factura:
            db_venta_existente = db.query(VentaModel).filter(
                VentaModel.numero_factura == venta.numero_factura
            ).first()
            if db_venta_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una venta con ese número de factura"
                )

        # Validar cliente si se proporciona
        if venta.id_cliente:
            if not db.query(ClienteModel).filter(ClienteModel.id_cliente == venta.id_cliente).first():
                raise HTTPException(
                    status_code=404, detail="Cliente no encontrado")

        # Validar usuario si se proporciona
        if venta.id_usuario_registro:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == venta.id_usuario_registro).first():
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")

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
    current_user=Depends(require_admin)
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


@router.get("/buscar/factura/{numero_factura}", response_model=VentaDetallada)
def buscar_venta_por_factura(
    numero_factura: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Buscar una venta por número de factura
    """
    try:
        db_venta = db.query(VentaModel).filter(
            VentaModel.numero_factura == numero_factura
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
            detail=f"Error al buscar venta: {str(e)}"
        )


@router.get("/filtrar/cliente/{cliente_id}", response_model=List[Venta])
def obtener_ventas_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las ventas de un cliente específico
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
def obtener_ventas_por_estado(estado: str, db: Session = Depends(get_db)):
    """
    Obtener todas las ventas por estado (pendiente, completada, cancelada, etc.)
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
    current_user=Depends(require_admin)
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
    current_user=Depends(require_admin)
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

        # Validar número de factura único si se está cambiando
        if 'numero_factura' in venta_data and venta_data['numero_factura']:
            if venta_data['numero_factura'] != db_venta.numero_factura:
                existing = db.query(VentaModel).filter(
                    VentaModel.numero_factura == venta_data['numero_factura']
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe una venta con ese número de factura"
                    )

        # Validar cliente si se está cambiando
        if 'id_cliente' in venta_data and venta_data['id_cliente']:
            if not db.query(ClienteModel).filter(ClienteModel.id_cliente == venta_data['id_cliente']).first():
                raise HTTPException(
                    status_code=404, detail="Cliente no encontrado")

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
    current_user=Depends(require_admin)
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
