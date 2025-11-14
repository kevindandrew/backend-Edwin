"""
Modelo de SQLAlchemy para la tabla EQUIPO_BIOMEDICO
"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EquipoBiomedico(Base):
    __tablename__ = "equipo_biomedico"

    id_equipo = Column(Integer, primary_key=True, index=True)
    nombre_equipo = Column(String(100), nullable=False)
    modelo = Column(String(100))
    numero_serie = Column(String(30), unique=True, index=True)
    fecha_adquisicion = Column(Date)
    garantia = Column(String(150))
    proveedor = Column(String(100))
    estado = Column(String(50))
    id_ubicacion = Column(Integer, ForeignKey("ubicacion.id_ubicacion"))
    id_fabricante = Column(Integer, ForeignKey("fabricante.id_fabricante"))
    id_categoria = Column(Integer, ForeignKey("categoria_equipo.id_categoria"))
    id_riesgo = Column(Integer, ForeignKey("nivel_riesgo.id_riesgo"))
    id_tecnologia = Column(Integer, ForeignKey(
        "tipo_tecnologia.id_tecnologia"))
    id_usuario_registro = Column(Integer, ForeignKey("usuario.id_usuario"))

    # Relaciones
    ubicacion = relationship("Ubicacion")
    fabricante = relationship("Fabricante")
    categoria = relationship("CategoriaEquipo")
    nivel_riesgo = relationship("NivelRiesgo")
    tecnologia = relationship("TipoTecnologia")
    usuario_registro = relationship("Usuario")
    datos_tecnicos = relationship(
        "DatosTecnicos", back_populates="equipo", uselist=False, cascade="all, delete-orphan")
