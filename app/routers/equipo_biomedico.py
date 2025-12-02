"""
Router para operaciones CRUD de Equipos Biomédicos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.equipo_biomedico import EquipoBiomedico as EquipoModel
from app.models.ubicacion import Ubicacion as UbicacionModel
from app.models.fabricante import Fabricante as FabricanteModel
from app.models.categoria_equipo import CategoriaEquipo as CategoriaModel
from app.models.nivel_riesgo import NivelRiesgo as NivelRiesgoModel
from app.models.tipo_tecnologia import TipoTecnologia as TecnologiaModel
from app.models.usuario import Usuario as UsuarioModel
from app.schemas.equipo_biomedico import EquipoBiomedico, EquipoBiomedicoCreate, EquipoBiomedicoUpdate, EquipoBiomedicoDetallado
from app.auth import require_admin_gestor_or_compras, require_any_authenticated

router = APIRouter(
    prefix="/equipos-biomedicos",
    tags=[" Módulo 4: Inventario y Equipos"],
    responses={404: {"description": "No encontrado"}},
)


@router.post("/", response_model=EquipoBiomedico, status_code=status.HTTP_201_CREATED)
def crear_equipo_biomedico(
    equipo: EquipoBiomedicoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_gestor_or_compras)
):
    """
    Crear un nuevo equipo biomédico (Solo Administrador)
    """
    try:
        # Validar número de serie único si se proporciona
        if equipo.numero_serie:
            db_equipo = db.query(EquipoModel).filter(
                EquipoModel.numero_serie == equipo.numero_serie
            ).first()
            if db_equipo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un equipo con ese número de serie"
                )

        # Validar relaciones si se proporcionan
        if equipo.id_ubicacion:
            if not db.query(UbicacionModel).filter(UbicacionModel.id_ubicacion == equipo.id_ubicacion).first():
                raise HTTPException(
                    status_code=404, detail=f"Ubicación {equipo.id_ubicacion} no encontrada")

        if equipo.id_fabricante:
            if not db.query(FabricanteModel).filter(FabricanteModel.id_fabricante == equipo.id_fabricante).first():
                raise HTTPException(
                    status_code=404, detail=f"Fabricante {equipo.id_fabricante} no encontrado")

        if equipo.id_categoria:
            if not db.query(CategoriaModel).filter(CategoriaModel.id_categoria == equipo.id_categoria).first():
                raise HTTPException(
                    status_code=404, detail=f"Categoría {equipo.id_categoria} no encontrada")

        if equipo.id_riesgo:
            if not db.query(NivelRiesgoModel).filter(NivelRiesgoModel.id_riesgo == equipo.id_riesgo).first():
                raise HTTPException(
                    status_code=404, detail=f"Nivel de riesgo {equipo.id_riesgo} no encontrado")

        if equipo.id_tecnologia:
            if not db.query(TecnologiaModel).filter(TecnologiaModel.id_tecnologia == equipo.id_tecnologia).first():
                raise HTTPException(
                    status_code=404, detail=f"Tipo de tecnología {equipo.id_tecnologia} no encontrado")

        if equipo.id_usuario_registro:
            if not db.query(UsuarioModel).filter(UsuarioModel.id_usuario == equipo.id_usuario_registro).first():
                raise HTTPException(
                    status_code=404, detail=f"Usuario {equipo.id_usuario_registro} no encontrado")

        # Crear equipo
        db_equipo = EquipoModel(**equipo.model_dump())
        db.add(db_equipo)
        db.commit()
        db.refresh(db_equipo)
        return db_equipo
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear equipo: {str(e)}"
        )


@router.get("/", response_model=List[EquipoBiomedico])
def obtener_equipos_biomedicos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_gestor_or_compras)
):
    """
    Obtener lista de equipos biomédicos (Solo Administrador)
    """
    try:
        equipos = db.query(EquipoModel).offset(skip).limit(limit).all()
        return equipos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener equipos: {str(e)}"
        )


@router.get("/buscar/serie/{numero_serie}", response_model=EquipoBiomedicoDetallado)
def buscar_equipo_por_serie(
    numero_serie: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Buscar un equipo biomédico por número de serie (Solo Administrador)
    """
    try:
        db_equipo = db.query(EquipoModel).filter(
            EquipoModel.numero_serie == numero_serie
        ).first()
        if db_equipo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipo no encontrado"
            )
        return db_equipo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar equipo: {str(e)}"
        )


@router.get("/filtrar/ubicacion/{ubicacion_id}", response_model=List[EquipoBiomedico])
def obtener_equipos_por_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los equipos de una ubicación específica (Solo Administrador)
    """
    try:
        equipos = db.query(EquipoModel).filter(
            EquipoModel.id_ubicacion == ubicacion_id
        ).all()
        return equipos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener equipos: {str(e)}"
        )


@router.get("/filtrar/estado/{estado}", response_model=List[EquipoBiomedico])
def obtener_equipos_por_estado(
    estado: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener todos los equipos por estado (operativo, mantenimiento, fuera de servicio, etc.) (Solo Administrador)
    """
    try:
        equipos = db.query(EquipoModel).filter(
            EquipoModel.estado == estado
        ).all()
        return equipos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener equipos: {str(e)}"
        )


@router.get("/{equipo_id}", response_model=EquipoBiomedicoDetallado)
def obtener_equipo_biomedico(
    equipo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_authenticated)
):
    """
    Obtener un equipo biomédico específico por ID con todas sus relaciones (Solo Administrador)
    """
    try:
        db_equipo = db.query(EquipoModel).filter(
            EquipoModel.id_equipo == equipo_id
        ).first()
        if db_equipo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipo no encontrado"
            )
        return db_equipo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener equipo: {str(e)}"
        )


@router.put("/{equipo_id}", response_model=EquipoBiomedico)
def actualizar_equipo_biomedico(
    equipo_id: int,
    equipo: EquipoBiomedicoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_gestor_or_compras)
):
    """
    Actualizar un equipo biomédico existente (Solo Administrador)
    """
    try:
        db_equipo = db.query(EquipoModel).filter(
            EquipoModel.id_equipo == equipo_id
        ).first()
        if db_equipo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipo no encontrado"
            )

        equipo_data = equipo.model_dump(exclude_unset=True)

        # Validar número de serie único si se está cambiando
        if 'numero_serie' in equipo_data and equipo_data['numero_serie']:
            if equipo_data['numero_serie'] != db_equipo.numero_serie:
                existing = db.query(EquipoModel).filter(
                    EquipoModel.numero_serie == equipo_data['numero_serie']
                ).first()
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe un equipo con ese número de serie"
                    )

        # Validar relaciones si se están cambiando
        if 'id_ubicacion' in equipo_data and equipo_data['id_ubicacion']:
            if not db.query(UbicacionModel).filter(UbicacionModel.id_ubicacion == equipo_data['id_ubicacion']).first():
                raise HTTPException(
                    status_code=404, detail=f"Ubicación no encontrada")

        for key, value in equipo_data.items():
            setattr(db_equipo, key, value)

        db.commit()
        db.refresh(db_equipo)
        return db_equipo
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar equipo: {str(e)}"
        )


@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo_biomedico(
    equipo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin_gestor_or_compras)
):
    """
    Eliminar un equipo biomédico (también eliminará sus datos técnicos en cascada) (Solo Administrador)
    """
    try:
        db_equipo = db.query(EquipoModel).filter(
            EquipoModel.id_equipo == equipo_id
        ).first()
        if db_equipo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Equipo no encontrado"
            )

        db.delete(db_equipo)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar equipo: {str(e)}"
        )
