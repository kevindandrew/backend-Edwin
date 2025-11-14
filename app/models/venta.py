"""
Modelo de SQLAlchemy para la tabla VENTA
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String(50), unique=True, index=True)
    fecha_venta = Column(Date)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    total_venta = Column(Numeric(10, 2))
    metodo_pago = Column(String(50))
    estado_venta = Column(String(50))
    observaciones = Column(Text)
    id_usuario_registro = Column(Integer, ForeignKey("usuario.id_usuario"))

    # Relaciones
    cliente = relationship("Cliente")
    usuario_registro = relationship("Usuario")
    detalles = relationship(
        "DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
