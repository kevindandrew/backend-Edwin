"""
Modelo de SQLAlchemy para la tabla DATOS_TECNICOS
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class DatosTecnicos(Base):
    __tablename__ = "datos_tecnicos"

    id_dato_tecnico = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey(
        "equipo_biomedico.id_equipo", ondelete="CASCADE"), unique=True, nullable=False)
    voltaje_operacion = Column(String(50))
    potencia = Column(String(50))
    frecuencia = Column(String(50))
    peso = Column(String(50))
    dimensiones = Column(String(50))
    vida_util = Column(String(50))
    manual_operacion = Column(String(255))
    observaciones = Column(Text)

    # Relación
    equipo = relationship("EquipoBiomedico", back_populates="datos_tecnicos")
