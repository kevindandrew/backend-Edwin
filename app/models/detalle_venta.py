"""
Modelo de SQLAlchemy para la tabla DETALLE_VENTA
"""
from sqlalchemy import Column, Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id_detalle_venta = Column(Integer, primary_key=True, index=True)
    id_venta = Column(Integer, ForeignKey(
        "venta.id_venta", ondelete="CASCADE"), nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipo_biomedico.id_equipo"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2))
    subtotal = Column(Numeric(10, 2))
    descripcion = Column(Text)

    # Relaciones
    venta = relationship("Venta", back_populates="detalles")
    equipo = relationship("EquipoBiomedico")
