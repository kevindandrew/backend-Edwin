"""
Router para operaciones CRUD de Clientes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cliente import Cliente as ClienteModel
from app.schemas.cliente import Cliente, ClienteCreate, ClienteUpdate, ClienteConUbicaciones
from app.auth import require_admin_or_gestor, require_any_authenticated

router = APIRouter(
    prefix="/clientes",
    tags=[" Módulo 2: Clientes y Ubicaciones"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Crear un nuevo cliente (Administrador o Gestor Biomédico)
    """
    try:
        # Verificar si ya existe un cliente con ese NIT/RUC
        if cliente.nit_ruc:
            db_cliente = db.query(ClienteModel).filter(
                ClienteModel.nit_ruc == cliente.nit_ruc
            ).first()
            if db_cliente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un cliente con ese NIT/RUC"
                )

        # Crear cliente
        db_cliente = ClienteModel(**cliente.model_dump())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}"
        )


@router.get("/", response_model=List[Cliente])
def obtener_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener lista de clientes
    """
    try:
        clientes = db.query(ClienteModel).offset(skip).limit(limit).all()
        return clientes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}"
        )


@router.get("/{cliente_id}", response_model=ClienteConUbicaciones)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener un cliente específico por ID con sus ubicaciones
    """
    try:
        db_cliente = db.query(ClienteModel).filter(
            ClienteModel.id_cliente == cliente_id
        ).first()
        if db_cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        return db_cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}"
        )


@router.put("/{cliente_id}", response_model=Cliente)
def actualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Actualizar un cliente existente (Administrador o Gestor Biomédico)
    """
    try:
        db_cliente = db.query(ClienteModel).filter(
            ClienteModel.id_cliente == cliente_id
        ).first()
        if db_cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )

        # Verificar NIT/RUC único si se está cambiando
        cliente_data = cliente.model_dump(exclude_unset=True)
        if 'nit_ruc' in cliente_data and cliente_data['nit_ruc'] and cliente_data['nit_ruc'] != db_cliente.nit_ruc:
            existing = db.query(ClienteModel).filter(
                ClienteModel.nit_ruc == cliente_data['nit_ruc']
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un cliente con ese NIT/RUC"
                )

        for key, value in cliente_data.items():
            setattr(db_cliente, key, value)

        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}"
        )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_or_gestor)
):
    """
    Eliminar un cliente (Administrador o Gestor Biomédico)
    """
    try:
        db_cliente = db.query(ClienteModel).filter(
            ClienteModel.id_cliente == cliente_id
        ).first()
        if db_cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )

        db.delete(db_cliente)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}"
        )


@router.get("/buscar/nit/{nit_ruc}", response_model=Cliente)
def buscar_cliente_por_nit(
    nit_ruc: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Buscar un cliente por NIT/RUC
    """
    try:
        db_cliente = db.query(ClienteModel).filter(
            ClienteModel.nit_ruc == nit_ruc
        ).first()
        if db_cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        return db_cliente
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar cliente: {str(e)}"
        )
