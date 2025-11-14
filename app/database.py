"""
Configuración de la base de datos PostgreSQL
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base declarativa
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
