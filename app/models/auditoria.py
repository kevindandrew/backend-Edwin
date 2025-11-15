"""
Modelo de SQLAlchemy para la tabla AUDITORIA
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Auditoria(Base):
    __tablename__ = "auditoria"

    id_auditoria = Column(Integer, primary_key=True, index=True)
    tabla = Column(String(50), nullable=False, index=True)
    id_registro = Column(Integer, nullable=False)
    operacion = Column(String(10), nullable=False)  # INSERT, UPDATE, DELETE
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    fecha_operacion = Column(DateTime, default=datetime.utcnow, index=True)
    datos_anteriores = Column(JSONB)
    datos_nuevos = Column(JSONB)
    ip_origen = Column(String(45))

    # Relaciones
    usuario = relationship("Usuario")
