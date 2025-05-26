import os
import pandas as pd
import argparse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar entorno
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def load_data(filepath):
    print("🔄 Leyendo archivo Excel...")
    df = pd.read_excel(filepath)
    df.columns = [col.strip().lower() for col in df.columns]
    
    df['ciudad'] = 'CABA'  # Asumimos fija

    required_cols = ['celda', 'sitio', 'sector', 'comuna', 'barrio']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Faltan columnas necesarias: {required_cols}")

    with engine.begin() as conn:
        ubicaciones = df[['ciudad', 'comuna', 'barrio']].drop_duplicates()
        for _, row in ubicaciones.iterrows():
            exists = conn.execute(
                text("""
                    SELECT id_ubicacion FROM dim_ubicacion
                    WHERE ciudad = :ciudad AND comuna = :comuna AND barrio = :barrio
                """), row.to_dict()).fetchone()
            if not exists:
                conn.execute(
                    text("""
                        INSERT INTO dim_ubicacion (ciudad, comuna, barrio)
                        VALUES (:ciudad, :comuna, :barrio)
                    """), row.to_dict()
                )

        for _, row in df.iterrows():
            row['ciudad'] = 'CABA'
            id_ubicacion = conn.execute(
                text("""
                    SELECT id_ubicacion FROM dim_ubicacion
                    WHERE ciudad = 'CABA' AND comuna = :comuna AND barrio = :barrio
                """), row.to_dict()).scalar()

            if id_ubicacion:
                conn.execute(
                    text("""
                        INSERT INTO dim_celda (id_celda, sitio, sector, id_ubicacion)
                        VALUES (:id_celda, :sitio, :sector, :id_ubicacion)
                        ON CONFLICT (id_celda) DO NOTHING
                    """), {
                        "id_celda": row['celda'],
                        "sitio": row['sitio'],
                        "sector": row['sector'],
                        "id_ubicacion": id_ubicacion
                    }
                )

    print("✅ Celdas y ubicaciones cargadas.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Ruta al archivo Excel de celdas')
    args = parser.parse_args()

    load_data(args.file)