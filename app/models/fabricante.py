"""
Modelo de SQLAlchemy para la tabla FABRICANTE
"""
from sqlalchemy import Column, Integer, String
from app.database import Base


class Fabricante(Base):
    __tablename__ = "fabricante"

    id_fabricante = Column(Integer, primary_key=True, index=True)
    nombre_fabricante = Column(String(100), nullable=False)
    pais_origen = Column(String(80))
    contacto = Column(String(80))
    telefono = Column(String(80))
    correo = Column(String(100))
    sitio_web = Column(String(150))
