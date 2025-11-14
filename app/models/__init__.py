"""
Módulo de modelos de SQLAlchemy
Importa todos los modelos para facilitar el acceso
"""
from app.database import Base
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.ubicacion import Ubicacion
from app.models.categoria_equipo import CategoriaEquipo
from app.models.nivel_riesgo import NivelRiesgo
from app.models.fabricante import Fabricante
from app.models.tipo_tecnologia import TipoTecnologia
from app.models.equipo_biomedico import EquipoBiomedico
from app.models.datos_tecnicos import DatosTecnicos
from app.models.mantenimiento import Mantenimiento
from app.models.repuesto import Repuesto
from app.models.uso_repuesto import UsoRepuesto
from app.models.compra_adquisicion import CompraAdquisicion
from app.models.detalle_compra import DetalleCompra
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta

__all__ = ["Base", "Rol", "Usuario", "Cliente", "Ubicacion",
           "CategoriaEquipo", "NivelRiesgo", "Fabricante", "TipoTecnologia",
           "EquipoBiomedico", "DatosTecnicos",
           "Mantenimiento", "Repuesto", "UsoRepuesto",
           "CompraAdquisicion", "DetalleCompra",
           "Venta", "DetalleVenta"]
