"""
Modelo de SQLAlchemy para la tabla ROL
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), nullable=False)

    # Relación con usuarios
    usuarios = relationship("Usuario", back_populates="rol")
