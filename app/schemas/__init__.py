"""
Módulo de schemas de Pydantic
Importa todos los schemas para facilitar el acceso
"""
from app.schemas.rol import Rol, RolCreate, RolUpdate, RolBase
from app.schemas.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioConRol
from app.schemas.cliente import Cliente, ClienteCreate, ClienteUpdate, ClienteConUbicaciones
from app.schemas.ubicacion import Ubicacion, UbicacionCreate, UbicacionUpdate, UbicacionConCliente
from app.schemas.categoria_equipo import CategoriaEquipo, CategoriaEquipoCreate, CategoriaEquipoUpdate
from app.schemas.nivel_riesgo import NivelRiesgo, NivelRiesgoCreate, NivelRiesgoUpdate
from app.schemas.fabricante import Fabricante, FabricanteCreate, FabricanteUpdate
from app.schemas.tipo_tecnologia import TipoTecnologia, TipoTecnologiaCreate, TipoTecnologiaUpdate
from app.schemas.equipo_biomedico import EquipoBiomedico, EquipoBiomedicoCreate, EquipoBiomedicoUpdate, EquipoBiomedicoDetallado
from app.schemas.datos_tecnicos import DatosTecnicos, DatosTecnicosCreate, DatosTecnicosUpdate, DatosTecnicosConEquipo
from app.schemas.mantenimiento import Mantenimiento, MantenimientoCreate, MantenimientoUpdate, MantenimientoDetallado
from app.schemas.repuesto import Repuesto, RepuestoCreate, RepuestoUpdate
from app.schemas.uso_repuesto import UsoRepuesto, UsoRepuestoCreate, UsoRepuestoUpdate, UsoRepuestoConDetalles
from app.schemas.compra_adquisicion import CompraAdquisicion, CompraAdquisicionCreate, CompraAdquisicionUpdate, CompraAdquisicionDetallada
from app.schemas.detalle_compra import DetalleCompra, DetalleCompraCreate, DetalleCompraUpdate, DetalleCompraConRelaciones
from app.schemas.venta import Venta, VentaCreate, VentaUpdate, VentaDetallada
from app.schemas.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate, DetalleVentaConRelaciones
from app.schemas.auth import Token, LoginRequest, LoginResponse

__all__ = [
    "Rol", "RolCreate", "RolUpdate", "RolBase",
    "Usuario", "UsuarioCreate", "UsuarioUpdate", "UsuarioConRol",
    "Cliente", "ClienteCreate", "ClienteUpdate", "ClienteConUbicaciones",
    "Ubicacion", "UbicacionCreate", "UbicacionUpdate", "UbicacionConCliente",
    "CategoriaEquipo", "CategoriaEquipoCreate", "CategoriaEquipoUpdate",
    "NivelRiesgo", "NivelRiesgoCreate", "NivelRiesgoUpdate",
    "Fabricante", "FabricanteCreate", "FabricanteUpdate",
    "TipoTecnologia", "TipoTecnologiaCreate", "TipoTecnologiaUpdate",
    "EquipoBiomedico", "EquipoBiomedicoCreate", "EquipoBiomedicoUpdate", "EquipoBiomedicoDetallado",
    "DatosTecnicos", "DatosTecnicosCreate", "DatosTecnicosUpdate", "DatosTecnicosConEquipo",
    "Mantenimiento", "MantenimientoCreate", "MantenimientoUpdate", "MantenimientoDetallado",
    "Repuesto", "RepuestoCreate", "RepuestoUpdate",
    "UsoRepuesto", "UsoRepuestoCreate", "UsoRepuestoUpdate", "UsoRepuestoConDetalles",
    "CompraAdquisicion", "CompraAdquisicionCreate", "CompraAdquisicionUpdate", "CompraAdquisicionDetallada",
    "DetalleCompra", "DetalleCompraCreate", "DetalleCompraUpdate", "DetalleCompraConRelaciones",
    "Venta", "VentaCreate", "VentaUpdate", "VentaDetallada",
    "DetalleVenta", "DetalleVentaCreate", "DetalleVentaUpdate", "DetalleVentaConRelaciones"
]
