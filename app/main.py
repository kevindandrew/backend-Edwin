"""
API FastAPI para Sistema de Gestión de Equipos Biomédicos
"""
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Importar los routers
from app.routers import (
    rol_router, usuario_router,
    cliente_router, ubicacion_router,
    categoria_equipo_router, nivel_riesgo_router,
    fabricante_router, tipo_tecnologia_router,
    equipo_biomedico_router, datos_tecnicos_router,
    mantenimiento_router, repuesto_router, uso_repuesto_router,
    compra_adquisicion_router, detalle_compra_router,
    venta_router, detalle_venta_router,
    estadisticas_router, auth_router, auditoria_router
)
from app.database import engine, get_db
from app.models import Base

# Cargar variables de entorno
load_dotenv()

# IMPORTANTE: NO crear tablas automáticamente - la base de datos ya existe con datos
# Base.metadata.create_all(bind=engine)  # ⚠️ COMENTADO para no sobreescribir datos existentes
print("📋 Conectando a base de datos existente 'Edwin' (sin modificar estructura)")

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Equipos Biomédicos",
    description="API para gestión de equipos biomédicos, mantenimiento y ventas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
# Auth debe ir primero para que /docs funcione correctamente
app.include_router(auth_router)
app.include_router(rol_router)
app.include_router(usuario_router)
app.include_router(cliente_router)
app.include_router(ubicacion_router)
app.include_router(categoria_equipo_router)
app.include_router(nivel_riesgo_router)
app.include_router(fabricante_router)
app.include_router(tipo_tecnologia_router)
app.include_router(equipo_biomedico_router)
app.include_router(datos_tecnicos_router)
app.include_router(mantenimiento_router)
app.include_router(repuesto_router)
app.include_router(uso_repuesto_router)
app.include_router(compra_adquisicion_router)
app.include_router(detalle_compra_router)
app.include_router(venta_router)
app.include_router(detalle_venta_router)
app.include_router(estadisticas_router)
app.include_router(auditoria_router)


@app.get("/")
def read_root():
    """
    Endpoint de bienvenida
    """
    return {
        "mensaje": "¡Bienvenido al Sistema de Gestión de Equipos Biomédicos!",
        "version": "1.0.0",
        "database": "Edwin",
        "docs": "/docs",
        "status": "🚀 API funcionando correctamente"
    }


@app.get("/health")
def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    try:
        # Verificar variables de entorno
        database_url = os.getenv("DATABASE_URL")

        return {
            "status": "healthy",
            "database_configured": bool(database_url),
            "message": "✅ API y configuración OK"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en health check: {str(e)}")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    Endpoint de ejemplo (mantener por compatibilidad)
    """
    return {"item_id": item_id, "q": q}
