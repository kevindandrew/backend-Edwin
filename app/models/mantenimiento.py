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
    tipo_mantenimiento = Column(String(90))
    fecha_programada = Column(Date)
    fecha_realizacion = Column(Date)
    descripcion_trabajo = Column(Text)
    costo_total = Column(Numeric(10, 2))
    id_tecnico = Column(Integer, ForeignKey("usuario.id_usuario"))

    # Relaciones
    equipo = relationship("EquipoBiomedico")
    tecnico = relationship("Usuario")
    uso_repuestos = relationship(
        "UsoRepuesto", back_populates="mantenimiento", cascade="all, delete-orphan")
