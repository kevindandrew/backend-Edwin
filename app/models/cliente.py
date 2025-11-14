"""
Modelo de SQLAlchemy para la tabla CLIENTE
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre_institucion = Column(String(150), nullable=False)
    nit_ruc = Column(String(20), unique=True, index=True)
    direccion = Column(String(255))
    telefono_contacto = Column(String(50))
    email_contacto = Column(String(100))
    persona_contacto = Column(String(100))

    # Relaciones
    ubicaciones = relationship("Ubicacion", back_populates="cliente")
