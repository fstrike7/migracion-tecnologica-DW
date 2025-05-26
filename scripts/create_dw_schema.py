import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
print(f"🔍 DB_URL: postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Crear la URL de conexión
DATABASE_URL = "postgresql://test:test@localhost:5432/proyecto_final_dw?client_encoding=utf8"

# Crear engine y metadata
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

# === Definición de dimensiones ===

dim_tiempo = Table('dim_tiempo', metadata,
    Column('id_tiempo', Integer, primary_key=True),
    Column('fecha', String),
    Column('hora', Integer),
    Column('dia', Integer),
    Column('mes', Integer),
    Column('anio', Integer)
)

dim_ubicacion = Table('dim_ubicacion', metadata,
    Column('id_ubicacion', Integer, primary_key=True),
    Column('ciudad', String),
    Column('comuna', String),
    Column('barrio', String)
)

dim_tecnologia = Table('dim_tecnologia', metadata,
    Column('id_tecnologia', Integer, primary_key=True),
    Column('tipo_red', String),
    Column('banda', String),
    Column('proveedor', String)
)

dim_celda = Table('dim_celda', metadata,
    Column('id_celda', String, primary_key=True),
    Column('sitio', String),
    Column('sector', String),
    Column('id_ubicacion', Integer, ForeignKey('dim_ubicacion.id_ubicacion'))
)

# === Definición de hechos ===

fact_uso_dispositivos = Table('fact_uso_dispositivos', metadata,
    Column('id_fact', Integer, primary_key=True),
    Column('id_celda', String, ForeignKey('dim_celda.id_celda')),
    Column('id_tecnologia', Integer, ForeignKey('dim_tecnologia.id_tecnologia')),
    Column('id_tiempo', Integer, ForeignKey('dim_tiempo.id_tiempo')),
    Column('id_dispositivo', String),
    Column('cantidad_conexiones', Integer)
)

fact_status_conexion = Table('fact_status_conexion', metadata,
    Column('id_fact', Integer, primary_key=True),
    Column('id_celda', String, ForeignKey('dim_celda.id_celda')),
    Column('id_tiempo', Integer, ForeignKey('dim_tiempo.id_tiempo')),
    Column('conexiones', Integer),
    Column('errores', Integer),
    Column('caidas', Integer)
)

# === Crear las tablas en la base de datos ===

if __name__ == "__main__":
    print("Creando esquema en PostgreSQL...")
    metadata.create_all(engine)
    print("Tablas creadas exitosamente.")
