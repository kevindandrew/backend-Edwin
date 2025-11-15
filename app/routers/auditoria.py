"""
Router para consultas de auditoría del sistema (SOLO LECTURA)
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, date
from app.database import get_db
from app.models.auditoria import Auditoria as AuditoriaModel
from app.schemas.auditoria import Auditoria, AuditoriaConUsuario
from app.auth import require_admin

router = APIRouter(
    prefix="/auditoria",
    tags=["🔍 Módulo 8: Auditoría del Sistema"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("/", response_model=List[AuditoriaConUsuario])
def obtener_auditoria(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, le=500),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener lista de registros de auditoría (Solo Administrador)
    """
    try:
        registros = db.query(AuditoriaModel).order_by(
            desc(AuditoriaModel.fecha_operacion)
        ).offset(skip).limit(limit).all()
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener auditoría: {str(e)}"
        )


@router.get("/tabla/{nombre_tabla}", response_model=List[AuditoriaConUsuario])
def obtener_auditoria_por_tabla(
    nombre_tabla: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener auditoría filtrada por nombre de tabla
    """
    try:
        registros = db.query(AuditoriaModel).filter(
            AuditoriaModel.tabla == nombre_tabla.upper()
        ).order_by(
            desc(AuditoriaModel.fecha_operacion)
        ).offset(skip).limit(limit).all()
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener auditoría: {str(e)}"
        )


@router.get("/usuario/{usuario_id}", response_model=List[AuditoriaConUsuario])
def obtener_auditoria_por_usuario(
    usuario_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener todas las operaciones realizadas por un usuario específico
    """
    try:
        registros = db.query(AuditoriaModel).filter(
            AuditoriaModel.id_usuario == usuario_id
        ).order_by(
            desc(AuditoriaModel.fecha_operacion)
        ).offset(skip).limit(limit).all()
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener auditoría: {str(e)}"
        )


@router.get("/registro/{tabla}/{id_registro}", response_model=List[AuditoriaConUsuario])
def obtener_historial_registro(
    tabla: str,
    id_registro: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener todo el historial de cambios de un registro específico
    """
    try:
        registros = db.query(AuditoriaModel).filter(
            AuditoriaModel.tabla == tabla.upper(),
            AuditoriaModel.id_registro == id_registro
        ).order_by(
            desc(AuditoriaModel.fecha_operacion)
        ).all()
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener historial: {str(e)}"
        )


@router.get("/operacion/{tipo_operacion}", response_model=List[AuditoriaConUsuario])
def obtener_auditoria_por_operacion(
    tipo_operacion: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener auditoría filtrada por tipo de operación (INSERT, UPDATE, DELETE)
    """
    try:
        if tipo_operacion.upper() not in ['INSERT', 'UPDATE', 'DELETE']:
            raise HTTPException(
                status_code=400,
                detail="Tipo de operación inválido. Use: INSERT, UPDATE o DELETE"
            )

        registros = db.query(AuditoriaModel).filter(
            AuditoriaModel.operacion == tipo_operacion.upper()
        ).order_by(
            desc(AuditoriaModel.fecha_operacion)
        ).offset(skip).limit(limit).all()
        return registros
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener auditoría: {str(e)}"
        )


@router.get("/fecha", response_model=List[AuditoriaConUsuario])
def obtener_auditoria_por_fecha(
    fecha_inicio: Optional[date] = Query(
        default=None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(
        default=None, description="Fecha fin (YYYY-MM-DD)"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener auditoría filtrada por rango de fechas
    """
    try:
        query = db.query(AuditoriaModel)

        if fecha_inicio:
            query = query.filter(AuditoriaModel.fecha_operacion >= datetime.combine(
                fecha_inicio, datetime.min.time()))

        if fecha_fin:
            query = query.filter(AuditoriaModel.fecha_operacion <= datetime.combine(
                fecha_fin, datetime.max.time()))

        registros = query.order_by(
            desc(AuditoriaModel.fecha_operacion)
        ).offset(skip).limit(limit).all()

        return registros
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener auditoría: {str(e)}"
        )


@router.get("/estadisticas")
def obtener_estadisticas_auditoria(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener estadísticas generales de auditoría
    """
    try:
        from sqlalchemy import func

        # Total de registros
        total = db.query(func.count(AuditoriaModel.id_auditoria)).scalar()

        # Por operación
        por_operacion = db.query(
            AuditoriaModel.operacion,
            func.count(AuditoriaModel.id_auditoria).label('total')
        ).group_by(AuditoriaModel.operacion).all()

        # Por tabla
        por_tabla = db.query(
            AuditoriaModel.tabla,
            func.count(AuditoriaModel.id_auditoria).label('total')
        ).group_by(AuditoriaModel.tabla).order_by(
            desc(func.count(AuditoriaModel.id_auditoria))
        ).limit(10).all()

        return {
            "total_registros": total,
            "por_operacion": [
                {"operacion": op, "total": total}
                for op, total in por_operacion
            ],
            "top_tablas": [
                {"tabla": tabla, "total": total}
                for tabla, total in por_tabla
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )
