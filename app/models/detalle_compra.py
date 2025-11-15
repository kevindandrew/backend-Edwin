"""
Modelo de SQLAlchemy para la tabla DETALLE_COMPRA
"""
from sqlalchemy import Column, Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class DetalleCompra(Base):
    __tablename__ = "detalle_compra"

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_compra = Column(Integer, ForeignKey(
        "compra_adquisicion.id_compra", ondelete="CASCADE"), nullable=False)
    id_repuesto = Column(Integer, ForeignKey("repuesto.id_repuesto"))
    id_equipo = Column(Integer, ForeignKey("equipo_biomedico.id_equipo"))
    cantidad = Column(Integer)
    precio_unitario = Column(Numeric(10, 2))

    # Relaciones
    compra = relationship("CompraAdquisicion", back_populates="detalles")
    repuesto = relationship("Repuesto")
    equipo = relationship("EquipoBiomedico")
