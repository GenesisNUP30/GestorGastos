"""
storage.py
Gestión de persistencia en JSON. Maneja carga, guardado y exportación de datos.
"""
import json
import os

def cargar_gastos(ruta: str) -> list:
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Error al leer datos: {e}. Se iniciará un registro vacío.")
        return []

def guardar_gastos(ruta: str, datos: list) -> bool:
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"❌ Error al guardar: {e}")
        return False

def exportar_txt(ruta: str, contenido: str) -> bool:
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return True
    except IOError as e:
        print(f"❌ Error al exportar: {e}")
        return False

def cargar_configuracion(ruta: str) -> dict:
    if not os.path.exists(ruta): return {}
    try:
        with open(ruta, "r", encoding="utf-8") as f: return json.load(f)
    except (json.JSONDecodeError, IOError): return {}

def guardar_configuracion(ruta: str, config: dict) -> bool:
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError: return False