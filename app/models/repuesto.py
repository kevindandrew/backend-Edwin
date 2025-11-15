"""
Modelo de SQLAlchemy para la tabla REPUESTO
"""
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Repuesto(Base):
    __tablename__ = "repuesto"

    id_repuesto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    stock = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=0)
    id_tecnologia = Column(Integer, ForeignKey(
        "tipo_tecnologia.id_tecnologia"))

    # Relaciones
    tecnologia = relationship("TipoTecnologia")
    uso_repuestos = relationship(
        "UsoRepuesto", back_populates="repuesto", cascade="all, delete-orphan")
