"""
Router para estadísticas y reportes del sistema
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date, datetime
from app.database import get_db
from app.models.equipo_biomedico import EquipoBiomedico
from app.models.venta import Venta
from app.models.compra_adquisicion import CompraAdquisicion
from app.models.mantenimiento import Mantenimiento
from app.models.repuesto import Repuesto
from app.models.detalle_venta import DetalleVenta
from app.models.detalle_compra import DetalleCompra
from app.auth import require_admin

router = APIRouter(
    prefix="/estadisticas",
    tags=[" Estadísticas y Reportes"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("/dashboard")
def obtener_estadisticas_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener estadísticas generales para el dashboard principal
    """
    try:
        # Total de equipos por estado
        equipos_por_estado = db.query(
            EquipoBiomedico.estado,
            func.count(EquipoBiomedico.id_equipo).label('total')
        ).group_by(EquipoBiomedico.estado).all()

        # Total de equipos
        total_equipos = db.query(func.count(
            EquipoBiomedico.id_equipo)).scalar()

        # Repuestos con stock bajo (stock menor que stock_minimo)
        repuestos_stock_bajo = db.query(func.count(Repuesto.id_repuesto)).filter(
            Repuesto.stock < Repuesto.stock_minimo
        ).scalar()

        # Total de mantenimientos este mes (usar fecha_realizacion)
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        mantenimientos_mes = db.query(func.count(Mantenimiento.id_mantenimiento)).filter(
            Mantenimiento.fecha_realizacion.isnot(None),
            extract('month', Mantenimiento.fecha_realizacion) == mes_actual,
            extract('year', Mantenimiento.fecha_realizacion) == año_actual
        ).scalar()

        # Total de ventas este mes
        ventas_mes = db.query(func.count(Venta.id_venta)).filter(
            extract('month', Venta.fecha_venta) == mes_actual,
            extract('year', Venta.fecha_venta) == año_actual
        ).scalar()

        # Ingresos del mes (sum de monto_total)
        ingresos_mes = db.query(func.sum(Venta.monto_total)).filter(
            extract('month', Venta.fecha_venta) == mes_actual,
            extract('year', Venta.fecha_venta) == año_actual
        ).scalar() or 0

        # Egresos del mes (sum de monto_total)
        egresos_mes = db.query(func.sum(CompraAdquisicion.monto_total)).filter(
            extract('month', CompraAdquisicion.fecha_solicitud) == mes_actual,
            extract('year', CompraAdquisicion.fecha_solicitud) == año_actual
        ).scalar() or 0

        return {
            "total_equipos": total_equipos,
            "equipos_por_estado": [
                {"estado": estado, "total": total}
                for estado, total in equipos_por_estado
            ],
            "repuestos_stock_bajo": repuestos_stock_bajo,
            "mantenimientos_mes_actual": mantenimientos_mes,
            "ventas_mes_actual": ventas_mes,
            "ingresos_mes": float(ingresos_mes),
            "egresos_mes": float(egresos_mes),
            "balance_mes": float(ingresos_mes - egresos_mes)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )


@router.get("/equipos/por-categoria")
def obtener_equipos_por_categoria(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener la cantidad de equipos agrupados por categoría
    """
    try:
        from app.models.categoria_equipo import CategoriaEquipo

        resultado = db.query(
            CategoriaEquipo.nombre_categoria,
            func.count(EquipoBiomedico.id_equipo).label('total')
        ).outerjoin(
            EquipoBiomedico,
            EquipoBiomedico.id_categoria == CategoriaEquipo.id_categoria
        ).group_by(CategoriaEquipo.nombre_categoria).all()

        return [
            {"categoria": nombre, "total": total}
            for nombre, total in resultado
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener equipos por categoría: {str(e)}"
        )


@router.get("/ventas/por-mes")
def obtener_ventas_por_mes(
    año: int = Query(default=datetime.now().year,
                     description="Año a consultar"),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener total de ventas agrupado por mes para un año específico
    """
    try:
        resultado = db.query(
            extract('month', Venta.fecha_venta).label('mes'),
            func.count(Venta.id_venta).label('cantidad'),
            func.sum(Venta.monto_total).label('total')
        ).filter(
            extract('year', Venta.fecha_venta) == año
        ).group_by(extract('month', Venta.fecha_venta)).all()

        return [
            {
                "mes": int(mes),
                "cantidad_ventas": cantidad,
                "total_ventas": float(total or 0)
            }
            for mes, cantidad, total in resultado
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener ventas por mes: {str(e)}"
        )


@router.get("/compras/por-mes")
def obtener_compras_por_mes(
    año: int = Query(default=datetime.now().year,
                     description="Año a consultar"),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener total de compras agrupado por mes para un año específico
    """
    try:
        resultado = db.query(
            extract('month', CompraAdquisicion.fecha_solicitud).label('mes'),
            func.count(CompraAdquisicion.id_compra).label('cantidad'),
            func.sum(CompraAdquisicion.monto_total).label('total')
        ).filter(
            extract('year', CompraAdquisicion.fecha_solicitud) == año
        ).group_by(extract('month', CompraAdquisicion.fecha_solicitud)).all()

        return [
            {
                "mes": int(mes),
                "cantidad_compras": cantidad,
                "total_compras": float(total or 0)
            }
            for mes, cantidad, total in resultado
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener compras por mes: {str(e)}"
        )


@router.get("/mantenimientos/costos-por-equipo/{equipo_id}")
def obtener_costos_mantenimiento_equipo(
    equipo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener el costo total de mantenimientos para un equipo específico
    """
    try:
        # Verificar que el equipo existe
        equipo = db.query(EquipoBiomedico).filter(
            EquipoBiomedico.id_equipo == equipo_id
        ).first()
        if not equipo:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")

        # Calcular costos
        total_mantenimientos = db.query(func.count(Mantenimiento.id_mantenimiento)).filter(
            Mantenimiento.id_equipo == equipo_id
        ).scalar()

        costo_total = db.query(func.sum(Mantenimiento.costo_total)).filter(
            Mantenimiento.id_equipo == equipo_id
        ).scalar() or 0

        # Mantenimientos por tipo
        por_tipo = db.query(
            Mantenimiento.tipo_mantenimiento,
            func.count(Mantenimiento.id_mantenimiento).label('cantidad'),
            func.sum(Mantenimiento.costo_total).label('costo_total')
        ).filter(
            Mantenimiento.id_equipo == equipo_id
        ).group_by(Mantenimiento.tipo_mantenimiento).all()

        return {
            "equipo_id": equipo_id,
            "nombre_equipo": equipo.nombre_equipo,
            "total_mantenimientos": total_mantenimientos,
            "costo_total": float(costo_total),
            "por_tipo": [
                {
                    "tipo": tipo,
                    "cantidad": cantidad,
                    "costo_total": float(costo or 0)
                }
                for tipo, cantidad, costo in por_tipo
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener costos de mantenimiento: {str(e)}"
        )


@router.get("/repuestos/mas-usados")
def obtener_repuestos_mas_usados(
    limit: int = Query(
        default=10, description="Cantidad de repuestos a retornar"),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener los repuestos más utilizados en mantenimientos
    """
    try:
        from app.models.uso_repuesto import UsoRepuesto

        resultado = db.query(
            Repuesto.id_repuesto,
            Repuesto.nombre,
            func.sum(UsoRepuesto.cantidad_usada).label('total_usado'),
            func.count(UsoRepuesto.id_mantenimiento).label('veces_usado')
        ).join(
            UsoRepuesto, UsoRepuesto.id_repuesto == Repuesto.id_repuesto
        ).group_by(
            Repuesto.id_repuesto,
            Repuesto.nombre
        ).order_by(
            func.sum(UsoRepuesto.cantidad_usada).desc()
        ).limit(limit).all()

        return [
            {
                "id_repuesto": id_rep,
                "nombre_repuesto": nombre,
                "total_usado": int(total),
                "veces_usado": int(veces)
            }
            for id_rep, nombre, total, veces in resultado
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener repuestos más usados: {str(e)}"
        )


@router.get("/clientes/top-compradores")
def obtener_top_clientes(
    limit: int = Query(
        default=10, description="Cantidad de clientes a retornar"),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener los clientes con mayor volumen de compras (Solo Administrador)
    """
    try:
        from app.models.cliente import Cliente

        resultado = db.query(
            Cliente.id_cliente,
            Cliente.nombre_institucion,
            func.count(Venta.id_venta).label('total_ventas'),
            func.sum(Venta.monto_total).label('monto_total')
        ).join(
            Venta, Venta.id_cliente == Cliente.id_cliente
        ).group_by(
            Cliente.id_cliente,
            Cliente.nombre_institucion
        ).order_by(
            func.sum(Venta.monto_total).desc()
        ).limit(limit).all()

        return [
            {
                "id_cliente": id_cli,
                "nombre_cliente": nombre,
                "total_ventas": int(total),
                "monto_total": float(monto or 0)
            }
            for id_cli, nombre, total, monto in resultado
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener top clientes: {str(e)}"
        )


@router.get("/ventas/resumen/{venta_id}")
def obtener_resumen_venta(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener resumen completo de una venta con cálculos automáticos
    """
    try:
        venta = db.query(Venta).filter(Venta.id_venta == venta_id).first()
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")

        # Calcular totales de los detalles (solo precio_venta)
        detalles = db.query(
            DetalleVenta.id_detalle_venta,
            DetalleVenta.precio_venta
        ).filter(DetalleVenta.id_venta == venta_id).all()

        subtotal_calculado = sum(float(d.precio_venta or 0) for d in detalles)
        total_items = len(detalles)

        return {
            "id_venta": venta.id_venta,
            "fecha_venta": str(venta.fecha_venta),
            "monto_total": float(venta.monto_total or 0),
            "estado_venta": venta.estado_venta,
            "resumen": {
                "total_items": total_items,
                "subtotal": subtotal_calculado
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener resumen de venta: {str(e)}"
        )


@router.get("/compras/resumen/{compra_id}")
def obtener_resumen_compra(
    compra_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    """
    Obtener resumen completo de una compra con cálculos automáticos
    """
    try:
        compra = db.query(CompraAdquisicion).filter(
            CompraAdquisicion.id_compra == compra_id
        ).first()
        if not compra:
            raise HTTPException(status_code=404, detail="Compra no encontrada")

        # Calcular totales de los detalles (cantidad y precio_unitario)
        detalles = db.query(
            DetalleCompra.id_detalle,
            DetalleCompra.cantidad,
            DetalleCompra.precio_unitario
        ).filter(DetalleCompra.id_compra == compra_id).all()

        subtotal_calculado = sum(
            float((d.cantidad or 0) * (d.precio_unitario or 0)) for d in detalles)
        total_items = len(detalles)
        total_cantidad = sum(int(d.cantidad or 0) for d in detalles)

        return {
            "id_compra": compra.id_compra,
            "fecha_solicitud": str(compra.fecha_solicitud),
            "fecha_aprobacion": str(compra.fecha_aprobacion) if compra.fecha_aprobacion else None,
            "estado_compra": compra.estado_compra,
            "monto_total": float(compra.monto_total or 0),
            "resumen": {
                "total_items": total_items,
                "total_cantidad": total_cantidad,
                "subtotal": subtotal_calculado
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener resumen de compra: {str(e)}"
        )
