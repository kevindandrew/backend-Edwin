"""
Modelo de SQLAlchemy para la tabla UBICACION
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id_ubicacion = Column(Integer, primary_key=True, index=True)
    nombre_ubicacion = Column(String(100))
    id_cliente = Column(Integer, ForeignKey(
        "cliente.id_cliente"), nullable=True)

    # Relaciones
    cliente = relationship("Cliente", back_populates="ubicaciones")
