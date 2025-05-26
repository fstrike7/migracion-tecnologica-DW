import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Cargar entorno
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Rango de fechas (ajustable)
start_date = datetime(2025, 5, 1)
end_date = datetime(2025, 5, 31)

def generar_dim_tiempo():
    print("🕒 Generando dimensión de tiempo...")

    fechas = []
    current = start_date
    while current <= end_date:
        for h in range(0, 24):
            fecha = current.date()
            fechas.append({
                "fecha": str(fecha),
                "hora": h,
                "dia": fecha.day,
                "mes": fecha.month,
                "anio": fecha.year
            })
        current += timedelta(days=1)

    df = pd.DataFrame(fechas)
    df.to_sql("dim_tiempo", engine, if_exists="append", index=False)
    print("✅ Cargada dim_tiempo con fechas del mes.")

if __name__ == "__main__":
    generar_dim_tiempo()
