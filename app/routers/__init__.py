"""
Módulo de routers de FastAPI
Importa todos los routers para facilitar el acceso
"""
from app.routers.rol import router as rol_router
from app.routers.usuario import router as usuario_router
from app.routers.cliente import router as cliente_router
from app.routers.ubicacion import router as ubicacion_router
from app.routers.categoria_equipo import router as categoria_equipo_router
from app.routers.nivel_riesgo import router as nivel_riesgo_router
from app.routers.fabricante import router as fabricante_router
from app.routers.tipo_tecnologia import router as tipo_tecnologia_router
from app.routers.equipo_biomedico import router as equipo_biomedico_router
from app.routers.datos_tecnicos import router as datos_tecnicos_router
from app.routers.mantenimiento import router as mantenimiento_router
from app.routers.repuesto import router as repuesto_router
from app.routers.uso_repuesto import router as uso_repuesto_router
from app.routers.compra_adquisicion import router as compra_adquisicion_router
from app.routers.detalle_compra import router as detalle_compra_router
from app.routers.venta import router as venta_router
from app.routers.detalle_venta import router as detalle_venta_router
from app.routers.estadisticas import router as estadisticas_router
from app.routers.auth_router import router as auth_router
from app.routers.auditoria import router as auditoria_router

__all__ = [
    "rol_router", "usuario_router",
    "cliente_router", "ubicacion_router",
    "categoria_equipo_router", "nivel_riesgo_router",
    "fabricante_router", "tipo_tecnologia_router",
    "equipo_biomedico_router", "datos_tecnicos_router",
    "mantenimiento_router", "repuesto_router", "uso_repuesto_router",
    "compra_adquisicion_router", "detalle_compra_router",
    "venta_router", "detalle_venta_router",
    "estadisticas_router", "auth_router", "auditoria_router"
]
