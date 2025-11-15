"""
Modelo de SQLAlchemy para la tabla COMPRA_ADQUISICION
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CompraAdquisicion(Base):
    __tablename__ = "compra_adquisicion"

    id_compra = Column(Integer, primary_key=True, index=True)
    fecha_solicitud = Column(Date)
    fecha_aprobacion = Column(Date)
    estado_compra = Column(String(50))
    monto_total = Column(Numeric(10, 2))
    id_usuario_admin = Column(Integer, ForeignKey("usuario.id_usuario"))

    # Relaciones
    usuario_admin = relationship("Usuario")
    detalles = relationship(
        "DetalleCompra", back_populates="compra", cascade="all, delete-orphan")
