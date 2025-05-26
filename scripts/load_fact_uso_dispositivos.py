# load_fact_uso_dispositivos.py

import argparse
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

# Cargar entorno
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def cargar_fact_uso():
    print("📄 Leyendo muestra.csv...")
    df = pd.read_csv(args.file)

    # Normalizar columnas
    df.columns = [c.lower() for c in df.columns]
    if 'timestamp' not in df.columns:
        raise Exception("No se encuentra columna 'timestamp' en el archivo CSV")

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['fecha'] = df['timestamp'].dt.date.astype(str)
    df['hora'] = df['timestamp'].dt.hour

    with engine.begin() as conn:
        print("🔗 Resolviendo claves y cargando datos...")

        for _, row in df.iterrows():
            id_tiempo = conn.execute(
                text("""
                    SELECT id_tiempo FROM dim_tiempo WHERE fecha = :fecha AND hora = :hora
                """), {"fecha": row['fecha'], "hora": row['hora']}
            ).scalar()

            id_tecnologia = conn.execute(
                text("""
                    SELECT id_tecnologia FROM dim_tecnologia WHERE tipo_red = :tipo AND proveedor = :prov
                """), {"tipo": row['tipo_red'], "prov": row['proveedor']}
            ).scalar()

            if id_tiempo and id_tecnologia:
                conn.execute(
                    text("""
                        INSERT INTO fact_uso_dispositivos (id_celda, id_tecnologia, id_tiempo, id_dispositivo, cantidad_conexiones)
                        VALUES (:celda, :tecnologia, :tiempo, :dispositivo, 1)
                    """), {
                        "celda": row['celda'],
                        "tecnologia": id_tecnologia,
                        "tiempo": id_tiempo,
                        "dispositivo": row['id_dispositivo']
                    }
                )

    print("✅ Datos cargados en fact_uso_dispositivos.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Ruta al archivo CSV o Excel')
    args = parser.parse_args()
    cargar_fact_uso()
