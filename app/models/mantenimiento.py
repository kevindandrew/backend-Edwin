"""
Modelo de SQLAlchemy para la tabla MANTENIMIENTO
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Mantenimiento(Base):
    __tablename__ = "mantenimiento"

    id_mantenimiento = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey(
        "equipo_biomedico.id_equipo"), nullable=False)
    tipo_mantenimiento = Column(String(50))
    fecha_mantenimiento = Column(Date)
    descripcion = Column(Text)
    costo = Column(Numeric(10, 2))
    tecnico_responsable = Column(String(100))
    observaciones = Column(Text)
    id_usuario_registro = Column(Integer, ForeignKey("usuario.id_usuario"))

    # Relaciones
    equipo = relationship("EquipoBiomedico")
    usuario_registro = relationship("Usuario")
    uso_repuestos = relationship(
        "UsoRepuesto", back_populates="mantenimiento", cascade="all, delete-orphan")
