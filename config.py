"""
config.py
Configuración global del proyecto. Define rutas, categorías por defecto y parámetros visuales.
"""
import os

# Determina la ruta base del proyecto y define directorios de trabajo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "almacen_datos")
REPORTES_DIR = os.path.join(BASE_DIR, "informes")

# Rutas completas para persistencia de datos y configuración de presupuestos (se crean si no existen)
EXPENSES_FILE = os.path.join(DATA_DIR, "gastos.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

# Categorías predefinidas para clasificar los registros
DEFAULT_CATEGORIES = ["comida", "transporte", "ocio", "estudio", "salud", "otros"]

# Nombres de archivo para exportaciones visuales y de texto
CHART_FILENAME = "grafico_gastos.png"
EXPORT_FILENAME = "resumen_gastos.txt"