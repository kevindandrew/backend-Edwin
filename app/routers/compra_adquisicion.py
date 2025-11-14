"""
Router para operaciones CRUD de Compras y Adquisiciones
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.compra_adquisicion import CompraAdquisicion as CompraModel
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.compra_adquisicion import CompraAdquisicion, CompraAdquisicionCreate, CompraAdquisicionUpdate, CompraAdquisicionDetallada
from app.auth import require_admin

router = APIRouter(
    prefix="/compras",
    tags=[" Módulo 6: Compras y Adquisiciones"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=CompraAdquisicion, status_code=status.HTTP_201_CREATED)
def crear_compra(
    compra: CompraAdquisicionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear un nuevo registro de compra/adquisición
    """
    try:
        # Validar número de factura único si se proporciona
        if compra.numero_factura:
            db_compra_existente = db.query(CompraModel).filter(
                CompraModel.numero_factura == compra.numero_factura
            ).first()
            if db_compra_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una compra con ese número de factura"
                )

        # Validar usuario si se proporciona
        if compra.id_usuario_registro:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == compra.id_usuario_registro).first():
                raise HTTPException(
                    status_code=404, detail="Usuario no encontrado")

        # Crear compra
        db_compra = CompraModel(**compra.model_dump())
        db.add(db_compra)
        db.commit()
        db.refresh(db_compra)
        return db_compra
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear compra: {str(e)}"
        )


@router.get("/", response_model=List[CompraAdquisicion])
def obtener_compras(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de compras/adquisiciones
    """
    try:
        compras = db.query(CompraModel).offset(skip).limit(limit).all()
        return compras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compras: {str(e)}"
        )


@router.get("/{compra_id}", response_model=CompraAdquisicionDetallada)
def obtener_compra(
    compra_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener una compra específica por ID con todos sus detalles
    """
    try:
        db_compra = db.query(CompraModel).filter(
            CompraModel.id_compra == compra_id
        ).first()
        if db_compra is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada"
            )
        return db_compra
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compra: {str(e)}"
        )


@router.put("/{compra_id}", response_model=CompraAdquisicion)
def actualizar_compra(
    compra_id: int,
    compra: CompraAdquisicionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Actualizar una compra/adquisición existente
    """
    try:
        db_compra = db.query(CompraModel).filter(
            CompraModel.id_compra == compra_id
        ).first()
        if db_compra is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada"
            )

        compra_data = compra.model_dump(exclude_unset=True)

        # Validar número de factura único si se está cambiando
        if 'numero_factura' in compra_data and compra_data['numero_factura']:
            if compra_data['numero_factura'] != db_compra.numero_factura:
                existing = db.query(CompraModel).filter(
                    CompraModel.numero_factura == compra_data['numero_factura']
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe una compra con ese número de factura"
                    )

        for key, value in compra_data.items():
            setattr(db_compra, key, value)

        db.commit()
        db.refresh(db_compra)
        return db_compra
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar compra: {str(e)}"
        )


@router.delete("/{compra_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_compra(
    compra_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Eliminar una compra (también eliminará sus detalles en cascada)
    """
    try:
        db_compra = db.query(CompraModel).filter(
            CompraModel.id_compra == compra_id
        ).first()
        if db_compra is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada"
            )

        db.delete(db_compra)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar compra: {str(e)}"
        )


@router.get("/buscar/factura/{numero_factura}", response_model=CompraAdquisicionDetallada)
def buscar_compra_por_factura(
    numero_factura: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Buscar una compra por número de factura
    """
    try:
        db_compra = db.query(CompraModel).filter(
            CompraModel.numero_factura == numero_factura
        ).first()
        if db_compra is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compra no encontrada"
            )
        return db_compra
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar compra: {str(e)}"
        )


@router.get("/proveedor/{proveedor}", response_model=List[CompraAdquisicion])
def obtener_compras_por_proveedor(
    proveedor: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener todas las compras de un proveedor específico
    """
    try:
        compras = db.query(CompraModel).filter(
            CompraModel.proveedor == proveedor
        ).all()
        return compras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compras: {str(e)}"
        )
