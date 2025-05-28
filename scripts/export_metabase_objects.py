import requests
import json

# Configuración
MB_URL = "http://localhost:3000"
MB_USER = "admin@admin.com"
MB_PASSWORD = "admin123"

# Login
auth = requests.post(f"{MB_URL}/api/session", json={
    "username": MB_USER,
    "password": MB_PASSWORD
})
token = auth.json()["id"]
headers = {"X-Metabase-Session": token}

# Exportar dashboards
dashboards = requests.get(f"{MB_URL}/api/dashboard", headers=headers).json()
for dash in dashboards:
    dash_id = dash["id"]
    dash_data = requests.get(f"{MB_URL}/api/dashboard/{dash_id}", headers=headers).json()
    with open(f"metabase/exports/dashboard_{dash_id}.json", "w", encoding="utf-8") as f:
        json.dump(dash_data, f, indent=2)
