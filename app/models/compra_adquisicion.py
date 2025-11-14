"""
Modelo de SQLAlchemy para la tabla COMPRA_ADQUISICION
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CompraAdquisicion(Base):
    __tablename__ = "compra_adquisicion"

    id_compra = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String(50), unique=True, index=True)
    fecha_compra = Column(Date)
    proveedor = Column(String(100))
    total_compra = Column(Numeric(10, 2))
    metodo_pago = Column(String(50))
    observaciones = Column(Text)
    id_usuario_registro = Column(Integer, ForeignKey("usuario.id_usuario"))

    # Relaciones
    usuario_registro = relationship("Usuario")
    detalles = relationship(
        "DetalleCompra", back_populates="compra", cascade="all, delete-orphan")
