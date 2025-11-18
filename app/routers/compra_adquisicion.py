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
from app.auth import require_admin_or_compras, require_any_authenticated

router = APIRouter(
    prefix="/compras",
    tags=[" Módulo 6: Compras y Adquisiciones"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=CompraAdquisicion, status_code=status.HTTP_201_CREATED)
def crear_compra(
    compra: CompraAdquisicionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_compras)
):
    """
    Crear un nuevo registro de compra/adquisición (Solo Administrador)
    """
    try:
        # Validar usuario administrador si se proporciona
        if compra.id_usuario_admin:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == compra.id_usuario_admin).first():
                raise HTTPException(
                    status_code=404, detail="Usuario administrador no encontrado")

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
    current_user=Depends(require_admin_or_compras)
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
    current_user=Depends(require_any_authenticated)
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
    current_user=Depends(require_admin_or_compras)
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

        # Validar usuario administrador si se está cambiando
        if 'id_usuario_admin' in compra_data and compra_data['id_usuario_admin']:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == compra_data['id_usuario_admin']).first():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario administrador no encontrado"
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
    current_user=Depends(require_admin_or_compras)
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


@router.get("/estado/{estado}", response_model=List[CompraAdquisicion])
def obtener_compras_por_estado(
    estado: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todas las compras por estado (Pendiente, Aprobada, Rechazada, etc.)
    """
    try:
        compras = db.query(CompraModel).filter(
            CompraModel.estado_compra == estado
        ).all()
        return compras
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener compras: {str(e)}"
        )
