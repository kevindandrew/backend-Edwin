"""
Modelo de SQLAlchemy para la tabla TIPO_TECNOLOGIA
"""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class TipoTecnologia(Base):
    __tablename__ = "tipo_tecnologia"

    id_tecnologia = Column(Integer, primary_key=True, index=True)
    nombre_tecnologia = Column(String(50), nullable=False)
    descripcion = Column(Text)
