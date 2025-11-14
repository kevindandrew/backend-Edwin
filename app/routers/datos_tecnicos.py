"""
Router para operaciones CRUD de Datos Técnicos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.datos_tecnicos import DatosTecnicos as DatosTecnicosModel
from app.models.equipo_biomedico import EquipoBiomedico as EquipoModel
from app.schemas.datos_tecnicos import DatosTecnicos, DatosTecnicosCreate, DatosTecnicosUpdate, DatosTecnicosConEquipo
from app.auth import require_admin

router = APIRouter(
    prefix="/datos-tecnicos",
    tags=[" Módulo 4: Inventario y Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=DatosTecnicos, status_code=status.HTTP_201_CREATED)
def crear_datos_tecnicos(
    datos: DatosTecnicosCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Crear datos técnicos para un equipo biomédico (relación 1:1) (Solo Administrador)
    """
    try:
        # Verificar que el equipo existe
        db_equipo = db.query(EquipoModel).filter(
            EquipoModel.id_equipo == datos.id_equipo
        ).first()
        if not db_equipo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Equipo con ID {datos.id_equipo} no encontrado"
            )

        # Verificar que el equipo no tenga ya datos técnicos
        db_datos_existente = db.query(DatosTecnicosModel).filter(
            DatosTecnicosModel.id_equipo == datos.id_equipo
        ).first()
        if db_datos_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este equipo ya tiene datos técnicos registrados"
            )

        # Crear datos técnicos
        db_datos = DatosTecnicosModel(**datos.model_dump())
        db.add(db_datos)
        db.commit()
        db.refresh(db_datos)
        return db_datos
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear datos técnicos: {str(e)}"
        )


@router.get("/", response_model=List[DatosTecnicosConEquipo])
def obtener_datos_tecnicos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de datos técnicos con información del equipo (Solo Administrador)
    """
    try:
        datos = db.query(DatosTecnicosModel).offset(skip).limit(limit).all()
        return datos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener datos técnicos: {str(e)}"
        )


@router.get("/{datos_id}", response_model=DatosTecnicosConEquipo)
def obtener_dato_tecnico(
    datos_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener datos técnicos específicos por ID (Solo Administrador)
    """
    try:
        db_datos = db.query(DatosTecnicosModel).filter(
            DatosTecnicosModel.id_dato_tecnico == datos_id
        ).first()
        if db_datos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Datos técnicos no encontrados"
            )
        return db_datos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener datos técnicos: {str(e)}"
        )


@router.get("/equipo/{equipo_id}", response_model=DatosTecnicos)
def obtener_datos_tecnicos_por_equipo(
    equipo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener los datos técnicos de un equipo específico (Solo Administrador)
    """
    try:
        db_datos = db.query(DatosTecnicosModel).filter(
            DatosTecnicosModel.id_equipo == equipo_id
        ).first()
        if db_datos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Este equipo no tiene datos técnicos registrados"
            )
        return db_datos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener datos técnicos: {str(e)}"
        )


@router.put("/{datos_id}", response_model=DatosTecnicos)
def actualizar_datos_tecnicos(
    datos_id: int,
    datos: DatosTecnicosUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Actualizar datos técnicos existentes (Solo Administrador)
    """
    try:
        db_datos = db.query(DatosTecnicosModel).filter(
            DatosTecnicosModel.id_dato_tecnico == datos_id
        ).first()
        if db_datos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Datos técnicos no encontrados"
            )

        datos_data = datos.model_dump(exclude_unset=True)
        for key, value in datos_data.items():
            setattr(db_datos, key, value)

        db.commit()
        db.refresh(db_datos)
        return db_datos
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar datos técnicos: {str(e)}"
        )


@router.delete("/{datos_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_datos_tecnicos(
    datos_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Eliminar datos técnicos (Solo Administrador)
    """
    try:
        db_datos = db.query(DatosTecnicosModel).filter(
            DatosTecnicosModel.id_dato_tecnico == datos_id
        ).first()
        if db_datos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Datos técnicos no encontrados"
            )

        db.delete(db_datos)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar datos técnicos: {str(e)}"
        )
