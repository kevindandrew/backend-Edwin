"""
Modelo de SQLAlchemy para la tabla CATEGORIA_EQUIPO
"""
from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class CategoriaEquipo(Base):
    __tablename__ = "categoria_equipo"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False)
    descripcion = Column(Text)
