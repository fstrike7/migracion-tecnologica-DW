import requests
import json
import os

MB_URL = "http://localhost:3000"
MB_USER = "admin@admin.com"
MB_PASSWORD = "admin123"

auth = requests.post(f"{MB_URL}/api/session", json={
    "username": MB_USER,
    "password": MB_PASSWORD
})
token = auth.json()["id"]
headers = {"X-Metabase-Session": token}

exports_path = "metabase/exports/"
for filename in os.listdir(exports_path):
    if filename.endswith(".json"):
        with open(os.path.join(exports_path, filename), "r", encoding="utf-8") as f:
            data = json.load(f)
        new_dash = requests.post(f"{MB_URL}/api/dashboard", json={
            "name": data["name"],
            "description": data.get("description", ""),
        }, headers=headers)
        print(f"Importado: {data['name']}")
