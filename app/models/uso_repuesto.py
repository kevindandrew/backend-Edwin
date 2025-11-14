"""
Modelo de SQLAlchemy para la tabla USO_REPUESTO
Tabla intermedia many-to-many entre MANTENIMIENTO y REPUESTO
"""
from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UsoRepuesto(Base):
    __tablename__ = "uso_repuesto"

    id_mantenimiento = Column(Integer, ForeignKey(
        "mantenimiento.id_mantenimiento", ondelete="CASCADE"), primary_key=True)
    id_repuesto = Column(Integer, ForeignKey(
        "repuesto.id_repuesto", ondelete="CASCADE"), primary_key=True)
    cantidad_usada = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2))

    # Relaciones
    mantenimiento = relationship(
        "Mantenimiento", back_populates="uso_repuestos")
    repuesto = relationship("Repuesto", back_populates="uso_repuestos")
