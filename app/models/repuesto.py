"""
Modelo de SQLAlchemy para la tabla REPUESTO
"""
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.database import Base


class Repuesto(Base):
    __tablename__ = "repuesto"

    id_repuesto = Column(Integer, primary_key=True, index=True)
    nombre_repuesto = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio_unitario = Column(Numeric(10, 2))
    stock_disponible = Column(Integer, default=0)
    proveedor = Column(String(100))

    # Relaciones
    uso_repuestos = relationship(
        "UsoRepuesto", back_populates="repuesto", cascade="all, delete-orphan")
