# Guía de instalación y uso del DW de Migración Tecnológica

Este documento explica cómo instalar y ejecutar el proyecto localmente para probar o continuar el desarrollo.

---

## 📦 Requisitos

- Python 3.10+
- PostgreSQL (recomendado usar pgAdmin para gestión visual)
- Git

---

## 🚀 Instalación rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/fstrike7/migracion-tecnologica-DW.git
cd migracion-tecnologica-DW
```

### 2. Crear entorno virtual

``` bash
python -m venv .venv
source .venv/bin/activate        # En Mac/Linux
.venv\Scripts\activate           # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🔐 Configurar variables de entorno

Crear un archivo .env en la raíz del proyecto basado en .env.example:
```ini
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=proyecto_final_dw
```
- ⚠️ Asegurate de que la base proyecto_final_dw exista y esté en codificación UTF-8.

## 🛠️ Crear el esquema de base de datos

```bash
python scripts/create_dw_schema.py
```

## 📂 Cargar datos
 Copiá tus archivos reales a la carpeta /data (no están en el repo por privacidad).
```bash
# Crear dimensión de tiempo
python scripts/load_dim_tiempo.py

# Cargar celdas y ubicaciones
python scripts/load_dim_celda.py --file data/Celdas_sectores.xlsx

# Cargar registros de conexiones
python scripts/load_fact_uso_dispositivos.py --file data/muestra.csv

# Cargar KPIs de red
python scripts/load_fact_status_conexion.py --file data/KPI_status.xlsx
```

## 📊 Consultas útiles (ver carpeta /sql)
Podés ejecutar consultas SQL para validar los datos cargados. Ejemplo:
```sql
SELECT comuna, COUNT(*) FROM dim_ubicacion GROUP BY comuna;
```