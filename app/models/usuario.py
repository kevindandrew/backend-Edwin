"""
Modelo de SQLAlchemy para la tabla USUARIO
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100))
    nombre_usuario = Column(String(50), unique=True,
                            nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)

    # Relación con rol
    rol = relationship("Rol", back_populates="usuarios")
