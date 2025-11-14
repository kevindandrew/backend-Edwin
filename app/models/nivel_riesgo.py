"""
Modelo de SQLAlchemy para la tabla NIVEL_RIESGO
"""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class NivelRiesgo(Base):
    __tablename__ = "nivel_riesgo"

    id_riesgo = Column(Integer, primary_key=True, index=True)
    nombre_riesgo = Column(String(50), nullable=False)
    descripcion = Column(Text)
