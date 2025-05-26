import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
import argparse

# Cargar entorno
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def cargar_status():
    print("📊 Leyendo archivo KPI...")
    df = pd.read_excel(args.file)
    df.columns = [c.lower() for c in df.columns]

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['fecha'] = df['timestamp'].dt.date.astype(str)
    df['hora'] = df['timestamp'].dt.hour

    with engine.begin() as conn:
        for _, row in df.iterrows():
            id_tiempo = conn.execute(
                text("""
                    SELECT id_tiempo FROM dim_tiempo WHERE fecha = :fecha AND hora = :hora
                """), {"fecha": row['fecha'], "hora": row['hora']}
            ).scalar()

            if id_tiempo:
                conn.execute(
                    text("""
                        INSERT INTO fact_status_conexion (id_celda, id_tiempo, conexiones, errores, caidas)
                        VALUES (:celda, :tiempo, :conex, :err, :caidas)
                    """), {
                        "celda": row['celda'],
                        "tiempo": id_tiempo,
                        "conex": row.get('conexiones', 0),
                        "err": row.get('errores', 0),
                        "caidas": row.get('caidas', 0)
                    }
                )

    print("✅ Datos cargados en fact_status_conexion.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Ruta al archivo CSV o Excel')
    args = parser.parse_args()
    cargar_status()
