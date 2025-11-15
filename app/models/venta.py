"""
Modelo de SQLAlchemy para la tabla VENTA
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey(
        "cliente.id_cliente"), nullable=False)
    id_usuario_vendedor = Column(Integer, ForeignKey("usuario.id_usuario"))
    fecha_venta = Column(Date)
    monto_total = Column(Numeric(10, 2))
    estado_venta = Column(String(50))

    # Relaciones
    cliente = relationship("Cliente")
    usuario_vendedor = relationship("Usuario")
    detalles = relationship(
        "DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
