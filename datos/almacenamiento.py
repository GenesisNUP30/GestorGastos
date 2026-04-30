"""
almacenamiento.py
Capa de persistencia del proyecto. Gestiona la lectura, escritura y exportación
de datos en formato JSON y TXT, asegurando integridad y manejo seguro de errores.
"""
import json
import os

def cargar_gastos(ruta: str) -> list:
    """Carga la lista de gastos desde un archivo JSON. Devuelve lista vacía si no existe o hay error."""
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Error al leer datos: {e}. Se iniciará un registro vacío.")
        return []

def guardar_gastos(ruta: str, datos: list) -> bool:
    """Guarda la lista de gastos en un archivo JSON con formato legible."""
    try:
        # Crea el directorio si no existe, sin lanzar error si ya está creado
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"❌ Error al guardar: {e}")
        return False

def exportar_txt(ruta: str, contenido: str) -> bool:
    """Exporta un resumen de texto a un archivo .txt en la carpeta de informes."""
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return True
    except IOError as e:
        print(f"❌ Error al exportar: {e}")
        return False

def cargar_configuracion(ruta: str) -> dict:
    """Carga la configuración de presupuestos. Retorna diccionario vacío si el archivo falta o está corrupto."""
    if not os.path.exists(ruta): return {}
    try:
        with open(ruta, "r", encoding="utf-8") as f: return json.load(f)
    except (json.JSONDecodeError, IOError): return {}

def guardar_configuracion(ruta: str, config: dict) -> bool:
    """Guarda o actualiza la configuración de presupuestos en formato JSON."""
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError: return False